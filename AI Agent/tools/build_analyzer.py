import os
import xml.etree.ElementTree as ET
import re

def analyze_build_xml(build_xml_path):
    
    insights = {
        "jars": []
    }

    if not build_xml_path or not os.path.isfile(build_xml_path):
        return insights

    tree = ET.parse(build_xml_path)
    root = tree.getroot()

    for elem in root.iter():
        location = elem.attrib.get("location")

        if location and location.endswith(".jar"):
            jar_name = os.path.basename(location)
            version = _extract_version(jar_name)

            insights["jars"].append({
                "jar": jar_name,
                "path": location,
                "version_hint": version,
                "source": "build.xml"
            })

    return insights


def _extract_version(jar_name):
    match = re.search(r"-(\d+[\w\.-]*)\.jar$", jar_name)
    return match.group(1) if match else None
