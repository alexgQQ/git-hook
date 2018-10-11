## Install

This is a simple flask server to catch push events from github webhook.
Use ngrok and port 80 as a endpoint.

Build `docker build -t git-hook:latest .`
Run `docker run -it --rm -p 80:80 --mount type=bind,source=$LOCAL_REPOS,target=/repos git-hook python app.py /repos/`
