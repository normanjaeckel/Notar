=======
 Notar
=======

This project is still under development.

::

    $ python -m venv .virtualenv
    $ source .virtualenv/bin/activate
    $ pip install -U pip
    $ pip install -r requirements.txt
    $ npm install
    $ export PATH="/path/to/project/node_modules/.bin:$PATH"
    $ bower install
    $ gulp
    $ sed -i 's/DEBUG = False/DEBUG = True/' NotarDeploy/settings.py
    $ python manage.py migrate
    $ python manage.py createsuperuser
    $ python manage.py runserver
