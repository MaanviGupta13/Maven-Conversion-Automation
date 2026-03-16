import os
import xml.etree.ElementTree as ET


def find_dependencies(project_path, project_type):
    """
    Finds all JAR dependencies in a legacy Java project.
    Detection is ADDITIVE and does not stop after first match.
    """

    jars = set()

    # 1. Known lib locations by project type
    lib_dirs = _get_lib_dirs(project_type)

    for lib_dir in lib_dirs:
        jars.update(_scan_dirs(project_path, [lib_dir]))

    # 2. Classpath (Eclipse / Ant style)
    jars.update(_scan_classpath(project_path))

    # 3. Brute force fallback (safety net)
    jars.update(_brute_lib_scan(project_path))

    return {
        "jars": sorted(jars)
    }


#helper functions

def _get_lib_dirs(project_type):
    """
    Centralized knowledge of common lib directories.
    """
    common = [
        "lib",
        "libs",
        "dist/lib",
        "build/lib"
    ]

    if project_type == "Simple":
        return common

    if project_type == "JSP":
        return common + [
            "WEB-INF/lib"
        ]

    if project_type in ["Ant", "Enterprise"]:
        return common + [
            "APP-INF/lib",
            "common/lib",
            "shared/lib",
            "WEB-INF/lib"
        ]

    return common


def _scan_dirs(root, dir_list):
    found = []
    for parent, _, files in os.walk(root):
        for d in dir_list:
            if d.lower() in parent.lower():
                for f in files:
                    if f.lower().endswith(".jar"):
                        found.append(f)
    return found


def _scan_classpath(project_path):
    jars = []
    classpath_file = os.path.join(project_path, ".classpath")

    if not os.path.isfile(classpath_file):
        return jars

    try:
        tree = ET.parse(classpath_file)
        root = tree.getroot()

        for entry in root.findall("classpathentry"):
            if entry.get("kind") == "lib":
                path = entry.get("path")
                if path and path.lower().endswith(".jar"):
                    jars.append(os.path.basename(path))
    except Exception:
        pass

    return jars


def _brute_lib_scan(project_path):
    jars = []

    for root, _, files in os.walk(project_path):
        if "lib" in root.lower():
            for f in files:
                if f.lower().endswith(".jar"):
                    jars.append(f)

    return jars
