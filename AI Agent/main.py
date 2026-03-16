# main.py
import os
from agent.agent_core import JavaToMavenAgent


def main():
    print("Java → Maven Agent")
    print("Start with: path <dir> → analyze → convert to convert project to maven\n")
    print("Type 'exit' to quit\n")

    agent = JavaToMavenAgent()

    while True:
        user_input = input(">> ").strip()

        if user_input.lower() == "exit":
            print("Thanks for using the Maven Convertor.Bye!")
            break

        if user_input.startswith("path"):
            project_path = user_input[len("path"):].strip().strip('"').strip("'")

            if not project_path:
                print(" Please provide a project path.")
                continue

            if not os.path.isdir(project_path):
                print("Invalid directory.")
                continue

            response = agent.set_project_path(project_path)
            print(response)
            continue

        if user_input == "analyze":
            response = agent.analyze()
            print(response)
            continue

        if user_input == "convert":
            response = agent.convert()
            print(response)
            
            choice = input("\n Show dependencies resolution report? (yes/no): ").strip().lower()
            if choice == "yes":
                print(agent.get_dependency_report())
                
            choice = input("\nRun 'mvn clean install -e'? (yes/no): ").strip().lower()
            if choice == "yes":
                print(agent.run_maven_build())

            continue
        

        print("""Unknown command. Command list
              1-path <dir> (provide java project path)
              2-analyze    (analyze the project)
              3-convert   (convert the project to maven-always analyze project before convert)
              4-exit""")


if __name__ == "__main__":
    main()


