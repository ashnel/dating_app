# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import datetime, date
import bcrypt
import re

emailregex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
nameregex = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if postData['formtype'] == 'register':
            user_data = User.objects.filter(email_address=postData['email_address'])
            if not user_data:
                 pass
            if len(postData['first_name']) < 1:
                errors['first_name'] = 'First name field cannot be empty.'
                return errors
            elif not nameregex.match(postData['first_name']):
                errors['first_name'] = 'First Name must be alphabetical characters only.'
                return errors
            elif len(postData['last_name']) < 1:
                errors['last_name'] = "Last name field cannot be empty."
                return errors
            elif not nameregex.match(postData['last_name']):
                errors['last_name'] = 'Last Name must be alphabetical characters only.'
                return errors
            if not 'gender' in postData:
                errors['gender'] = 'You must select a gender option.'
                return errors
            if not 'orientation' in postData:
                errors['orientation'] = 'You must select an orientation option.'
                return errors
            if postData['birthdate'] == '':
                errors['birthdate'] = 'You must enter a birthday.'
                return errors
            elif postData['birthdate'] != '':
                current_date = (datetime.now())
                birthday = datetime.strptime(postData['birthdate'], "%Y-%m-%d")
                days = current_date - birthday
                if days.days < 6570 and days.days > 0:
                    errors['birthdate'] = 'You must be 18 or older to sign up.'
                    return errors
                elif days.days < 0:
                    errors['birthdate'] = 'You cannot select a date that has not occured yet.'
                    return errors
            elif len(postData['email_address']) < 1:
                errors['email_address'] = 'Email field cannot be empty.'
                return errors
            if not emailregex.match(postData['email_address']):
                errors['email_address'] = 'Invalid email address.'
                return errors
            if len(postData['password']) == 0:
                errors['password'] = 'Password field cannot be empty.'
                return errors
            elif len(postData['password']) < 9:
                errors['password'] = 'Password must be more than 8 characters.'
                return errors
            elif len(postData['passwordcheck']) == 0:
                errors['password'] = 'Confirm passw ord field cannot be empty.'
                return errors
            elif len(postData['passwordcheck']) < 9:
                errors['password'] = 'Password must be more than 8 characters.'
                return errors
            elif postData['password'] != postData['passwordcheck']:
                errors['password'] = 'Password does not match password confirmation.'
                return errors
            if User.objects.filter(email_address=postData['email_address']):
                if postData['email_address'] == user_data[0].email_address:
                    errors['email_address'] = 'This email is already registered.'
                    return errors
            return errors
        elif postData['formtype'] == 'login':
            user_data = User.objects.filter(email_address=postData['email_address'])
            if not emailregex.match(postData['email_address']) and postData['email_address'] != '':
                errors['email_address'] = 'Invalid email address.'
                return errors
            elif not user_data or postData['email_address'] == '':
                 errors['email_address'] = 'Email field cannot be empty.'
                 return errors
            elif not user_data:
                errors['email_address'] = 'That email address does not exist.'
                return errors
            user_data = User.objects.get(email_address=postData['email_address'])
            password = bcrypt.checkpw(postData['password'].encode(), user_data.password.encode())
            if len(postData['password']) == 0:
                errors['password'] = 'Password field cannot be empty.'

            elif postData['email_address'] != user_data.email_address or password != True:
                errors['password'] = 'Your email and password do not match. Please try again.'
            return errors

class Location(models.Model):
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    orientation = models.CharField(max_length=255)
    birthdate = models.DateField()
    age = models.IntegerField()
    number = models.IntegerField()
    email_address = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    location = models.ForeignKey(Location, related_name='address') 
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Number(models.Model):
    pass

class Picture(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Rating(models.Model):
    rating_answer = models.BooleanField()
    users = models.ManyToManyField(User, related_name="ratings")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Match(models.Model):
    answer = models.BooleanField()
    user = models.ManyToManyField(User, related_name="matches")

class Chatroom(models.Model):
    users = models.ManyToManyField(User, related_name="chatrooms")
    updated_at = models.DateTimeField(auto_now = True)

class Message(models.Model):
    message = models.TextField()
    chatroom = models.ForeignKey(Chatroom, related_name='messages')
    user = models.ForeignKey(User, related_name='messages_sent')
    recipient = models.ForeignKey(User, related_name='messages_received')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)