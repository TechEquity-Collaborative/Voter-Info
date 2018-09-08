release: python ./voter_info/manage.py migrate
web: sh -c 'cd ./voter_info/ && exec gunicorn voter_info.wsgi:application --log-file -'