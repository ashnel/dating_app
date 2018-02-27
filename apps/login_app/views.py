# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from datetime import datetime, date
from .models import User
import bcrypt

def homepage(request):
    return render(request, 'login_app/homepage.html')

def personal_profile(request):
    errors = User.objects.basic_validator(request.POST)
    if request.POST['formtype'] == 'register':
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags='register')
            return redirect('/')
        else:
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            current_date = (datetime.now())
            birthday = datetime.strptime(request.POST['birthdate'], "%Y-%m-%d")
            days = current_date - birthday
            age = round(days.days / 365) 
            added_date = birthday.day + birthday.month + birthday.year
            added_date_string = str(added_date)
            life_path_number = 0
            for x in added_date_string:
                life_path_number += int(x)
            if life_path_number > 9:
                number_str = str(life_path_number)
                life_path_number = 0
                for x in number_str:
                    life_path_number += int(x)
            User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email_address=request.POST['email_address'], password=password, gender=request.POST['gender'], orientation=request.POST['orientation'], birthdate=request.POST['birthdate'], age=age, number=life_path_number)
            user_info = User.objects.get(email_address=request.POST['email_address'])
            request.session['first_name'] = user_info.first_name 
    elif request.POST['formtype'] == 'login':
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags='login')
            return redirect('/')
        else:
            user_info = User.objects.get(email_address=request.POST['email_address'])
            request.session['first_name'] = user_info.first_name 
            request.session['id'] = user_info.id
            password = bcrypt.checkpw(request.POST['password'].encode(), user_info.password.encode())
            if request.POST['email_address'] == user_info.email_address and password == True:
                return render(request, 'login_app/personal_profile.html')
    return render(request, 'login_app/personal_profile.html')