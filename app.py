import hmac
import sys
import os
import logging

from hashlib import sha1
from github_webhook import Webhook
from flask import Flask, request, abort
from settings import REPOS, SECRET_KEY, LOG_FILE_LOCATION
from git import Repo
from logging.handlers import RotatingFileHandler


class GitKeeper(object):
    def __init__(self, home_path):
        self.repos = dict()

        for loc, repo_data in REPOS.items():
            repo_url = repo_data['url']
            working_branch = repo_data['default-branch']
            local_repo_path = home_path + loc

            if not os.path.isdir(local_repo_path):
                repo = Repo.clone_from(repo_url, local_repo_path)
                repo.git.checkout(working_branch)
                self.repos[loc] = {
                    'repo_obj': repo,
                    'working_branch': working_branch,
                }
            else:
                repo = Repo(local_repo_path)
                repo.git.pull()
                repo.git.checkout(working_branch)
                self.repos[loc] = {
                    'repo_obj': repo,
                    'working_branch': working_branch,
                }

    def pull(self, repo_name, branch_name):
        repo = self.repos.get(repo_name, None)
        repo_obj = repo['repo_obj']
        if not repo:
            app.logger.error('Repo {} not found!'.format(repo_name))
            return False
        if branch_name is repo['working_branch']:
            repo_obj.git.pull()
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
        branch = data[u'ref'].split('/')[-1]
        app.logger.info('Push event received for {}'.format(name))
        try:
            jenkins.pull(name, branch)
            app.logger.info('Pull success!')
        except Exception as e:
            app.logger.error('Pull failed with {}'.format(e))
        return '200 OK!'
    app.logger.warning(' 403 - Unverified request received!')
    return abort(403)

if __name__ == "__main__":
    handler = RotatingFileHandler(LOG_FILE_LOCATION, maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host="0.0.0.0", port=80)
