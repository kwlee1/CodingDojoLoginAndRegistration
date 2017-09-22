# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt
import re 

errors = {}
chars = r'[a-zA-Z]{2,}'
chars = re.compile(chars)
email = r"^\w+@\w+\.[a-z]{3}"
email = re.compile(email)

class UserManager(models.Manager):
    def validator(self,postData):
        if chars.match(postData['fn']):
            errors['fn'] = ""
        else: 
            errors['fn'] = "First Name must be at least two characters and only contain letters"
        if chars.match(postData['ln']):
            errors['ln'] = ""
        else: 
            errors['ln'] = "Last Name must be at least two characters and only contain letters"
        if email.match(postData['email']):
            errors['email'] = ""
        else:
            errors['email'] = "Please enter a valid email address"
        if len(Users.objects.filter(email=postData['email'])) != 0:
            errors['email'] = "Email already in use"
        if len(postData['pw']) > 7:
            errors['pw'] = ""
        else: 
            errors['pw'] = "Password must be at least 8 characters"
        if postData['cpw'] == postData['pw']:
            errors['cpw'] = ""
        else:
            errors['cpw'] = "Password Confirmation must match Password "
        return errors

    def logincheck(self,postData):
        pw = Users.objects.filter(email=postData['email'])[0].password
        print pw 
        print bcrypt.checkpw(postData['pw'].encode(), pw.encode())
        if not email.match(postData['email']):
            errors['login'] = "Please enter a valid email address"
        elif len(Users.objects.filter(email=postData['email'])) == 0:
            errors['login'] = "Email not registered"
        elif not bcrypt.checkpw(postData['pw'].encode(), pw.encode()):
            errors['login'] = "Password incorrect"
        else:
            errors['login'] = ""
        return errors
        

class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()