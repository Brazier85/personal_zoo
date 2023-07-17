# How to stay up to date?

Being up to date with Personal Zoo is very important. Not only for security reasons (See [security](/security)) but also to be in sync with the latest improvements I made.

Run the following commands to update your installation.
```bash
# Pull new image
docker pull brazier85/personal_zoo:latest

# Stop old container
docker stop personal_zoo

# Remove old container
docker rm personal_zoo

# Start new container
docker run -d -p 5000:5000 -v ./data:/app/data --name personal_zoo brazier85/personal_zoo:latest
```
Hint: You can use the commands above in a script

## Manual installation
To update the application you only have to run `git pull` in your application folder or start the `run_docker.sh`-script.

After the update you should visit the `<host/ip>:5000/update`-page. This page will update your database to the latest changes if there are any.

## Automatic updates

At the current time, my application does not have a auto update function implemented.  But you can find this function on my [roadmap](/roadmap).