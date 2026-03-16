import json
import os
import re

from tools.repository_search import search_maven_central


def normalize_jar_name(jar_name):
    return re.sub(r"-\d+[\w\.-]*\.jar$", ".jar", jar_name)


def map_dependencies(jars):
    knowledge = _load_knowledge_base()

    resolved = []
    unresolved = []

    for jar in jars:
        jar_name = os.path.basename(jar).lower()

        artifact, version = _extract_artifact_and_version(
            jar_name.replace(".jar", "")
        )

        # normalize jar name for KB lookup
        normalized_jar = normalize_jar_name(jar_name)
        artifact_name = normalized_jar.replace(".jar", "").replace("-bin", "")

        # Checking Knowledge Base first
        if artifact_name in knowledge:
            meta = knowledge[artifact_name]

            final_version = version if version else meta.get("version")
            if not final_version:
                unresolved.append(jar)
                continue

            dep_entry = {
                "groupId": meta["groupId"],
                "artifactId": meta["artifactId"],
                "version": final_version,
                "source": "Knowledge Base"
            }

            # forward classifier if present (json-lib case)
            if meta.get("classifier"):
                dep_entry["classifier"] = meta["classifier"]

            # forward scope if present
            if meta.get("scope"):
                dep_entry["scope"] = meta["scope"]

            resolved.append(dep_entry)

        #  Fallback to Maven Central for unknown artifacts
        else:
            maven_dep = search_maven_central(artifact_name)

            if maven_dep:
                final_version = version if version else maven_dep.get("version")
                if not final_version:
                    unresolved.append(jar)
                    continue

                resolved.append({
                    "groupId": maven_dep["groupId"],
                    "artifactId": maven_dep["artifactId"],
                    "version": final_version,
                    "source": "MAVEN_CENTRAL"
                })
            else:
                unresolved.append(jar)


    return {
        "resolved": resolved,
        "unresolved": unresolved,
    }


def _load_knowledge_base():
    base_path = os.path.dirname(os.path.dirname(__file__))
    knowledge_path = os.path.join(
        base_path, "knowledge", "known_dependencies.json"
    )

    print("Loading JSON from:", knowledge_path)

    with open(knowledge_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _extract_artifact_and_version(name):
    match = re.match(r"(.+)-(\d+(\.\d+)+)", name)

    if not match:
        return None, None

    return match.group(1), match.group(2)
