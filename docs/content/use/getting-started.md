---
title: Getting Started
weight: -20
---

This page tells you how to get started with your personal zoo.

<!--more-->

{{< toc >}}

## Install requirements

You need a recent version of Docker to run the application. Please keep in mind, that this application is ready to be accessible in the public due to the lack of authentication and authorization.

### Quick startup

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

### Manuel installation
To run the application without docker you need to install Python3 and some Submodules

```shell
# install submodules
python3 -m pip install -r requirements.txt

# Run the app
python3 main.py
```

## Using the application

After you have successfully started the application you can go to the settings page to change the basic settings as you need them.
