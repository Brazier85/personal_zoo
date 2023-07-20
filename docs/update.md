# How to Stay Up to Date with Personal Zoo?

Staying up to date with Personal Zoo is crucial, not only for security reasons (refer to [security](/security)), but also to benefit from the latest improvements and enhancements I have made.

For users running Personal Zoo with Docker, you can update your installation with the following commands:
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
Pro Tip: You can automate these commands in a script to streamline the update process.

## Manual Installation

If you have a manual installation, updating the application is simple. Just run `git pull` in your application folder or start the `run_docker.sh` script.

After updating, it's advisable to visit the `<host/ip>:5000/update` page. This page will automatically update your database to incorporate the latest changes, if any.

## Automatic updates

As of now, Personal Zoo does not include an auto-update function. However, it is on my [roadmap](/roadmap) for future implementation.

Ensuring your Personal Zoo installation is up to date guarantees you'll have access to the latest features and improvements. Don't hesitate to check for updates regularly to make the most of our application!