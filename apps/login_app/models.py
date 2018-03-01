# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import datetime, date
import bcrypt
import re

emailregex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
nameregex = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData, fileData):
        errors = {}
        if not 'formtype' in postData: 
            return False
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
                errors['password'] = 'Confirm password field cannot be empty.'
                return errors
            elif len(postData['passwordcheck']) < 9:
                errors['password'] = 'Confirmed password must be more than 8 characters.'
                return errors
            elif postData['password'] != postData['passwordcheck']:
                errors['password'] = 'Password does not match password confirmation.'
                return errors
            if not 'profile_pic' in fileData:
                errors['image'] = "Please upload a profile picture."
            if len(postData['city']) == 0:
                errors['city'] = "Please enter a valid city."
            if len(postData['state']) == 0:
                errors['state'] = "Please enter a valid state."
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
            elif not user_data and postData['email_address'] == '':
                 errors['email_address'] = 'Email field cannot be empty.'
                 return errors
            elif not user_data:
                errors['email_address'] = 'That email address does not exist.'
                return errors
            user_data = User.objects.get(email_address=postData['email_address'])
            password = bcrypt.checkpw(postData['password'].encode(), user_data.password.encode())
            if len(postData['password']) <= 0:
                errors['password'] = 'Password field cannot be empty.'
                return errors
            elif postData['email_address'] != user_data.email_address or password != True:
                errors['password'] = 'Your email and password do not match. Please try again.'
                return errors
        elif postData['formtype'] == 'update':
            if len(postData['password']) < 9:
                errors['password'] = 'Password must be more than 8 characters.'
            elif len(postData['passwordcheck']) < 9:
                errors['password'] = 'Confirmed password must be more than 8 characters.'
                return errors
            elif postData['password'] != postData['passwordcheck']:
                errors['password'] = 'Password does not match password confirmation.'
                return errors
        return errors


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
    #location = models.ForeignKey(Location, related_name='address') 
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Location(models.Model):
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    user = models.ForeignKey(User, related_name="location")
    
class Number(models.Model):
    number = models.IntegerField()
    good = models.IntegerField()
    bad = models.IntegerField()

class Picture(models.Model):
    image = models.FileField(upload_to='profile', null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User, related_name='pictures', null=True)

class Rating(models.Model):
    rating_answer = models.BooleanField()
    users = models.ManyToManyField(User, related_name="ratings")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Match(models.Model):
    answer = models.BooleanField()
    user = models.ForeignKey(User, related_name="users")
    matched_user = models.ForeignKey(User, related_name="matches")

class Chatroom(models.Model):
    label = models.SlugField(unique=True)
    users = models.ManyToManyField(User, related_name="chatrooms")
    updated_at = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return self.label

class Message(models.Model):
    message = models.TextField()
    chatroom = models.ForeignKey(Chatroom, related_name='messages')
    handle = models.TextField()
    #No longer needed. All messages will be contained in a chat room, and the chatroom will remember the users belonging to it
    # user = models.ForeignKey(User, related_name='messages_sent')
    # recipient = models.ForeignKey(User, related_name='messages_received')
    created_at = models.DateTimeField(auto_now_add = True)
    #We won't be updating sent messages
    # updated_at = models.DateTimeField(auto_now = True)
    def __unicode__(self):
        return '[{created_at}] {handle}: {message}'.format(**self.as_dict())

    @property
    def formatted_created_at(self):
        return self.created_at.strftime('%b %d %I:%M %p')
    def as_dict(self):
        return {'handle': self.handle, 'message': self.message, 'created_at': self.formatted_created_at}