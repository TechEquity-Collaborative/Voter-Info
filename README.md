# Voter-Info
Find out who represents you now, and who else wants to.


## dev setup guide.

Install:

    # install pyenv, a tool for managing python versions, e.g. on mac with homebrew
    # (more info here: https://github.com/pyenv/pyenv)
    $ brew install pyenv
    $ brew install pyenv-virtualenv

    # Use pyenv to install the version of Python that you want (heroku runs on 3.6.4)
    $ pyenv install 3.6.4

    # Create a virtualenv for voter_info
    $ pyenv virtualenv 3.6.4 voter_info

    # Activate virtualenv
    $ pyenv activate voter_info

    # (Optional) Set this as default env for this directory so whenever you're in this dir, you use this virtualenv
    $ pyenv local voter_info

    # Confirm you are running the right python:
    $ which python
    # should be .../.pyenv/shims/python
    $ python --version
    # should be Python 3.6.4

    # Install requirements
    $ pip install -r requirements.txt



## Database:

1) Ensure you have Postgres 9.6 (or newer) installed locally

https://www.postgresql.org/download/

On MacOS Ben Mathes has found homebrew helpful, but the Postgres.app is another option for running postgres with postGIS


2) install the GIS extensions for postgres:

With homebrew for mac: https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/#homebrew
With Postgres.app: https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/#postgresapp


3) Create a database

    # Create a database provisioned to your user account
    $ createdb voter_info_dev

    # create the voter_info_dev database user and grant it permissions on the voter_info_dev DB:
    # connect to the voter_info_dev database in postgres:
    $ psql voter_info_dev
    # create your dev user with a password (only for dev, not used in production).
    # if you change the username or password from what is here, be sure to change the 'USER' and 'PASSWORD'
    # values in the DATABASES value in $git_root/voter_info/voter_info/settings.py
    $ create role voter_info_dev_user with login encrypted password 'super_sekrit_dev_pw_1234'
    # make sure your database user has access to the dev database:
    $ grant all on database voter_info_dev to voter_info_dev_user;

3) Check that django can connect to your dev database:

    $ python $git_root/voter_info/manage.py dbshell

4) Run all migrations to create your database schema:

    ####################IMPORTANT#################
    # THE FIRST TIME YOU MIGRATE, YOU MUST HAVE SUPERUSER PRIVLIGES
    # TO CREATE YOUR postGIS (geography stuff) EXTENSION:
    $ postgres> alter role voter_info_dev_user SUPERUSER;
    $ shel> python $git_root/voter_info/manage.py migrate
    $ postgres> alter role voter_info_dev_user NOSUPERUSER


# SET HEROKU CONFIG VARIABLE FOR SECRET KEY. STORE WHERE?

# PUSH TO HEROKU? HEROKU MASTER?

# HEROKU COMMAND LINE FOR TEC ACCOUNT, NOT PERSONAL

## Geospatial Database addons:

We use the Geospatial Data Abstraction Library (GDAL). GDAL requires a few extra libraries
you cannot install with pip.

https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/

With options for
https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/#homebrew



## deployment guide

install the heroku command line:
https://devcenter.heroku.com/articles/heroku-command-line
