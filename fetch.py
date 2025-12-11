import requests, json, os

GITHUB_USER = "BK3820"  # change this
TOKEN = os.getenv("GH_TOKEN")

headers = {"Authorization": f"Bearer {TOKEN}"}

# --- Fetch repositories ---
repos = requests.get(
    f"https://api.github.com/users/{GITHUB_USER}/repos?per_page=100",
    headers=headers,
).json()

output = []

for r in repos:
    name = r["name"]
    archived = r["archived"]

    # --- Last Committer ---
    commits = requests.get(
        f"https://api.github.com/repos/{GITHUB_USER}/{name}/commits",
        headers=headers,
    ).json()
    last_commit = (
        commits[0]["commit"]["author"]["name"] if commits and type(commits) == list else "N/A"
    )

    # --- Secrets Check ---
    secrets = requests.get(
        f"https://api.github.com/repos/{GITHUB_USER}/{name}/actions/secrets",
        headers=headers,
    ).json()
    has_secrets = len(secrets.get("secrets", [])) > 0

    # --- Append final data ---
    output.append({
        "repo": name,
        "archived": archived,
        "has_secrets": has_secrets,
        "last_committer": last_commit,
        "updated_at": r["updated_at"],
    })

with open("data.json", "w") as f:
    json.dump(output, f, indent=2)

print("Generated data.json")
