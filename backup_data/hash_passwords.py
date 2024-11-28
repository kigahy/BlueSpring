# 유저 패스워드 해시처리하는 코드

import os
import django
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

# Django 설정을 초기화합니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youth.settings')
django.setup()

User = get_user_model()

def hash_user_passwords():
    users = User.objects.all()
    updated_count = 0

    for user in users:
        if not user.password.startswith('pbkdf2_'):
            user.password = make_password(user.password)
            user.save()
            updated_count += 1

    print(f'Successfully hashed passwords for {updated_count} user(s).')

if __name__ == '__main__':
    hash_user_passwords()
