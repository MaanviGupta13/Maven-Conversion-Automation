def enrich_platform_dependencies(dependencies, project_type):
    def has(artifact_id):
        return any(d["artifactId"] == artifact_id for d in dependencies)

    if project_type in ["JSP", "Enterprise"]:
        if not has("javax.servlet-api"):
            dependencies.append({
                "groupId": "javax.servlet",
                "artifactId": "javax.servlet-api",
                "version": "3.1.0",
                "scope": "provided",
                "source": "PLATFORM"
            })

    if project_type == "JSP":
        if not has("jsp-api"):
            dependencies.append({
                "groupId": "javax.servlet.jsp",
                "artifactId": "jsp-api",
                "version": "2.2",
                "scope": "provided",
                "source": "PLATFORM"
            })

    if project_type == "Enterprise":
        if not has("javaee-api"):
            dependencies.append({
                "groupId": "javax",
                "artifactId": "javaee-api",
                "version": "7.0",
                "scope": "provided",
                "source": "PLATFORM"
            })

    #ant project
    if project_type == "Ant":
        if not has("junit"):
            dependencies.append({
                "groupId": "junit",
                "artifactId": "junit",
                "version": "4.8.2",
                "scope": "compile",
                "source": "PLATFORM"
            })

    if project_type == "Simple":
        # Do nothing platform-wise (intentionally)
        pass

    if not has("junit"):
        dependencies.append({
            "groupId": "junit",
            "artifactId": "junit",
            "version": "4.8.2",
            "scope": "compile",
            "source": "PLATFORM"
        })
    
    return dependencies
