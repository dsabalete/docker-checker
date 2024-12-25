from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
import requests
import subprocess


# Load environment variables from .env file
load_dotenv()

# Read Docker Hub credentials from environment variables
DOCKER_HUB_USERNAME = os.environ.get('DOCKER_HUB_USERNAME')
DOCKER_HUB_TOKEN = os.environ.get('DOCKER_HUB_TOKEN')

# Add validation to ensure variables are set
if not DOCKER_HUB_USERNAME or not DOCKER_HUB_TOKEN:
    raise ValueError("Please set DOCKER_HUB_USERNAME and DOCKER_HUB_TOKEN environment variables")

# Constants
API_BASE_URL = "https://hub.docker.com/v2/repositories"
THRESHOLD_DAYS = 180  # 6 months
HEADERS = {"Authorization": f"JWT {DOCKER_HUB_TOKEN}"}

def get_repositories():
    """Fetch all public repositories for the user."""
    url = f"{API_BASE_URL}/{DOCKER_HUB_USERNAME}/"
    repositories = []
    while url:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        repositories.extend(data["results"])
        url = data.get("next")
    return repositories

def get_tags(repo_name):
    """Fetch all tags for a repository."""
    url = f"{API_BASE_URL}/{DOCKER_HUB_USERNAME}/{repo_name}/tags"
    tags = []
    while url:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        tags.extend(data["results"])
        url = data.get("next")
    return tags

def re_push_image(repo_name, tag):
    """Pull, re-tag, and push the image."""
    image = f"{DOCKER_HUB_USERNAME}/{repo_name}:{tag}"
    print(f"Updating image: {image}")
    subprocess.run(["docker", "pull", image], check=True)
    subprocess.run(["docker", "tag", image, image], check=True)
    subprocess.run(["docker", "push", image], check=True)

def main():
    repositories = get_repositories()
    now = datetime.now(timezone.utc)
    threshold_date = now - timedelta(days=THRESHOLD_DAYS)

    for repo in repositories:
        repo_name = repo["name"]
        print(f"Checking repository: {repo_name}")
        tags = get_tags(repo_name)

        for tag in tags:
            last_updated = datetime.strptime(tag["last_updated"], "%Y-%m-%dT%H:%M:%S.%fZ")
            last_updated = last_updated.replace(tzinfo=timezone.utc)
            if last_updated < threshold_date:
                print(f"Tag '{tag['name']}' in repo '{repo_name}' is nearing inactivity threshold. Updating...")
                re_push_image(repo_name, tag["name"])

if __name__ == "__main__":
    main()