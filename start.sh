#!/bin/sh

export LOCAL_REPOS=$1

echo 'Building docker image...'
docker build -q -t git-hook:latest .

echo 'Starting ngrok...'
~/ngrok http 80 > /dev/null &
export NGROK_PID=$!
sleep 2
export NGROK_HOST=$(curl --silent --show-error http://127.0.0.1:4040/api/tunnels | sed -nE 's/.*public_url":"https:..([^"]*).*/\1/p')
echo 'NGROK running at: '
echo https://${NGROK_HOST}/postreceive

echo 'Running Flask server...'
docker run -it --rm -p 80:80 \
       --mount type=bind,source=$LOCAL_REPOS,target=/repos \
       --mount type=bind,source=${LOCAL_REPOS}git-hook,target=/app \
       git-hook python app.py /repos/

echo 'Closing pipeline...'
kill $NGROK_PID