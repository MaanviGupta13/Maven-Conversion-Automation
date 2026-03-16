import os
import xml.etree.ElementTree as ET


def generate_pom(project_path, dependencies, project_type):

    pom_path = os.path.join(project_path, "pom.xml")

    project = ET.Element("project", {
        "xmlns": "http://maven.apache.org/POM/4.0.0",
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsi:schemaLocation": (
            "http://maven.apache.org/POM/4.0.0 "
            "http://maven.apache.org/xsd/maven-4.0.0.xsd"
        )
    })

    ET.SubElement(project, "modelVersion").text = "4.0.0"
    ET.SubElement(project, "groupId").text = _safe_name(project_path)
    ET.SubElement(project, "artifactId").text = _safe_name(project_path)
    ET.SubElement(project, "version").text = "1.0-SNAPSHOT"

    is_web = project_type in ["JSP", "Enterprise"]
    packaging = "war" if is_web else "jar"
    ET.SubElement(project, "packaging").text = packaging

    # properties
    properties = ET.SubElement(project, "properties")
    ET.SubElement(properties, "java.version").text = "1.8"
    ET.SubElement(properties, "project.build.sourceEncoding").text = "UTF-8"

    # Dependencies
    dependencies_node = ET.SubElement(project, "dependencies")

    for dep in dependencies:
        if not _is_valid(dep):
            continue

        dep_node = ET.SubElement(dependencies_node, "dependency")
        ET.SubElement(dep_node, "groupId").text = dep["groupId"]
        ET.SubElement(dep_node, "artifactId").text = dep["artifactId"]
        ET.SubElement(dep_node, "version").text = dep["version"]

        # Optional scope support
        if dep.get("scope"):
            ET.SubElement(dep_node, "scope").text = dep["scope"]

        if dep.get("classifier"):
            ET.SubElement(dep_node, "classifier").text = dep["classifier"]

    build = ET.SubElement(project, "build")

    # Resources
    resources = ET.SubElement(build, "resources")

    r1 = ET.SubElement(resources, "resource")
    ET.SubElement(r1, "directory").text = "src/main/resources"

    r2 = ET.SubElement(resources, "resource")
    ET.SubElement(r2, "directory").text = "src/main/java"
    includes = ET.SubElement(r2, "includes")
    ET.SubElement(includes, "include").text = "**/*.xml"
    ET.SubElement(includes, "include").text = "**/*.properties"

    # Compiler plugin
    plugins = ET.SubElement(build, "plugins")

    compiler = ET.SubElement(plugins, "plugin")
    ET.SubElement(compiler, "groupId").text = "org.apache.maven.plugins"
    ET.SubElement(compiler, "artifactId").text = "maven-compiler-plugin"
    ET.SubElement(compiler, "version").text = "3.8.1"

    config = ET.SubElement(compiler, "configuration")
    ET.SubElement(config, "source").text = "${java.version}"
    ET.SubElement(config, "target").text = "${java.version}"

    if packaging == "war":
        war_plugin = ET.SubElement(plugins, "plugin")
        ET.SubElement(war_plugin, "groupId").text = "org.apache.maven.plugins"
        ET.SubElement(war_plugin, "artifactId").text = "maven-war-plugin"
        ET.SubElement(war_plugin, "version").text = "3.4.0"

        war_config = ET.SubElement(war_plugin, "configuration")
        ET.SubElement(war_config, "failOnMissingWebXml").text = "false"

    # XML formatting
    _indent(project)
    tree = ET.ElementTree(project)
    tree.write(pom_path, encoding="utf-8", xml_declaration=True)


def _is_valid(dep):
    return all(dep.get(k) for k in ("groupId", "artifactId", "version"))


def _safe_name(path):
    return os.path.basename(os.path.abspath(path)).lower().replace(" ", "-")


def _indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for child in elem:
            _indent(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = i
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i
