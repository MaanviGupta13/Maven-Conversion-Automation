Java → Maven Conversion Agent

This project is a rule-based Python agent that converts a non-Maven Java project into a Maven project automatically.

Many legacy Java projects store dependencies as JAR files inside folders like lib/, WEB-INF/lib/, or dist/lib/ and do not follow the standard Maven directory structure. This agent analyzes such projects, detects dependencies from JAR files, maps them to Maven coordinates using a knowledge base, restructures the project into the Maven layout, and generates a pom.xml.

After conversion, the project can be built using Maven.


How to Run the Project

1. Start the agent

Run the main program:

python main.py

You will see the interactive agent prompt.


2. Set the project path

Provide the path to the non-Maven Java project using:

path <project-directory>

Example:

path "C:/projects/legacy-java-project"

The agent will store the project path for analysis.


3. Analyze the project

Run:

analyze

The agent will inspect the project and display information such as:

- Project type (Simple / JSP / Ant)
- Number of JAR dependencies found
- Whether a build.xml file exists


4. Convert the project

Run:

convert

During this step the agent will:

- Load the dependency knowledge base
- Map JAR files to Maven dependencies
- Add required platform dependencies (Servlet API, JSP API, JUnit)
- Restructure the project into Maven directory layout
- Generate a pom.xml


5. View dependency resolution report (optional)

After conversion, the agent can display a dependency resolution report showing:

- Total JARs discovered
- Dependencies resolved using the knowledge base
- Platform dependencies added automatically
- Dependencies resolved from Maven Central
- Any unresolved dependencies


6. Build the project

The agent can optionally run:

mvn clean install -e

If the build succeeds, the project is now a fully buildable Maven project.


Exit

To close the agent, type:

exit
