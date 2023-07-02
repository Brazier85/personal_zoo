#/bin/bash

# Get new data
git pull

# Built new container
docker build -t personal_zoo .

# Stop old container
docker stop personal_zoo

# remove old container
docker rm personal_zoo

# Run new container
docker run -d -p 5000:5000 -v ./data:/app/data --name personal_zoo personal_zoo