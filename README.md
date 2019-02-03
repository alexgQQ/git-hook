## Install

This is a simple flask server to catch push events from github webhook.
Use ngrok and port 80 as a endpoint.

Download [ngrok binary](https://ngrok.com/download) to the user home directory.

Simply run with `~/ngrok http 80`

Build docker image with `docker build -t git-hook:latest .`

Set `LOCAL_REPOS` envrionmental variable.
This will map the repos you want to pull and update to the local filesystem
`export LOCAL_REPOS=/repos/live/here`

Run application with `docker run -it --rm -p 80:80 \
                             --mount type=bind,source=$LOCAL_REPOS,target=/repos \
                             --mount type=bind,source=${LOCAL_REPOS}/git-hook,target=/app \
                             git-hook python app.py /repos/`

For convenience `start.sh /repos/live/here` will handle startup with ease.
