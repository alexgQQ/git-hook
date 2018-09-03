from github_webhook import Webhook
from flask import Flask
import git
import pprint


def update_repos(self, to_update):
    home=r'~/Development/RPI/'
    g = git.cmd.Git(home + to_update)
    g.pull

app = Flask(__name__)
webhook = Webhook(app) # /postreceive endpoint

@app.route("/")
def hello_world():
    return "Hello, World!"

@webhook.hook()
def on_push(data):
    pprint.pprint(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
