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

# Return user friends information.
# This is for user profile page.
# Input http:hostname/profile/friends/1
# return json is like:
# {
#     'friends':
#     [
#         {
#             'u_id': 2,
#             'username': 'jhe',
#             'img_id': 5,
#             'best_song': 'love story'
#         },
#         {
#             'u_id': 3,
#             'username': 'cmm',
#             'img_id': 8,
#             'best_song': 'in the name of father'
#         }
#     ]
# }
def getfriends(request, user_id):
    print "I'm in"
    if request.method != 'GET':
        return HttpResponse(status=404)

    result = {'friends': []}
    cursor1 = connection.cursor()
    cursor1.execute('SELECT * FROM friends WHERE u1_id = ' + str(user_id) + ';')
    friends1 = cursor1.fetchall()
    friends1 = [i[1] for i in friends1]
    cursor2 = connection.cursor()
    cursor2.execute('SELECT * FROM friends WHERE u2_id = ' + str(user_id) + ';')
    friends2 = cursor2.fetchall()
    friends2 = [i[0] for i in friends2]
    friends = friends1 + friends2
    
    print friends

    for f_id in friends:
        friend_info = {}
        cursor3 = connection.cursor()
        cursor3.execute('SELECT * FROM users WHERE u_id = ' + str(f_id) + ';')
        f_info = cursor3.fetchone()

        print 'f_info', f_info

        friend_info['username'] = f_info[1]
        friend_info['img_id'] = f_info[3]
        cursor4 = connection.cursor()
        cursor4.execute('SELECT album_name FROM songs ' +
                        'WHERE score = ( SELECT max(score) FROM songs )')
        f_song_info = cursor4.fetchone()

        print 'f_song_info', f_song_info

        friend_info['best_song'] = f_song_info[0]
        result['friends'].append(friend_info)

    print result
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
        print item
        rank += 1
        the_row = {}
        the_row['rank'] = rank
        the_row['img_id'] = item[3]
        the_row['username'] = item[1]
        the_row['token'] = item[2]
        the_id = item[0]

        cursor2 = connection.cursor()
        print 'the_id:' + str(the_id)
        print 'user_id:' + str(user_id)
        
        if the_id < int(user_id):
            the_string = 'SELECT * FROM Friends WHERE u1_id = ' + str(the_id) + ' AND u2_id = ' + str(user_id) + ' ;'
            print the_string
            cursor2.execute(the_string)
        else:
            the_string = 'SELECT * FROM Friends WHERE u1_id = ' + str(user_id) + ' AND u2_id = ' + str(the_id) + ' ;'
            print the_string
            cursor2.execute(the_string)
        rd = cursor2.fetchall()
        print rd
        # for the_tuple in rd:
        #     if (the_tuple[0] == the_id and the_tuple[1] == int(user_id)) or (the_tuple[1] == the_id and the_tuple[0] == int(user_id)):
        #         the_row['if_friend'] = True
        #         break
        if rd:
            the_row['if_friend'] = True
        the_row['if_friend'] = False

        # print return_data
        # print type(return_data)
        # print cursor2.rowcount
        # if cursor2.rowcount != 0:
        #     the_row['if_friend'] = True
        # else: the_row['if_friend'] = False
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
                    '(%d, %s, %d, %d, %d);', (ID, username, 0, img_id, 1))
    return JsonResponse({})


# curl -X POST --header "Content-Type: application/json
# --data '{"u_id":4, "username":"yqy"}'
# http://localhost:9000/updatename/
@csrf_exempt
def updatename(request):
    if request.method != 'POST':
        return HttpResponse(status=404)
    json_data = json.loads(request.body)
    u_id = json_data['u_id']
    username = json_data['username']
    cursor = connection.cursor()
    toExecute = "UPDATE users SET username = '" + str(username) + "' WHERE u_id = " + str(u_id) + ";"
    cursor.execute(toExecute)
    return JsonResponse({})


# curl -X POST --header "Content-Type: application/json
# --data '{"u1_id": 3, "u2_id": 4}'
# http://localhost:9001/updatename/
@csrf_exempt
def addfriend(request):
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
    print u1_id
    print u2_id
    cursor.execute('INSERT INTO friends (u1_id, u2_id) VALUES '
                    '(%d, %d);', (u1_id, u2_id))
    return JsonResponse({})