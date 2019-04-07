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
        print the_id
        print type(the_id)
        if the_id < user_id:
            cursor2.execute('SELECT * FROM Friends WHERE u1_id = ' + str(the_id) + ' AND u2_id = ' + str(user_id) + ' ;')
        elif the_id > user_id:
            cursor2.execute('SELECT * FROM Friends WHERE u1_id = ' + str(user_id) + ' AND u2_id = ' + str(the_id) + ' ;')
        print "2"
        return_data = cursor2.fetchone()
        print return_data
        print type(return_data)
        print cursor2.rowcount
        if return_data != ():
            the_row['if_friend'] = True
        else: the_row['if_friend'] = False
        print the_row
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
    img_id = json_data['img_id']
    cursorid = connection.cursor()
    cursorid.execute('SELECT MAX(u_id) FROM Users;')
    return_data = cursor.fetchone()
    ID = return_data[0]
    ID += 1
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users (u_id, username, token, img_id, level) VALUES '
                    '(%d, %s, %d, %d, %d);', (ID, username, 0, img_id, 0))
    return JsonResponse({})


@csrf_exempt
def updatename(request):
    if request.method != 'POST':
        return HttpResponse(status=404)
    json_data = json.loads(request.body)
    u_id = json_data['u_id']
    username = json_data['username']
    cursor = connection.cursor()
    cursor.execute('UPDATE users SET username = ' + str(username) +
                    'WHERE u_id = ' + str(u_id) + ';')
    return JsonResponse({})


@csrf_exempt
def addFriend(request):
    if request.method != 'POST':
        return HttpResponse(status=404)
    json_data = json.loads(request.body)
    u1_id = json_data['u1_id']
    u2_id = json_data['u2_id']
    cursor = connection.cursor()
    if u1_id > u2_id:
        temp = u2_id
        u2_id = u1_id
        u1_id = temp
    cursor.execute('INSERT INTO Friends (u1_id, u2_id) VALUES '
                    '(%d, %d);', (u1_id, u2_id))
    return JsonResponse({})