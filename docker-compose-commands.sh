#!/usr/bin/env bash

while true; do
    read -p "Do you want to rebuild?: " yn
    case $yn in
        [Yy]* ) docker-compose build; break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

docker-compose run --rm web python manage.py migrate
docker-compose run --rm web python manage.py test

while true; do
    read -p "Do you want to create superuser for project?: " yn
    case $yn in
        [Yy]* ) docker-compose run web python manage.py createsuperuser; break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

docker-compose up
