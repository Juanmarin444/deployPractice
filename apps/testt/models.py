from __future__ import unicode_literals
from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postdata):
        errors = {}
        if len(postdata['first_name']) < 3:
            errors['first_name'] = 'First Name is not long enough.'
        if len(postdata['last_name']) < 3:
            errors['last_name'] = 'Last Name in not long enough.'
        if postdata['password'] != postdata['conf_pass']:
            errors['password'] = 'Password confirmation does NOT match.'
        if len(postdata['email']) < 1:
            errors['email'] = 'Email cannot be Blank.'
        elif not EMAIL_REGEX.match(postdata['email']):
            errors['email'] = 'Invalid Email Address!'
        if len(postdata['password']) < 8:
            errors['password'] = 'Password needs to be at least 8 Characters long.'
        print(postdata['first_name'])
        print(postdata['last_name'])
        print(postdata['email'])
        print(postdata['password'])
        return errors

    def login_validator(self, postdata):
        errors = {}
        email = postdata['email']
        print(postdata['email'])
        print(postdata['password'])
        logged_user = User.objects.filter(email = email)

        if logged_user:
            if bcrypt.checkpw(postdata['password'].encode(), logged_user[0].password.encode()):
                errors['user'] = logged_user[0]
            else:
                errors['notmatch'] = 'Email does not match User.'
        else:
            errors['usernotmatch'] = 'Password and email do not match.'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 254)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
