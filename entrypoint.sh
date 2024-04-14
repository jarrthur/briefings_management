#!/bin/bash

set -e

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Confirming and loading initial Categories..."
python manage.py create_initial_categories

echo "Checking if superuser exists..."
SUPERUSER_EXISTS=$(python manage.py shell -c "from django.contrib.auth import get_user_model; print(get_user_model().objects.filter(username='admin').exists())")

if [ "$SUPERUSER_EXISTS" = "True" ]; then
    echo "Superuser already exists."
else
    echo "Creating superuser:"
    echo "Username: admin"
    echo "Password: admin"
    python manage.py createsuperuser --noinput
fi

echo "Starting the web server..."
exec "$@"
