import os
import subprocess
from tools.project_converter import restructure_project
from tools.dependency_finder import find_dependencies
from tools.dependency_mapper import map_dependencies
from tools.pom_generator import generate_pom
from tools.project_detector import detect_project_type, find_build_xml
from tools.build_analyzer import analyze_build_xml  
from tools.platform_dependencies import enrich_platform_dependencies


class JavaToMavenAgent:
    def __init__(self):
        self.maven_path = None
        self.project_path = None
        self.project_type = None
        self.raw_dependencies = None
        self.mapped_dependencies = None

    def set_project_path(self, path):
        self.project_path = path
        self.maven_path = os.path.join(path, "maven_project")
        return f"Project path set: {path}"

    def analyze(self):
        if not self.project_path:
            return "Project path not set."

        for root, dirs , files in os.walk(self.project_path):
            if "pom.xml" in files:
                pom_path = os.path.join(root,"pom.xml")
                return f"Maven project detected at {pom_path}. No conversion needed."

                
        self.build_xml_path = find_build_xml(self.project_path)

        self.project_type = detect_project_type(self.project_path)
        if not self.project_type:
            return "Unable to detect project type."


        self.raw_dependencies = find_dependencies(
            self.project_path,
            self.project_type
        )

        if self.build_xml_path:
            build_insights = analyze_build_xml(self.build_xml_path)
            self.raw_dependencies.setdefault("jars", [])
            self.raw_dependencies["jars"].extend(
                build_insights.get("jars", [])
            )

        jar_count = len(self.raw_dependencies.get("jars", []))

        return (
            f"Project type: {self.project_type}\n"
            f"JARs found: {jar_count}\n"
            f"build.xml found: {'Yes' if self.build_xml_path else 'No'}"
        )

    def convert(self):
        if not self.project_path:
            return "Project path not set."

        if not self.raw_dependencies:
            return "Analyze the project before convert."

        self.mapped_dependencies = map_dependencies(self.raw_dependencies.get("jars", []))

        # ALWAYS initialize from mapped dependencies
        resolved = self.mapped_dependencies.get("resolved", [])
        unresolved = self.mapped_dependencies.get("unresolved", [])

        os.makedirs(self.maven_path, exist_ok=True)
        restructure_project(self.project_path, self.maven_path, self.project_type)

        # enrich platform dependencies (Servlet API etc.)
        resolved = enrich_platform_dependencies(
            resolved,
            self.project_type
        )

        # generate pom with enriched deps
        generate_pom(self.maven_path, resolved, self.project_type)

        message = (
            "Maven conversion completed\n"
            f"Dependencies added: {len(resolved)}\n"
            f"Unresolved dependencies: {len(unresolved)}"
        )

        if unresolved:
            message += "\nUnresolved JARs:"
            for jar in unresolved:
                message += f"\n- {jar}"

        return message

    def run_maven_build(self):
        if not self.maven_path or not os.path.isdir(self.maven_path):
            return "Maven project not found. Cannot run Maven."

        try:
            process = subprocess.run(
                "mvn clean install -e",
                cwd=self.maven_path,
                shell=True,
                capture_output=True,
                text=True
            )

            if process.returncode == 0:
                return "Maven build successful."
            else:
                return (
                    "Maven build failed.\n"
                    "STDOUT:\n" + process.stdout +
                    "\nSTDERR:\n" + process.stderr
                )

        except FileNotFoundError:
            return "Maven not found. Ensure Maven is installed and in PATH."
    
    def get_dependency_report(self):
        lines = []

        lines.append("\n========== Dependency Resolution Summary ==========\n")

        # ---- 1. Total JARs found ----
        jars = (
            self.raw_dependencies.get("jars", [])
            if self.raw_dependencies else []
        )
        lines.append(f"1. Total JARs found: {len(jars)}")
        if jars:
            for jar in sorted(jars):
                lines.append(f"   - {jar}")
        else:
            lines.append("   None")

        # ---- Prepare resolved / unresolved from authoritative source ----
        resolved = (
            self.mapped_dependencies.get("resolved", [])
            if self.mapped_dependencies else []
        )
        unresolved = (
            self.mapped_dependencies.get("unresolved", [])
            if self.mapped_dependencies else []
        )

        # ---- 2. Knowledge Base resolved ----
        kb_resolved = [d for d in resolved if d.get("source") == "Knowledge Base"]
        lines.append(f"\n2. Dependencies added using Knowledge Base: {len(kb_resolved)}")
        if kb_resolved:
            for d in kb_resolved:
                lines.append(
                    f"   - {d.get('groupId')}:{d.get('artifactId')}:{d.get('version')}"
                )
        else:
            lines.append("   None")

        # ---- 3. Platform dependencies ----
        platform_resolved = [d for d in resolved if d.get("source") == "PLATFORM"]
        lines.append(f"\n3. Platform dependencies added: {len(platform_resolved)}")
        if platform_resolved:
            for d in platform_resolved:
                lines.append(
                    f"   - {d.get('groupId')}:{d.get('artifactId')}:{d.get('version')}"
                )
        else:
            lines.append("   None")

        # ---- 4. Maven Central resolved ----
        mc_resolved = [d for d in resolved if d.get("source") == "MAVEN_CENTRAL"]
        lines.append(f"\n4. Dependencies added using Maven Central: {len(mc_resolved)}")
        if mc_resolved:
            for d in mc_resolved:
                lines.append(
                    f"   - {d.get('groupId')}:{d.get('artifactId')}:{d.get('version')}"
                )
        else:
            lines.append("   None")

        # ---- 5. Unresolved dependencies ----
        lines.append(f"\n5. Unresolved dependencies: {len(unresolved)}")
        if unresolved:
            for jar in unresolved:
                lines.append(f"   - {jar}")
        else:
            lines.append("   None")

        lines.append("\n==================================================")
        return "\n".join(lines)
