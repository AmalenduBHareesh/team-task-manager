# Team Task Manager

## Setup

### Create Virtual Environment
python -m venv venv

### Activate
venv\Scripts\activate

### Install Dependencies
pip install -r requirements.txt

### Run Migrations
python manage.py makemigrations
python manage.py migrate

### Create Superuser
python manage.py createsuperuser

### Run Server
python manage.py runserver