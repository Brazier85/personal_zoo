# Maintenance Mode in the App

Our app comes equipped with a convenient maintenance mode, accessible via the `/maintenance` route. This feature serves a critical purpose: it allows for manual modifications to the database when necessary.

## Purpose
In certain situations, you may encounter scenarios that demand manual intervention to alter the database. Hence, I have implemented this maintenance mode to enable direct changes within the app itself.

## Database Modifications
Within the maintenance mode, you have the capability to make adjustments to the database values. This functionality covers a range of operations, including updating, inserting, or deleting records.

### Tables
To facilitate these tasks, I provide access to the skeleton structures of the most vital tables. This ensures a smooth and secure process when making necessary changes to the database.

Should you have any specific inquiries or require assistance with utilizing the maintenance mode or implementing database changes, please don't hesitate to reach out to me.

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