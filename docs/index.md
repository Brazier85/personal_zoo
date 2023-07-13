# Welcome to the docs

![](img/logo-no-background.svg){ width="500" }

Personal Zoo is a web application to keep track of your personal zoo.

!!! warning "Warning"
    
    This documentation is work in progress!

## Install requirements

You need a recent version of Docker to run the application. Please keep in mind, that this application is **not** ready to be accessible in the public due to the lack of authentication and authorization.

### Quick startup

1. Clone the repo from github
    ```
    git clone https://github.com/Brazier85/personal_zoo.git
    ```
2. Install docker<br>
    [See docker docs](https://docs.docker.com/get-docker/)
3. Run `run_docker.sh`
    ```bash
    sh run_docker.sh
    ```
4. Visit `<host/ip>:5000`

### Manual installation
To run the application without docker you need to install Python3 and some Submodules

```shell
# install submodules
python3 -m pip install -r requirements.txt

# Run the app
python3 main.py
```

## Using the application

After you have successfully started the application you can go to the settings page to change the basic settings as you need them.

