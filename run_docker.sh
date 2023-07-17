#/bin/bash

# Get new data
echo "Pull new data"
git pull

# Built new container
#echo "built new container"
#docker build -t personal_zoo .

echo "pull latest image"
docker pull brazier85/personal_zoo:latest

# Stop old container
echo "Stop old container"
docker stop personal_zoo

# remove old container
echo "Remove old container"
docker rm personal_zoo

echo "Remove old images"
docker image prune -a --force --filter "until=240h"

# Run new container
echo "Start new container"
docker run -d -p 5000:5000 -v ./data:/app/data --name personal_zoo brazier85/personal_zoo:latest

echo "done"

IP=$(hostname -I | awk '{print $1}')

echo ""
echo "Please visit the update page: http://$IP:5000/update"