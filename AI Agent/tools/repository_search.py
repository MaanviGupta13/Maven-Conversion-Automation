import json
import urllib.request
import urllib.parse


def search_maven_central(artifact_id):
   
    base_url = "https://search.maven.org/solrsearch/select"

    params = {
        "q": f"a:{artifact_id}",
        "rows": 1,
        "wt": "json"
    }

    url = base_url + "?" + urllib.parse.urlencode(params)

    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))

        docs = data.get("response", {}).get("docs", [])
        if not docs:
            return None

        doc = docs[0]
        return {
            "groupId": doc.get("g"),
            "artifactId": doc.get("a"),
            "version": doc.get("v")
        }

    except Exception as e:
        print(f"[WARN] Maven Central lookup failed for {artifact_id}: {e}")
        return None

