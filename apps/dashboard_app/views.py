# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from apps.login_app.models import User, Message, Picture
from django.db.models import Q

# Create your views here.
def dashboard(request):
    if 'id' in request.session:
        user =  user.objects.get(id=request.session['id'])
        context = {
            'user': user,
            'friends': User.objects.get(id=request.session['id']).friends,
            'pic': Picture.objects.get(user=request.session['id'])
        }
        pic = user.pictures.all()
        print "Please Work!!!"
        result = render(request, 'dashboard_templates/dashboard.html', context)
    else:
        result = redirect ('/login')
    return result

def get_messages(request):
    if request.is_ajax():
        friend_id = request.POST('id')
        messages = Message.objects.filter((Q(sender_id=request.session['id']) | Q(reciever_id=request.session['id'])) & (Q(sender_id=friend_id]) | Q(reciever_id=friend_id))).order_by('-created_on')[:5]
        response = {
            'success': True,
            'messages' : messages
        }

    return HttpResponse(simplejson.dumps(response))