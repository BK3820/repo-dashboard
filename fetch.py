import requests, json, os

GITHUB_USER = "BK3820"  # change here if needed
TOKEN = os.getenv("GH_TOKEN", "").strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

# ---- Fetch all repositories ----
repos = requests.get(
    f"https://api.github.com/users/{GITHUB_USER}/repos?per_page=100",
    headers=headers
).json()

output = []

for r in repos:
    name = r.get("name")
    archived = r.get("archived", False)

    # ---- Last Committer ----
    commits = requests.get(
        f"https://api.github.com/repos/{GITHUB_USER}/{name}/commits",
        headers=headers
    ).json()

    if isinstance(commits, list) and len(commits) > 0:
        last_committer = commits[0]["commit"]["author"]["name"]
    else:
        last_committer = "N/A"

    # ---- Has Secrets ----
    secrets = requests.get(
        f"https://api.github.com/repos/{GITHUB_USER}/{name}/actions/secrets",
        headers=headers
    ).json()

    has_secrets = len(secrets.get("secrets", [])) > 0

    # ---- Append data ----
    output.append({
        "repo": name,
        "archived": archived,
        "has_secrets": has_secrets,
        "last_committer": last_committer,
        "updated_at": r.get("updated_at")
    })

# ---- Write JSON Output ----
with open("data.json", "w") as f:
    json.dump(output, f, indent=2)

print("Generated data.json")
