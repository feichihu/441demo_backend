# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json

# Return user information.
# This is for user profile page.
# Input http:hostname/profile/1
# return json is like:
# {
#     u_id: 1,
#     username: llw,
#     img_id: 1,
#     token: 100,
#     level: 1 
# }
def getuser(request, user_id):
    print "I'm in"
    if request.method != 'GET':
        return HttpResponse(status=404)
    cursor = connection.cursor()
    print "I'm in 2"
    cursor.execute('SELECT * FROM Users WHERE u_id = ' + str(user_id) + ';')
    return_data = cursor.fetchone()
    print return_data
    result = {}
    result['u_id'] = return_data[0]
    result['username'] = return_data[1]
    result['img_id'] = return_data[2]
    result['token'] = return_data[3]
    result['level'] = return_data[4]
    print result
    return JsonResponse(result)

@csrf_exempt
def addchatt(request):
    if request.method != 'POST':
        return HttpResponse(status=404)
    json_data = json.loads(request.body)
    username = json_data['username']
    message = json_data['message']
    cursor = connection.cursor()
    cursor.execute('INSERT INTO chatts (username, message) VALUES '
                    '(%s, %s);', (username, message))
    return JsonResponse({})


@csrf_exempt
def adduser(request):
    if request.method != 'POST':
        return HttpResponse(status=404)
    json_data = json.loads(request.body)
    username = json_data['username']
    name = json_data['name']
    email = json_data['email']
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users (username, name, email) VALUES '
                    '(%s, %s, %s);', (username, name, email))
    return JsonResponse({})
