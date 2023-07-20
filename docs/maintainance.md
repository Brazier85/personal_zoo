# Maintainance

There is a maintainance mode included into the app. You can visit it via `/maintainance`.

## Why?

In some cases it is required to do manual changes to the database. So I tought it would be nice to be able to do this changes direct in the app.

## Database changes

Here you can change values in the database.

### Tables

Here you can see the skeleton for the most important tables.

#### animal
```yaml
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
art TEXT,
morph TEXT,
gender TEXT,
birth DATE,
notes TEXT,
image TEXT,
background_color TEXT,
created_date DATE DEFAULT CURRENT_DATE,
updated_date DATE DEFAULT CURRENT_DATE
```

#### feeding
```yaml
id INTEGER PRIMARY KEY AUTOINCREMENT,
animal INT,
type TEXT,
count INT,
unit TEXT,
date DATE DEFAULT CURRENT_DATE
```

#### history
```yaml
id INTEGER PRIMARY KEY AUTOINCREMENT,
animal INT,
event TEXT,
text TEXT,
date DATE DEFAULT CURRENT_DATE
```