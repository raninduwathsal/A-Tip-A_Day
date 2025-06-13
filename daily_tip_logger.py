import os
import random
import requests
import subprocess
from datetime import datetime

with open("/home/debian/cron_debug.log", "a") as f:
    f.write(f"Script ran at {datetime.now()}\n")

REPO_PATH = os.path.dirname(os.path.abspath(__file__))
CATEGORIES = ['python', 'javascript', 'typescript', 'react', 'vue', 'angular', 'webdev', 'html', 'css', 'tailwindcss', 'frontend', 'backend', 'node', 'express', 'api', 'sql', 'postgresql', 'mongodb', 'mysql', 'devops', 'docker', 'kubernetes', 'terraform', 'ansible', 'aws', 'azure', 'gcp', 'cloud', 'ci', 'github', 'gitlab', 'git', 'linux', 'bash', 'shell', 'security', 'cybersecurity', 'networking', 'machinelearning', 'deeplearning', 'datascience', 'ai', 'nlp', 'blockchain', 'web3', 'solidity', 'programming', 'beginners', 'productivity', 'testing', 'unittesting', 'tdd', 'debugging', 'performance', 'softwareengineering', 'architecture', 'clean-code', 'oop', 'designpatterns', 'freelancing', 'remote', 'career', 'interview', 'resume', 'opensource', 'game-dev', 'gamedev', 'unity', 'godot', 'rust', 'go', 'csharp', 'java', 'kotlin', 'swift', 'android', 'ios', 'flutter', 'dart']
FALLBACK_TIPS = {'python': 'Use list comprehensions for concise loops.', 'javascript': 'Always use === instead of == for comparisons.', 'devops': 'Automate deployments using CI/CD tools.', 'git': 'Use `git stash` to save your changes temporarily.', 'docker': 'Keep your Docker images lean by using slim base images.', 'linux': 'Use `htop` to monitor your system performance in real-time.'}
GIT_BRANCH = "main"

today = datetime.now().strftime("%Y-%m-%d")
category = random.choice(CATEGORIES)
api_url = f"https://dev.to/api/articles?tag={category}&top=10"

try:
    response = requests.get(api_url, timeout=10)
    response.raise_for_status()
    data = response.json()
    if data:
        article = random.choice(data)
        title = article.get("title", "No title")
        url = article.get("url", "No URL")
    else:
        raise ValueError("No articles found.")
except Exception as e:
    print(f"[ERROR] Using fallback for {category}: {e}")
    title = FALLBACK_TIPS.get(category, "No fallback tip available.")
    url = "N/A"

category_path = os.path.join(REPO_PATH, category.replace("-", "_").capitalize())
os.makedirs(category_path, exist_ok=True)
filename = os.path.join(category_path, f"tip-{today}.md")

with open(filename, "w") as f:
    f.write(f"# {category.capitalize()} Tip - {today}\n\n")
    f.write(f"**Title:** {title}\n\n")
    f.write(f"**Link:** {url}\n\n")
    f.write("_Automatically added._\n")

# Git commit & push
try:
    subprocess.run(["git", "-C", REPO_PATH, "add", "."], check=True)
    subprocess.run(["git", "-C", REPO_PATH, "commit", "-m", f"Add {category} tip for {today}"], check=True)
    subprocess.run(["git", "-C", REPO_PATH, "push", "origin", GIT_BRANCH], check=True)
    print("Tip committed and pushed successfully.")
except subprocess.CalledProcessError as e:
    print(f"[ERROR] Git operation failed: {e}")
