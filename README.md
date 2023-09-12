# Personal Zoo

## Purpose

This webapp is for managing my "personal zoo" @home. You can add animals, there feedings, ect...

A full documentation with more details can be found [here](https://personal-zoo.com)

Currently the app is still under development and not stable.

### **The app is NOT production ready!**

## Startup

1. Clone this repo
    ```
    git clone https://github.com/Brazier85/personal_zoo.git
    ```
2. Install docker

    [See docker docs](https://docs.docker.com/get-docker/)
3. Run `run_docker.sh`
    ```bash
    sh run_docker.sh
    ```
4. Visit `<host/ip>:5000`

### Update

Just start the `run_docker.sh` file again. It will pull the latest changes from github and build a new container.

## Docker manual version
```bash
docker build -t personal_zoo .

docker run -d -p 5000:5000 -v ./data:/app/data --name personal_zoo personal_zoo
```
**Note:** The `data` mount is important. Without you will loose your settings after each update!

## DEVELOPMENT

### Startup
```bash
python3 -m pip install -r requirements.txt
```

### ENV
```bash
FLASK_ENV=dev # For dev -> If not set it will use prod
```

### Change `requirements.txt`
```bash

#create venv
python3 -m venv venv

#activate venv
source venv/bin/activate

# install packages
pip install flask

# create requirements.txt
pip freeze > requirements.txt

# For new versions
backports.zoneinfo==0.2.1;python_version<"3.9"

# deactivate venv
deactivate

```

## Docs

```bash

# Requirements
python3 m pip install mkdocs-material

# Build docs
python3 -m mkdocs build

# Test docs
python3 -m mkdocs serve

```
