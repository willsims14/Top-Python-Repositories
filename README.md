# Top Python Repositories
#### Will Sims
###### 12/19/2019


## Clone Repo
```
git clone https://github.com/willsims14/Top-Python-Repositories.git
cd Top-Python-Repositories/
```


## Prerequisites

Install Required Packages:
* Django == 3.0.1
* inflection == 0.3.1
* requests == 2.22.0

```
pip install -r requirements.txt
```



## Usage
1) Once the repository is cloned and the required packages are installed, migrate the provided migrations to initialize a the database:

```
python manage.py migrate
```
> Notice the `db.sqlite3` file that was created to act as our database

2) Now that the database is initialized and ready to house data, we can populate it with data (most-starred public Python repositories):

```
python manage.py populate
```

3) Start your server and browse away!

```
python manage.py runserver
```

Using your favorite internet browser navigate to http://localhost:8000/