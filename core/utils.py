from django.contrib.auth.models import User


data = {
    'username': 'dang',
    'email': 'dang@da.c',
    'password': '123',
    'password2': '123',
}


def check_error_accout(username, email, password, password2):
    errors = {}
    if User.objects.filter(username=username).exists():
        errors['username'] = "Username Taken"
    if User.objects.filter(email=email).exists():
        errors['email'] = "Email Taken"
    if password != password2:
        errors['password'] = "Password not matching"

    return errors


