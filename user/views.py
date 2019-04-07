# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json

# Return user information.
# This is for user profile page.
# Input: http:hostname/profile/{user_id}
# return json is like:
# {
#     u_id: 1,
#     username: llw,
#     img_id: 1,
#     token: 100,
#     level: 1 
# }
def getuser(request, user_id):
    if request.method != 'GET':
        return HttpResponse(status=404)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Users WHERE u_id = ' + str(user_id) + ';')
    return_data = cursor.fetchone()
    result = {}
    result['u_id'] = return_data[0]
    result['username'] = return_data[1]
    result['img_id'] = return_data[2]
    result['token'] = return_data[3]
    result['level'] = return_data[4]
    return JsonResponse(result)


# Return leaderboard information.
# This is for leaderboard page.
# Input: http:hostname/leaderboard/{user_id}
# return json is like:
# {
#   leaderboard:
#   [{
#       rank: 1,
#       img_id: 1,
#       username: llw,
#       token: 10000,
#       if_friend: true
#   }]
# }
def getleaderboard(request, user_id):
    if request.method != 'GET':
        return HttpResponse(status=404)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Users ORDER BY token DESC;')
    return_data = cursor.fetchall()
    result = {}
    row = []
    rank = 0
    for item in return_data:
        rank += 1
        the_row = {}
        the_row['rank'] = rank
        the_row['img_id'] = item[3]
        the_row['username'] = item[1]
        the_row['token'] = item[2]
        the_id = item[0]
        cursor2 = connection.cursor()
        print "1"
        if the_id < user_id:
            cursor2.execute('SELECT * FROM Friends WHERE u1_id = ' + the_id + ' AND u2_id = ' + user_id + ';')
        elif the_id > user_id:
            cursor2.execute('SELECT * FROM Friends WHERE u1_id = ' + user_id + ' AND u2_id = ' + the_id + ';')
        print "2"
        return_data = cursor.fetchone()
        print return_data
        if return_data[0]:
            the_row['if_friend'] = True
        else: the_row['if_friend'] = False
        row.append(the_row)
    result['leaderboard'] = row
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
