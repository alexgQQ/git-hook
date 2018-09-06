from github_webhook import Webhook
from flask import Flask
from repos import REPOS
from git import Repo
import sys
import os


class GitKeeper(object):
    def __init__(self, home_path):
        self.repos = dict()

        for loc, repo_url in REPOS.items():
            local_repo_path = home_path + loc

            if not os.path.isdir(local_repo_path):
                self.repos[loc] = Repo.clone_from(repo_url, local_repo_path)
            else:
                self.repos[loc] = Repo(local_repo_path)

    def pull(self, repo_name):
        repo = self.repos.get(repo_name, None)
        if not repo:
            print('Error - Repo: %s not found!', repo_name)
            return False
        repo.git.pull()
        return True


jenkins = GitKeeper(sys.argv[1])


app = Flask(__name__)
webhook = Webhook(app) # /postreceive endpoint

@app.route("/")
def hello_world():
    return "Hello, World!"

@webhook.hook()
def on_push(data):
    name = data[u'repository'][u'name']
    print('Push received for %s repo', name)
    try:
        jenkins.pull(name)
    except Exception as e:
        print('Push failed with %s', e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
