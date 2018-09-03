from github_webhook import Webhook
from flask import Flask
import git


def update_repo(to_update):
    home = r'~/Development/RPI/'
    try:
        print('Pulling %s repo...'.format(to_update))
        repo = git.Repo(home + to_update)
        origin = repo.remotes.origin
        origin.pull()
        return True
    except Exception as e:
        print('Pull for %s repo failed !!'.format(to_update))
        print('Error: %s'.format(e))
        return False

app = Flask(__name__)
webhook = Webhook(app) # /postreceive endpoint

@app.route("/")
def hello_world():
    return "Hello, World!"

@webhook.hook()
def on_push(data):
    name = data[u'repository'][u'name']
    print('Push received for %s repo', name)
    update_repo(name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
