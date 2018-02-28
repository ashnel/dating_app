# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from ..login_app.models import *
from django.db.models import Q
import string, random


# Create your views here.
def dashboard(request):
    if 'id' in request.session:
        context = {
            'user': User.objects.get(id=request.session['id']),
            'friends': User.objects.get(id=request.session['id']).friends
        }

        result = render(request, 'dashboard_templates/dashboard.html', context)
    else:
        result = redirect ('/login')
    return result

# def get_messages(request):
#     if request.is_ajax():
#         friend_id = request.POST('id')
#         messages = Message.objects.filter((Q(sender_id=request.session['id']) | Q(reciever_id=request.session['id'])) & (Q(sender_id=friend_id]) | Q(reciever_id=friend_id))).order_by('-created_on')[:5]
#         response = {
#             'success': True,
#             'messages' : messages
#         }

#     return HttpResponse(simplejson.dumps(response))
def chat(request):
    if 'id' in request.session:
        friend_id = request.POST['friend']
        room = Chatroom.objects.filter(users=User.objects.get(id=request.session['id'])).filter(users=User.objects.get(id=friend_id))
        if len(room)==0:
            new_room = None
            while not new_room:
                label = "".join([random.choice(string.ascii_letters + string.digits) for n in xrange(6)])
                if len(Chatroom.objects.filter(label=label))==0:
                    new_room = Chatroom.objects.create(label=label)
            room = new_room
        result = redirect('chat/{}'.format(room.label))
    else:
        result = redirect('/login')
    return result
def chat_room(request, label):
    if  len(Chatroom.objects.filter(label=label))==0:
        result = redirect('/login')
    else: 
        room = Chatroom.objects.get(label=label)
        messages = reversed(room.messages.order_by('-created_on')[:50])
        result = render(request, "chatroom.html", {'room':room, 'messages':messages, 'user':User.objects.get(id=request.session['id'])})
    return result
    # return HttpResponse({'success':True, 'messages':messages})
