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
     .../.pyenv/shims/python

    $ python --version
    Python 3.6.4

    # Install requirements
    $ pip install -r requirements.txt



## Database:

#### Ensure you have Postgres 10.3 installed locally. Heroku defaults to 10.3

https://www.postgresql.org/download/

    # If you installed postgres with homebrew, make sure you start your local postgres server:
    # brew services start postgresql

On MacOS Ben Mathes has found homebrew helpful, but the Postgres.app is another option for running postgres with postGIS support.


#### install the GIS extensions for postgres:

We use the Geospatial Data Abstraction Library (GDAL). GDAL requires a few extra libraries
you cannot install with pip.

https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/

With homebrew for mac: https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/#homebrew
With Postgres.app: https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/#postgresapp


#### Create a database

    # Create a database provisioned to your user account
    $ createdb voter_info_dev

    # create the voter_info_dev database user and grant it permissions on the voter_info_dev DB:
    # connect to the voter_info_dev database in postgres:
    $ psql voter_info_dev

    # create your dev user with a password (only for dev, not used in production).
    # if you change the username or password from what is here, be sure to change the 'USER' and 'PASSWORD'
    # values in the DATABASES value in $git_root/voter_info/voter_info/settings.py
    $ psql> create role voter_info_dev_user with login encrypted password 'super_sekrit_dev_pw_1234';

    # make sure your database user has access to the dev database:
    $ psql> grant all on database voter_info_dev to voter_info_dev_user;

#### Check that django can connect to your dev database:

    $ python $git_root/voter_info/manage.py dbshell

#### Run all migrations to create your database schema:

    ####################IMPORTANT#################
    # THE FIRST TIME YOU MIGRATE, YOU MUST HAVE SUPERUSER PRIVLIGES
    # TO CREATE YOUR postGIS (geography stuff) EXTENSION:
    $ postgres> alter role voter_info_dev_user SUPERUSER;
    $ shell> python $git_root/voter_info/manage.py migrate
    $ postgres> alter role voter_info_dev_user NOSUPERUSER;

### Setup the frontend and it's depenencies:

    # We'll use yarn for package management
    # the yarn installer will also install node if
    # it doesn't find it.
    $ brew install yarn

    # You will probably want a node version manager if you don't already have one.
    # @ericsandine recommends `n`
    $ npm install -g n

    # Then install the production version of Node
    # This command will install it and switch to the version
    # You can swap versions by using `n` if needed
    $ n 9.5.0

    # Now install the current dependencies
    $ yarn install

    # To install a new package use
    $ yarn add <some-some-awesome-package>

## Run your local dev server

    # Since this is a Procfile based app we'll use Foreman
    # to manage processes
    # https://github.com/ddollar/foreman

    # Check to see if you have a version of ruby installed
    # if you do, skip to installing the gem
    # You may also want to install RVM anyway.
    $ ruby -v

    # Install RVM and Ruby
    # This will install RVM (a Ruby version manager)
    # and the current stable version of Ruby
    # https://rvm.io/rvm/install
    $ \curl -sSL https://get.rvm.io | bash -s stable --ruby

    # Install the foreman Gem
    $ gem install foreman

    # To run your dev server use
    $ foreman run -f $git_root/Procfile.local
    ...
    Starting development server at http://127.0.0.1:8000/


now open http://127.0.0.1:8000/ And you should see a web page.



## Deployment Guide

    # Before deploying, if you've made any front end changes
    # make sure you build the react app.
    $ cd $git_root/voter_info/frontend && yarn build

# SET HEROKU CONFIG VARIABLE FOR SECRET KEY. STORE WHERE?

# PUSH TO HEROKU? HEROKU MASTER?

# HEROKU COMMAND LINE FOR TEC ACCOUNT, NOT PERSONAL

install the heroku command line:
https://devcenter.heroku.com/articles/heroku-command-line
