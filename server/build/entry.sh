#!/bin/bash

until nc -z mastermind-postgresql 5432; do
    echo "$(date) - waiting for postgresql..."
    sleep 1
done

echo "sleep for 5 more seconds for postgresql...";
sleep 5;

>&2 echo "Postgresql is ready - executing command":

#cd /opt/src && python3 manage.py makemigrations
cd /opt/src && python3 manage.py migrate

cd /opt/src && python3 manage.py runserver 0.0.0.0:8000
