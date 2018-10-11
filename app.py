import hmac
import sys
import os

from hashlib import sha1
from github_webhook import Webhook
from flask import Flask, request, abort
from settings import REPOS, SECRET_KEY
from git import Repo


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

    def validate_header(self):
        header_signature = request.headers.get('X-Hub-Signature')
        if header_signature is None:
            return False

        sha_name, signature = header_signature.split('=')
        if sha_name != 'sha1':
            return False

        mac = hmac.new(SECRET_KEY, msg=request.data, digestmod='sha1')

        if not str(mac.hexdigest()) == str(signature):
            return False

        return True


jenkins = GitKeeper(sys.argv[1])


app = Flask(__name__)
webhook = Webhook(app) # /postreceive endpoint

@webhook.hook()
def on_push(data):
    if jenkins.validate_header():
        name = data[u'repository'][u'name']
        print('Push received for %s repo', name)
        try:
            jenkins.pull(name)
        except Exception as e:
            print('Push failed with %s', e)
        return '200 OK!'
    return abort(403)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
