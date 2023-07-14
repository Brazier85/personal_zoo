# Getting started

## Requirements
 
There are two main ways to run this application. First with Docker (recommended) and secondly als local python app. So you must have:

 - Docker 

or

- Python3

Please keep in mind, that this application is **not** ready to be accessible in the public due to the lack of authentication and authorization. (See [security](/security))

### Quick startup (Docker)

1. Clone the repo from github
    ``` bash
    git clone https://github.com/Brazier85/personal_zoo.git
    ```
2. Install docker<br>
    [See docker docs](https://docs.docker.com/get-docker/){:target="_blank"}
3. Run `run_docker.sh`
    ``` bash
    sh run_docker.sh
    ```
4. Visit `<host/ip>:5000`

### Manual installation
To run the application without docker you need to install Python3 and some Submodules

It is recommended to use a [virtual environment](https://docs.python.org/3/library/venv.html){:target="_blank"}..

``` bash
# install submodules
python3 -m pip install -r requirements.txt

# Run the app
python3 main.py
```

## Using the application

After you have successfully started the application you can go to the settings page to change the basic settings as you need them. Please have a look at the [features](/features/overview)