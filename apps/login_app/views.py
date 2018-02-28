# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from datetime import datetime, date
from .models import User, Number, Picture
import bcrypt

def homepage(request):
    if 'compat_arr' not in request.session:
        request.session['compat_arr'] = []
    else:
        request.session['compat_arr'] = []
    return render(request, 'login_app/homepage.html')

def dashboard(request):
    errors = User.objects.basic_validator(request.POST, request.FILES)
    if not 'formtype' in request.POST:
        pic = Picture.objects.get(user=request.session['id'])
        format 
        return render(request, 'dashboard_templates/dashboard.html', {'user': request.session['first_name'], 'pic': pic})
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
            user_info = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email_address=request.POST['email_address'], password=password, gender=request.POST['gender'], orientation=request.POST['orientation'], birthdate=request.POST['birthdate'], age=age, number=life_path_number)
            picture = Picture.objects.create(image=request.FILES['profile_pic'], user = user_info)
            request.session['first_name'] = user_info.first_name 
            errors['email'] = 'Thank you for registering. You may now login.'
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags='register')
            return redirect('/')
    elif request.POST['formtype'] == 'login':
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags='login')
            return redirect('/')
        else:
            user_info = User.objects.get(email_address=request.POST['email_address'])
            request.session['first_name'] = user_info.first_name 
            request.session['id'] = user_info.id
            request.session['number'] = user_info.number
            password = bcrypt.checkpw(request.POST['password'].encode(), user_info.password.encode())

            if request.POST['email_address'] == user_info.email_address and password == True:
                #return render(request, 'dashboard_templates/dashboard.html', {'user': request.session['first_name']})
                return redirect('/dashboard')
    return render(request, 'dashboard_templates/dashboard.html', {'user': request.session['first_name']})

def home(request):
    return render(request, 'dashboard_templates/dashboard.html', {'user': request.session['first_name']})

def settings(request):
    current_user = User.objects.get(id=request.session['id'])
    birthday = unicode(current_user.birthdate)
    return render(request, 'dashboard_templates/settings.html', {'first_name': current_user.first_name, 'last_name': current_user.last_name, 'birthdate': birthday, 'email_address': current_user.email_address, 'gender': current_user.gender, 'orientation': current_user.orientation})

def matches(request):
    # if len(request.session['compat_arr']) == 0:
    #      return HttpResponse('No Matches')
    # print 'matches route'
    # print request.session['compat_arr']
    #request.session['compat_arr'] = []
    current_user = User.objects.get(id=request.session['id'])
    numbers = Number.objects.filter(number=current_user.number)
    for x in numbers:
        compats = User.objects.filter(number=x.good)
        for i in compats:
            if i.id != request.session['id']:
                request.session['compat_arr'].append(i.id)
                request.session.modified = True
                print request.session['compat_arr']
    return render(request, 'dashboard_templates/matches.html', {'match_name':User.objects.get(id=request.session['compat_arr'][0]).first_name, 'match_age':User.objects.get(id=request.session['compat_arr'][0]).age})
    #return render(request, 'dashboard_templates/matches.html')

def vote(request):
    if len(request.session['compat_arr']):
        if request.POST['formtype'] == 'match':
            print len(request.session['compat_arr'])
            print 'if'
            del request.session['compat_arr'][0]
            if len(request.session['compat_arr']) == 0:
                return redirect('/dashboard')
            else:
                print len(request.session['compat_arr'])
                #print request.session['compat_arr']
                request.session.modified = True
                #return render(request, 'dashboard_templates/matches.html')
                return render(request, 'dashboard_templates/matches.html', {'match_name':User.objects.get(id=request.session['compat_arr'][0]).first_name, 'match_age':User.objects.get(id=request.session['compat_arr'][0]).age})
        elif request.POST['formtype'] == 'no':
            print 'no' 
            return redirect('/dashboard')  
    else:
        print 'else'
        return redirect('/dashboard')
            #return render(request, 'dashboard_templates/matches.html')
            #return render(request, 'dashboard_templates/matches.html', {'match_name':User.objects.get(id=request.session['compat_arr'][0]).first_name, 'match_age':User.objects.get(id=request.session['compat_arr'][0]).age})

def new_match(request):
    #print 'newmatch route'
    #print request.session['compat_arr']
    return render(request, 'dashboard_templates/matches.html', {'match_name':User.objects.get(id=request.session['compat_arr'][0]).first_name, 'match_age':User.objects.get(id=request.session['compat_arr'][0]).age})

def update(request):
    errors = User.objects.basic_validator(request.POST)
    updated_user = User.objects.get(id=request.session['id'])
    if request.POST['password'] == '':
        updated_user.first_name = request.POST['first_name']
        updated_user.last_name = request.POST['last_name']
        updated_user.gender = request.POST['gender']
        updated_user.orientation = request.POST['orientation']
        updated_user.birthdate = request.POST['birthdate']
        updated_user.email_address = request.POST['email_address']
        updated_user.save()
        request.session['first_name'] = updated_user.first_name
    else:
        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags='update')
        else:
            updated_user.first_name = request.POST['first_name']
            updated_user.last_name = request.POST['last_name']
            updated_user.gender = request.POST['gender']
            updated_user.orientation = request.POST['orientation']
            updated_user.birthdate = request.POST['birthdate']
            updated_user.email_address = request.POST['email_address']
            updated_user.password = password
            updated_user.save()
            request.session['first_name'] = updated_user.first_name
    return redirect('/settings')

def logout(request):
    request.session.flush()
    return redirect('/')