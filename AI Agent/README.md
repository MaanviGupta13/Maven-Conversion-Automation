Java → Maven Conversion Agent

This project is a rule-based Python agent that converts a normal (non-Maven) Java project into a Maven project automatically.

Many older Java projects store dependencies as JAR files and do not follow a standard build structure. This agent analyzes such projects, detects dependencies, reorganizes the project into the Maven directory structure, and generates a pom.xml file.


Agent Workflow

User → Input Project Path → Agent Brain → Detection Tools → Conversion → Maven Project → Dependency Report


Agent Steps

1. User Input
User provides the path of a Java project that is not using Maven.

2. Agent Brain
The main workflow is controlled by agent_core.py which coordinates all modules.

3. Project Detection
project_detector.py identifies the type of Java project:
- Simple Java project
- JSP/Web project
- Ant-based project

4. Dependency Discovery
dependency_finder.py scans the project to find JAR files from locations like:
- lib/
- dist/lib/
- WEB-INF/lib/
- build.xml

5. Dependency Mapping
dependency_mapper.py maps detected JAR files to Maven dependencies using a knowledge base JSON file.

Example:
servlet-api.jar → javax.servlet:javax.servlet-api

6. Project Conversion
project_converter.py reorganizes the project into Maven standard structure.

Before:

project/
src/
lib/
classes/

After:

project/
src/main/java
src/main/resources
src/test/java
pom.xml

7. POM Generation
pom_generator.py creates the pom.xml with the required dependencies and scopes.

8. Result
The output project becomes Maven compatible and can be built using Maven commands.

9. Explanation
The agent prints a dependency resolution report showing how dependencies were mapped.


Project Structure

java-maven-agent/

main.py                (entry point)
agent_core.py          (controls workflow)

project_detector.py    (detect project type)
dependency_finder.py   (find JAR dependencies)
dependency_mapper.py   (map JARs to Maven dependencies)

project_converter.py   (convert folder structure)
pom_generator.py       (generate pom.xml)

knowledge_base/
dependency_mapping.json


Features

- Rule-based agent system
- Automatic Java project detection
- JAR dependency scanning
- Knowledge-base dependency mapping
- Maven directory restructuring
- Automatic pom.xml generation
- Dependency resolution report


How to Run

Run the program:

python main.py

Then provide the path to the Java project.

Example:

Enter project path:
C:/projects/legacy-java-project


Output

The project is converted to Maven format:

project/
src/main/java
src/main/resources
src/test/java
pom.xml

Now the project can be built with:

mvn clean install


Author

Maanvi Gupta