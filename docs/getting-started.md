# Getting Started with Personal Zoo

## Hosting Simplified

Setting up Docker and hosting can be a bit challenging for less experienced users. If you'd prefer a hassle-free hosting solution for your Personal Zoo instance, we've got you covered!

Simply visit the following URL to order your Personal Zoo hosting today:

[Order Personal Zoo Hosting](https://buy.stripe.com/8wMeVm3ic7mB3OE8ww)

With our hosting service, you can focus on enjoying the benefits of Personal Zoo without the technical complexities of setting up and maintaining the infrastructure.

[read more](/hosting)

## Requirements
 
To run this application, there are two main methods: using Docker (recommended) or running it as a local Python app. Ensure that you have:

 - Docker 

or

- Python3

Please note that this application is not designed for public access due to the absence of authentication and authorization mechanisms. (See [security](/security))

### Quick Startup with Docker

To quickly set up Personal Zoo using Docker, follow these steps:

1. Create a new folder:
```bash
mkdir ~/personal_zoo
```

2. Move to the new folder:
```bash
cd ~/personal_zoo
```

3. Pull and run the `latest` image from Docker Hub:
```bash
docker run -d -p 5000:5000 -v ./data:/app/data --name personal_zoo brazier85/personal_zoo:latest
```

### Build It Yourself
If you prefer building the application from the source, follow these steps:

1. Clone the repository from GitHub:
    ``` bash
    cd ~
    git clone https://github.com/Brazier85/personal_zoo.git
    ```
2. Install Docker:<br>
    [See docker docs](https://docs.docker.com/get-docker/){:target="_blank"}
    ```bash
    # Download install script
    curl -fsSL https://get.Docker.com -o get-Docker.sh

    # Run script as root
    sudo sh get-Docker.sh

    # Add current user to docker group
    sudo usermod -aG docker $USER

    # Switch to group context
    newgrp docker
    ```
3. Run the `run_docker.sh` script:
    ``` bash
    cd personal_zoo
    sh run_docker.sh
    ```
4. Access the application by visiting `<host/ip>:5000`

### Manual installation
For running the application without Docker, follow these steps:

1. Install Python3 and necessary submodules.<br>
It is recommended to use a [virtual environment](https://docs.python.org/3/library/venv.html){:target="_blank"}..

``` bash
# install submodules
python3 -m pip install -r requirements.txt

# Run the app
python3 main.py
```

## Using the application

Once the application is successfully running, you can access the settings page to modify basic configurations as needed. For additional features, please refer to the [features overview](/features/overview)