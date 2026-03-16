import os


def detect_project_type(project_path):

    # Enterprise FIRST (even if build.xml exists)
    if (
        os.path.isdir(os.path.join(project_path, "APP-INF")) or
        _file_exists_recursive(project_path, "application.xml") or
        _dir_exists_recursive(project_path, "EAR")
    ):
        return "Enterprise"

    #  JSP / Web
    if (
        os.path.isdir(os.path.join(project_path, "WEB-INF")) or
        _file_exists_recursive(project_path, "web.xml")
    ):
        return "JSP"

    # Ant-based (non-web, non-enterprise)
    if os.path.isfile(os.path.join(project_path, "build.xml")):
        if _file_exists_recursive(project_path, "import javafx."):
            return "Ant-JavaFX"
        return "Ant"

    # Basic Java
    if _file_exists_recursive(project_path, ".java"):
        return "Simple"

    return None

#to prevent recursive os.walk calls
def _file_exists_recursive(root, extension):
    for _, _, files in os.walk(root):
        for f in files:
            if f.endswith(extension):
                return True
    return False

# 
def _dir_exists_recursive(root, dirname):
    for dirpath, dirnames, _ in os.walk(root):
        if dirname in dirnames:
            return True
    return False

# to find build.xml
def find_build_xml(project_path):
    for root, dirs , files in os.walk(project_path):
            if "build.xml" in files:
                    return os.path.join(root, "build.xml")  
    return None
