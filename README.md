# Personal Zoo

## Purpose

This webapp is for managing my "personal zoo" @home. You can add animals, there feedings, ect...

Currently the app is still under development and not stable.

### **The app is NOT production ready!**

## Custom Types
You can set your custom settings by editing the `data/custom_settings.py` file!
```python
# Custom feeding types
FEEDING_TYPES = ["Elefant",'Heuschrecke',"Kleinkind","Maus","Ratte","Wal"]

# Custom events
EVENT_TYPES = ["Häutung","Gewogen","Medizinisch","Sonstiges"]
```

**WARNING**: You must restart the app after this changes!


## Docker 
```bash
docker build -t personal_zoo .

docker run -d -p 5000:5000 -v ./data:/app/data --name personal_zoo personal_zoo

# For dev
docker run -d -p 5000:5000 -v .:/app --name personal_zoo personal_zoo
```

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

# deactivate venv
deactivate

```
