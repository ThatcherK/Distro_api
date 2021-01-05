![distro_api Actions status](https://github.com/ThatcherK/Distro_api/workflows/distro_api/badge.svg)

An API for the distroIQ  web app


## Technologies

1. Python 3.8
2. Postgresql
3. Flask 1.1.2

## Setup 

### Create a virtual environment 

`python3 -m venv env`

### Activate the virtual environment
 
For macOS/Linux

`source env/bin/activate`

For windows

`env\Scripts\activate`

### Install dependencies

`pip3 install -r requirements.txt`

### Get environment variables
You will need to set the following environment variables inorder to run the application
```
SECRET_KEY
DATABASE_URL
TEST_DATABASE_URL
SENDGRID_API_KEY
SENDGRID_SENDER_MAIL
```
### Create and seed the database
These should be run the first time the application is run
`python3 manage.py recreate_db`
`python3 manage.py seed_db`

### Run the app 

`python3 manage.py run`

### Run the tests

`pytest`