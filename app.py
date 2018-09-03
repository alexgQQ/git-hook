from github_webhook import Webhook
from flask import Flask
import git


def update_repo(to_update):
    home=r'~/Development/RPI/'
    try:
        g = git.cmd.Git(home + to_update)
        g.pull
        return True
    except:
        print('Pull for %s repo failed !!', to_update)
        return False

app = Flask(__name__)
webhook = Webhook(app) # /postreceive endpoint

@app.route("/")
def hello_world():
    return "Hello, World!"

@webhook.hook()
def on_push(data):
    update_repo(data[u'repository'][u'name'])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
