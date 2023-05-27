### Setup

confirm that you have installed virtualenv globally as well. If not, run this:

    $ pip install virtualenv

Then, Git clone this repo to your PC

    $ git clone - ***url
    $ cd social_media_task

### Create a virtual environment

    $ virtualenv .venv && source .venv/bin/activate
Install dependancies

    $ pip install -r requirements.txt


### Create Log folder   
    $ mkdir Log

<!-- CREATE ROLE -->
    FOR CREATE THE ROLES RUN THE COMMAND BELOW,
        * python manage.py create_role


<!-- MAKING MIGRATION -->
    *python manage.py makemigrations 

    then,
    *python manage.py migrate

<!-- RUN THE PROJECT -->
    python manage.py runserver

