# Personal Zoo

## Startup
```bash
python3 -m pip install -r requirements.txt
```

## Docker 
```bash
docker build -t personal_zoo .

docker run -d -p 5000:5000 -v ./data:/app/data --name personal_zoo personal_zoo

# For dev
docker run -d -p 5000:5000 -v .:/app --name personal_zoo personal_zoo
```

## Development
```bash

#create venv
python3 -m venv venv

#activate venv
source venv/bin/activate

# install packages
pip install flask

# create requirements.txt
pip freeze > requirements.txt

# deactivate venv
deactivate

```
