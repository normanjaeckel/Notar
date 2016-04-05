=======
 Notar
=======

This project is still under development.

::

    $ python3 -m venv .virtualenv
    $ source .virtualenv/bin/activate
    $ pip install -U pip
    $ pip install -r requirements.txt
    $ npm install
    $ node_modules/.bin/bower install
    $ node_modules/.bin/gulp
    $ sed -i 's/DEBUG = False/DEBUG = True/' NotarDeploy/settings.py
    $ python manage.py migrate
    $ python manage.py createsuperuser
    $ python manage.py runserver
