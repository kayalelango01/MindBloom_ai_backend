#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py shell -c "
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

if not User.objects.filter(username='demo').exists():
    user = User.objects.create_user(username='demo', password='demo1234', email='demo@mindbloom.com')
    Token.objects.get_or_create(user=user)
    print('Demo user created!')
else:
    print('Demo user already exists.')
"