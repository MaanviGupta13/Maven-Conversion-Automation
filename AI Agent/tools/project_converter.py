import os
import shutil

TEXT_EXTENSIONS = (".xml", ".properties", ".yml", ".yaml", ".json")

def restructure_project(src_path, dest_path, project_type):
   
    java_dest = os.path.join(dest_path, "src", "main", "java")
    res_dest  = os.path.join(dest_path, "src", "main", "resources")
    web_dest  = os.path.join(dest_path, "src", "main", "webapp")
    ear_dest  = os.path.join(dest_path, "src", "main", "ear")

    # Create dirs based on project type
    os.makedirs(java_dest, exist_ok=True)
    os.makedirs(res_dest, exist_ok=True)

    if project_type in ("JSP", "Enterprise"):
        os.makedirs(web_dest, exist_ok=True)

    if project_type == "Enterprise":
        os.makedirs(ear_dest, exist_ok=True)

    # Walk original project
    for root, dirs, files in os.walk(src_path):

        # Skip writing into maven output to avoid loop
        if dest_path in root:
            continue

        for f in files:
            old_path = os.path.join(root, f)

            # .JAVA
            if f.endswith(".java"):
                rel = os.path.relpath(root, src_path)
                copy_to(java_dest, rel, old_path)

            # CONFIG / RESOURCE
            elif f.endswith(TEXT_EXTENSIONS):
                shutil.copy2(old_path, res_dest)

            # JSP & HTML
            elif project_type in ("JSP", "Enterprise") and f.endswith((".jsp", ".html")):
                rel = os.path.relpath(root, src_path)
                copy_to(web_dest, rel, old_path)

            # WEB-INF or XML descriptors
            elif "WEB-INF" in root and project_type in ("JSP", "Enterprise"):
                rel = os.path.relpath(root, src_path)
                copy_to(web_dest, rel, old_path)

            # EAR structure
            elif project_type == "Enterprise" and (
                "APP-INF" in root or "META-INF" in root
            ):
                rel = os.path.relpath(root, src_path)
                copy_to(ear_dest, rel, old_path)

def copy_to(base, rel_path, src_file):
    target_dir = os.path.join(base, rel_path)
    os.makedirs(target_dir, exist_ok=True)
    shutil.copy2(src_file, target_dir)
