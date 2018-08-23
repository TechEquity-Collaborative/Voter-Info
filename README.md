# Voter-Info
Find out who represents you now, and who else wants to.


## dev setup guide.

Install:

    # install pyenv, a tool for managing python versions, e.g. on mac with homebrew
    # (more info here: https://github.com/pyenv/pyenv)
    $ shell> brew install pyenv
    $ shell> brew install pyenv-virtualenv

    # Use pyenv to install the version of Python that you want (heroku runs on 3.6.4)
    $ shell> pyenv install 3.6.4

    # Create a virtualenv for voter_info
    $ shell> pyenv virtualenv 3.6.4 voter_info

    # Activate virtualenv
    $ shell> pyenv activate voter_info

    # (Optional) Set this as default env for this directory so whenever you're in this dir, you use this virtualenv
    $ shell> pyenv local voter_info

    # Confirm you are running the right python:
    $ shell> which python
     .../.pyenv/shims/python

    $ shell> python --version
    Python 3.6.4

    # Install requirements
    $ shell> pip install -r requirements.txt



## Database:

#### Ensure you have Postgres 10.3 installed locally. Heroku defaults to 10.3

https://www.postgresql.org/download/

    # e.g. to install with homebrew on macos
    $ shell> brew install postgresql

    # If you installed postgres with homebrew, make sure you start your local postgres server:
    $ bash> brew services start postgresql

On MacOS Ben Mathes has found homebrew helpful, but the Postgres.app is another option for running postgres with postGIS support.


#### install the GIS extensions for postgres:

We use the Geospatial Data Abstraction Library (GDAL). GDAL requires a few extra libraries
you cannot install with pip.

https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/

With homebrew for mac: https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/#homebrew

With Postgres.app: https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/#postgresapp

E.g. with homebrew:

    $ brew install postgis
    $ brew install gdal
    $ brew install libgeoip


#### Create a database

    # Create a database provisioned to your user account
    $ shell> createdb voter_info_dev

    # create the voter_info_dev database user and grant it permissions on the voter_info_dev DB:
    # connect to the voter_info_dev database in postgres:
    $ shell> psql voter_info_dev

    # create your dev user with a password (only for dev, not used in production).
    # if you change the username or password from what is here, be sure to change the 'USER' and 'PASSWORD'
    # values in the DATABASES value in $git_root/voter_info/voter_info/settings.py
    $ psql> create role voter_info_dev_user with login encrypted password 'super_sekrit_dev_pw_1234';

    # make sure your database user has access to the dev database:
    $ psql> grant all on database voter_info_dev to voter_info_dev_user;

#### Check that django can connect to your dev database:

    $ shell> python $git_root/voter_info/manage.py dbshell

#### Run all migrations to create your database schema:

    ####################IMPORTANT#################
    # THE FIRST TIME YOU MIGRATE, YOU MUST HAVE SUPERUSER PRIVLIGES
    # TO CREATE YOUR postGIS (geography stuff) EXTENSION:
    $ postgres> alter role voter_info_dev_user SUPERUSER;
    $ shell> python $git_root/voter_info/manage.py migrate
    $ postgres> alter role voter_info_dev_user NOSUPERUSER;

#### Import Shapefiles to the Postgres Database

    # run the custom manage.py command:
    & shell> python $git_root/voter_info/manage.py import_shapefiles

## Frontend:

    # We'll use yarn for package management. The yarn installer will also install node if
    # it doesn't find it.
    $ brew install yarn

    # You will probably want a node version manager if you don't already have one.
    # @ericsandine recommends `n`
    $ npm install -g n

    # Then install the production version of Node
    # This command will install it and switch to the version
    # You can swap versions by using `n` if needed
    $ n 10.9.0

    # Now install the current dependencies
    $ yarn install

    # To install a new package use
    $ yarn add <some-some-awesome-package>

## Run your local dev server

    # don't forget to have the heroku CLI installed
    $ shell> npm install -g heroku

    # To run your dev server use heroku, which is compatible with procfiles
    # (recall that a procfile is basically a list of commands to run)
    $ heroku local -f $git_root/Procfile.local


Django will run on http://127.0.0.1:8000/
The react dev server will run on http://127.0.0.1:5000/ (or the next open port) and proxy requests to Django



## Pull Requests and Heroku Builds.


Every time you create a PR, heroku will kick off a build to see if it can create
a server running the version of your PR. You can see the builds here:

https://dashboard.heroku.com/pipelines/514a9ea9-75d3-4056-81cc-24b8aebd5592



## Deployment Guide

install the heroku command line:
https://devcenter.heroku.com/articles/heroku-command-line

    # don't forget to have the heroku CLI installed
    $ shell> npm install -g heroku

Then follow the guide to get started: https://devcenter.heroku.com/articles/heroku-cli#getting-started

    $ shell> heroku login

    # confirm your login is part of the TEC:
    $ shell> heroku teams
    techequity
    $ shell> heroku apps --team techequity
    === Apps in team techequity
    voter-info
    voter-info-pr-15
    ...


The Heroku CLI defaults to your personal account and requires the --team flag when
performing team actions. If you generally work under an organization, you can set
the HEROKU_ORGANIZATION environment variable in order to default to that organization.

    $ bash> export HEROKU_ORGANIZATION=techequity
    $ bash> heroku apps
    === Apps in team techequity
    voter-info
    voter-info-pr-15
    ...
