# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from ..login_app.models import *
from django.db.models import Q
import string, random

# # Create your views here.
# def dashboard(request):
#     if 'id' in request.session:
#         user =  user.objects.get(id=request.session['id'])
#         context = {
#             'user': user,
#             'friends': User.objects.get(id=request.session['id']).friends,
#             'pic': Picture.objects.get(user=request.session['id'])
#         }
#         pic = user.pictures.all()
#         print "Please Work!!!"
#         result = render(request, 'dashboard_templates/dashboard.html', context)
#     else:
#         result = redirect ('/login')
#     return result

def chat(request):
    print "Chat*******************"
    if 'id' in request.session:
        print 'if'
        friend_id = request.POST['friend']
        room = Chatroom.objects.filter(users=User.objects.get(id=request.session['id'])).filter(users=User.objects.get(id=friend_id))
        if len(room)==0:
            new_room = None
            while not new_room:
                label = "".join([random.choice(string.ascii_letters + string.digits) for n in xrange(6)])
                if len(Chatroom.objects.filter(label=label))==0:
                    new_room = Chatroom.objects.create(label=label)
                    new_room.users.add(User.objects.get(id=request.session['id']))
                    new_room.users.add(User.objects.get(id=friend_id))
            room = new_room
        result = redirect('/dashboard/chat/{}/'.format(room[0].label))
    else:
        print 'else'
        result = redirect('/login')
    return result
def chat_room(request, label):
    print "ChatRoom*************************"
    if 'id' in request.session:
        if  len(Chatroom.objects.filter(label=label))==0:
            result = redirect('/dashboard')
        else:
            room = Chatroom.objects.get(label=label)
            if room.users.filter(id=request.session['id']) > 0:
                messages = reversed(room.messages.order_by('-created_at')[:50])
                result = render(request, "dashboard_templates/chatroom.html", {'room':room, 'messages':messages, 'user':User.objects.get(id=request.session['id'])})
            else:
                result =redirect('/dashboard')
    else:
        result = redirect('../')
    return result
    # return HttpResponse({'success':True, 'messages':messages})


# def chat_room(request, label): #For testing only
#     if  len(Chatroom.objects.filter(label=label))==0:
#         new_room = None
#         while not new_room:
#             label = "".join([random.choice(string.ascii_letters + string.digits) for n in xrange(6)])
#             if len(Chatroom.objects.filter(label=label))==0:
#                 new_room = Chatroom.objects.create(label=label)
#         room = new_room
#         messages = {}
#         result = render(request, "dashboard_templates/chatroom.html", {'room':room, 'messages':messages, 'user':User.objects.get(id=request.session['id'])})
#     else: 
#         room = Chatroom.objects.get(label=label)
#         messages = reversed(room.messages.order_by('-created_at')[:50])
#         result = render(request, "dashboard_templates/chatroom.html", {'room':room, 'messages':messages, 'user':User.objects.get(id=request.session['id'])})
#     return result
