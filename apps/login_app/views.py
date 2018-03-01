# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from datetime import datetime, date
from .models import User, Number, Picture, Match, Location
import bcrypt

def homepage(request):
    if 'compat_arr' not in request.session:
        request.session['compat_arr'] = []
    if 'friends' not in request.session:
        request.session['friends'] = []
    else:
        request.session['friends'] = []
    return render(request, 'login_app/homepage.html')

def dashboard(request):
    errors = User.objects.basic_validator(request.POST, request.FILES)
    if not 'formtype' in request.POST:
        pic = Picture.objects.get(user=request.session['id'])
        friends_array = []
        current_user = request.session['id']
        user = Match.objects.filter(user=current_user)
        matched = Match.objects.filter(matched_user=current_user)
        for m in matched:
            matchee = m.user
            if m.answer == True:
                for u in user:
                    if u.matched_user == matchee:
                        if u.answer == True and m.answer == True:
                            friends_array.append(m.user)
        friends = friends_array
        print friends
        context = {
             'pic': pic,
             'user': request.session['first_name'],
             'all_friends': friends
        }
        # for u in user:
        #     if u.matched_user == u.user:
        #         if u.answer == True:
        #             friends_array.append(u)
        # friends = friends_array
        # context = {
        #     'pic': pic,
        #     'user': request.session['first_name'],
        #     'all_friends': friends
        # }
        return render(request, 'dashboard_templates/dashboard.html', context)
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
            location = Location.objects.create(city=request.POST['city'], state=request.POST['state'], user=user_info)
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
                pic = Picture.objects.get(user=request.session['id'])
                friends_array = []
                current_user = request.session['id']
                user = Match.objects.filter(user=current_user)
                matched = Match.objects.filter(matched_user=current_user)
                for u in user:
                    if u.matched_user == u.user:
                        if u.answer == True:
                            friends_array.append(u)
                friends = friends_array
                context = {
                    'pic': pic,
                    'user': request.session['first_name'],
                    'all_friends': friends
                }
                return render(request, 'dashboard_templates/dashboard.html', context)
    return render(request, 'dashboard_templates/dashboard.html', {'user': request.session['first_name']})

def home(request):
    return render(request, 'dashboard_templates/dashboard.html', {'user': request.session['first_name'], 'all_frieds': friends})

def settings(request):
    current_user = User.objects.get(id=request.session['id'])
    birthday = unicode(current_user.birthdate)
    return render(request, 'dashboard_templates/settings.html', {'first_name': current_user.first_name, 'last_name': current_user.last_name, 'birthdate': birthday, 'email_address': current_user.email_address, 'gender': current_user.gender, 'orientation': current_user.orientation})

def matches(request):
    
    current_user = User.objects.get(id=request.session['id'])
    numbers = Number.objects.filter(number=current_user.number)
    for x in numbers:
        compats = User.objects.filter(number=x.good)
        for i in compats:
            matches = Match.objects.filter(matched_user=i.id).filter(user=current_user.id)
            if len(matches) == 1:
                if i.id != matches[0].matched_user.id:
                    continue
            else:
                if i.id != request.session['id']:
                    request.session['compat_arr'].append(i.id)
                    request.session.modified = True
    if request.session['compat_arr'] == []:
        return redirect('/dashboard')
    return render(request, 'dashboard_templates/matches.html', {'match_name':User.objects.get(id=request.session['compat_arr'][0]).first_name, 'match_age':User.objects.get(id=request.session['compat_arr'][0]).age})

def vote(request):
    print request.session['compat_arr']
    matched_user_person = request.session['compat_arr'][0]
    current_user = User.objects.get(id=request.session['id'])
    if len(request.session['compat_arr']):
        if request.POST['formtype'] == 'match':
            Match.objects.create(answer=True, user=current_user, matched_user=User.objects.get(id=matched_user_person))
            del request.session['compat_arr'][0]
            if len(request.session['compat_arr']) == 0:
                request.session.modified = True
                return redirect('/dashboard')
            else:
                request.session.modified = True
                return render(request, 'dashboard_templates/matches.html', {'match_name':User.objects.get(id=request.session['compat_arr'][0]).first_name, 'match_age':User.objects.get(id=request.session['compat_arr'][0]).age})
        elif request.POST['formtype'] == 'no':
            Match.objects.create(answer=False, user=current_user, matched_user=User.objects.get(id=matched_user_person))
            del request.session['compat_arr'][0]
            if len(request.session['compat_arr']) == 0:
                request.session.modified = True
                return redirect('/dashboard')
            else:
                request.session.modified = True
                return render(request, 'dashboard_templates/matches.html', {'match_name':User.objects.get(id=request.session['compat_arr'][0]).first_name, 'match_age':User.objects.get(id=request.session['compat_arr'][0]).age})
    else:
        print 'else'
        return redirect('/dashboard')

def new_match(request):
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