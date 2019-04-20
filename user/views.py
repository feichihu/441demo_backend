# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json
import arrow

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
    toExecute = "SELECT * FROM Users WHERE u_id = '" + str(user_id) + "';"
    cursor.execute(toExecute)
    return_data = cursor.fetchone()
    result = {}
    result['u_id'] = return_data[0]
    result['username'] = return_data[1]
    result['img_id'] = return_data[2]
    result['token'] = return_data[3]
    result['level'] = return_data[4]
    return JsonResponse(result)


# Return user information.
# This is for search bar.
# curl -X POST --header "Content-Type: application/json" 
# --data '{"username":"qyao", "self_u_id":"1"}'
# http://localhost:9000/searchuser/{user_id}
# return json is like:
# {
#     u_id: 8,
#     username: 'qyao',
#     img_id: 2,
#     token: 100,
#     level: 1,
#     friend_status: 'n';
# }
# there are three options for friend_status:
# 'f': friends
# 'n': not friends
# 'p': pending friends, either i have sent request to this user,
# or this user has sent request to me.
@csrf_exempt
def search_user(request):
    if request.method != 'POST':
        return HttpResponse(status=404)
    result = {}
    json_data = json.loads(request.body)
    username = json_data['username']
    self_u_id = json_data['self_u_id']

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = '" + username + "';")
    return_data = cursor.fetchone()

    the_id = return_data[0]
    result['u_id'] = the_id
    result['username'] = return_data[1]
    result['img_id'] = return_data[2]
    result['token'] = return_data[3]
    result['level'] = return_data[4]

    result['friend_status'] = 'n'

    cursor1 = connection.cursor()
    cursor1.execute("SELECT * FROM friends WHERE u1_id = '" + str(self_u_id) +
                    "' and u2_id = '" + str(the_id) + "';")
    cursor2 = connection.cursor()
    cursor2.execute("SELECT * FROM friends WHERE u1_id = '" + str(the_id) +
                    "' and u2_id = '" + str(self_u_id) + "';")
    row1 = cursor1.fetchone()
    row2 = cursor2.fetchone()
    if row1 != None or row2 != None:
        result['friend_status'] = 'f'

    cursor3 = connection.cursor()
    cursor3.execute("SELECT * FROM pending_friends WHERE u1_id = '" + str(self_u_id) +
                    "' and u2_id = '" + str(the_id) + "';")
    cursor4 = connection.cursor()
    cursor4.execute("SELECT * FROM pending_friends WHERE u1_id = '" + str(the_id) +
                    "' and u2_id = '" + str(self_u_id) + "';")
    row3 = cursor3.fetchone()
    row4 = cursor4.fetchone()
    if row3 != None or row4 != None:
        result['friend_status'] = 'p'

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
#             'best_song': 'love story',
#             'link': 'google.com'
#         },
#         {
#             'u_id': 3,
#             'username': 'cmm',
#             'img_id': 8,
#             'best_song': 'in the name of father',
#             'link': 'google.com'
#         }
#     ]
# }
def getfriends(request, user_id):
    if request.method != 'GET':
        return HttpResponse(status=404)

    result = {'friends': []}
    cursor1 = connection.cursor()
    cursor1.execute("SELECT * FROM friends WHERE u1_id = '" + str(user_id) + "';")
    friends1 = cursor1.fetchall()
    friends1 = [i[1] for i in friends1]
    cursor2 = connection.cursor()
    cursor2.execute("SELECT * FROM friends WHERE u2_id = '" + str(user_id) + "';")
    friends2 = cursor2.fetchall()
    friends2 = [i[0] for i in friends2]
    friends = friends1 + friends2


    for f_id in friends:
        friend_info = {}
        cursor3 = connection.cursor()
        cursor3.execute("SELECT * FROM users WHERE u_id = '" + str(f_id) + "';")
        f_info = cursor3.fetchone()

        friend_info['u_id'] = f_info[0]
        friend_info['username'] = f_info[1]
        friend_info['img_id'] = f_info[3]
        cursor4 = connection.cursor()
        cursor4.execute("SELECT * FROM songs " +
                        "WHERE u_id ='" + str(f_id) + "';")
        f_song_info = cursor4.fetchall()

        friend_info['best_song'] = ''
        friend_info['link'] = ''
        max_score = 0
        for item in f_song_info:
            if item[2] > max_score:
                max_score = item[2]
                friend_info['best_song'] = item[4]
                friend_info['link'] = item[3]

        result['friends'].append(friend_info)

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
        the_id = item[0]
        the_row['u_id'] = the_id
        the_row['username'] = item[1]
        the_row['token'] = item[2]
        the_row['img_id'] = item[3]
        cursor2 = connection.cursor()
        if the_id < int(user_id):
            the_string = "SELECT * FROM Friends WHERE u1_id = '" + str(the_id) + "' AND u2_id = '" + str(user_id) + "' ;"
            cursor2.execute(the_string)
        else:
            the_string = "SELECT * FROM Friends WHERE u1_id = '" + str(user_id) + "' AND u2_id = '" + str(the_id) + "' ;"
            cursor2.execute(the_string)
        rd = cursor2.fetchall()
        if rd:
            the_row['if_friend'] = True
        else:
            the_row['if_friend'] = False
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


# curl -X POST --header "Content-Type: application/json" 
# --data '{"username":"qyao", "img_id": 2}'
# http:localhost:9000/adduser/
@csrf_exempt
def adduser(request):
    if request.method != 'POST':
        return HttpResponse(status=404)
    json_data = json.loads(request.body)
    username = json_data['username']
    img_id = json_data['img_id']
    cursorid = connection.cursor()
    cursorid.execute('SELECT MAX(u_id) FROM Users;')
    return_data = cursorid.fetchone()
    ID = int(return_data[0])
    ID += 1
    cursor = connection.cursor()
    toExecute = "INSERT INTO users (u_id, username, token, img_id, level) VALUES ('" + str(ID) + "', '" + str(username) + "', " + str(0) + ", " + str(img_id) + ", 1);"
    cursor.execute(toExecute)
    return JsonResponse({})


# curl -X POST --header "Content-Type: application/json"
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
    toExecute = "UPDATE users SET username = '" + str(username) + "' WHERE u_id = '" + str(u_id) + "';"
    cursor.execute(toExecute)
    return JsonResponse({})


# curl -X POST --header "Content-Type: application/json" --data '{"wantFollower": 2, "beFollowed": 4}' http://localhost:9000/addfriend/
# --data '{"wantFollower": 3, "beFollowed": 4}'
# http://localhost:9000/updatename/
@csrf_exempt
def addfriend(request):
    if request.method != 'POST':
        return HttpResponse(status=404)
    json_data = json.loads(request.body)
    user1 = json_data['wantFollower']
    user2 = json_data['beFollowed']
    if int(user1) > int(user2):
        temp = user2
        user2 = user1
        user1 = temp
    cursor = connection.cursor()
    deleteExecute = "DELETE FROM pending_friends WHERE u1_id = '" + str(user2) + "' and u2_id = '" + str(user1) + "';"
    cursor.execute(deleteExecute)
    toExecute = "INSERT INTO friends (u1_id, u2_id) VALUES ('" + str(user1) + "', '" + str(user2) + "');"
    cursor.execute(toExecute)
    return JsonResponse({})


# Return pending friends information of <user_id>.
# This is for user pending friends page.
# Input: http:hostname/getpending/{user_id}/
# e.g. if user 2 and user 3 sent friend request to 1,
# curl http:hostname/getpending/1/
# would return
# {
#     'pending_friends':
#     [
#         {
#             'u_id': 2,
#             'username': 'jhe',
#             'img_id': 5,
#             'token': 10000
#         },
#         {
#             'u_id': 3,
#             'username': 'cmm',
#             'img_id': 8
#             'token': 20000
#         }
#     ]
# }
def getpending(request, user_id):
    if request.method != 'GET':
        return HttpResponse(status=404)

    result = {'pending_friends': []}
    cursor1 = connection.cursor()
    cursor1.execute("SELECT * FROM Pending_friends WHERE u1_id = '" + str(user_id) + "';")
    pending_friends = cursor1.fetchall()
    pending_friends = [i[1] for i in pending_friends]

    for pf_id in pending_friends:
        pfriend_info = {}
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE u_id = '" + str(pf_id) + "';")
        pf_info = cursor.fetchone()
        pfriend_info['u_id'] = pf_id
        pfriend_info['username'] = pf_info[1]
        pfriend_info['token'] = pf_info[2]
        pfriend_info['img_id'] = pf_info[3]
        result['pending_friends'].append(pfriend_info)

    return JsonResponse(result)


# curl -X POST --header "Content-Type: application/json"
# --data '{"wantFollower": 3, "beFollowed": 4}'
# http://localhost:9000/addpending/
@csrf_exempt
def addpending(request):
    if request.method != 'POST':
        return HttpResponse(status=404)
    json_data = json.loads(request.body)
    wantFollower = json_data['wantFollower']
    beFollowed = json_data['beFollowed']
    cursor = connection.cursor()
    toExecute = "INSERT INTO pending_friends (u1_id, u2_id) VALUES ('" + str(beFollowed) + "', '" + str(wantFollower) + ");"
    cursor.execute(toExecute)
    return JsonResponse({})


# Post: ["token": ?, "score": ?, "date": ? ]
@csrf_exempt
def delete_pending(request):
    if request.method != 'POST':
        return HttpResponse(status=404)
    json_data = json.loads(request.body)
    user1 = json_data['u1_id']
    user2 = json_data['u2_id']
    cursor = connection.cursor()
    toExecute = "DELETE FROM pending_friends WHERE u1_id = '" + str(user1) + "' and u2_id = '" + str(user2) + "';"
    cursor.execute(toExecute)
    return JsonResponse({})


#Table:
#u_id, time, score, link, song_name
# Post: ["u_id":  "token": ?]
@csrf_exempt
def update_all(request):
    if request.method != 'POST':
        return HttpResponse(status=404)
    json_data = json.loads(request.body)
    user_id = int(json_data['u_id'])

    print "1"

    cursor1 = connection.cursor()
    cursor1.execute(" SELECT * FROM Users WHERE u_id = '" + str(user_id) + "';")

    print "2"

    user_info = cursor1.fetchall()[0]

    print user_info

    past_token = int(user_info[2])

    print past_token

    new_token = int(json_data['token'])

    token =  new_token + past_token
    cursor3 = connection.cursor()
    cursor3.execute(" UPDATE Users SET token = " + str(token) + "WHERE u_id = '" + str(user_id) + "';")

    result = {}

    return JsonResponse(result)

#Post: [ u_id: xxx sing_time: xxx score: xxx link: xxx song_name: xxx]
@csrf_exempt
def Update_Link(request):
    if request.method != 'POST':
        return HttpResponse(status=404)
    json_data = json.loads(request.body)
    u_id = int(json_data['u_id'])
    sing_time = json_data['sing_time']
    sing_time = arrow.get(sing_time, 'YYYY-MM-DD HH:mm:ss')
    sing_time = sing_time.format('YYYY-MM-DD HH:mm:ss')

    score = int(json_data['score'])
    link = json_data['link']
    song_name = json_data['song_name']

    cursor = connection.cursor()
    cursor.execute("INSERT INTO songs (u_id, sing_time, score, link, song_name) VALUES ('" +str(u_id)+"', '"+str(sing_time)+"', "+str(score)+", '"+str(link)+"', '"+str(song_name)+"');" )
    result = {}

    return JsonResponse(result)



# Post: [u_id: sing_time: ]
# return json:
# {'link': 'xxxx' } or { }
@csrf_exempt
def Search_song(request):
    '''
    When user press the share button for a song,
    He needs a link for this song.
    If he hasn't uploaded to the cloud before,
    return empty result
    Else return the link for this song.
    '''

    if request.method != 'GET':
        return HttpResponse(status=404)
    json_data = json.loads(request.body)
    u_id = json_data['u_id']
    sing_time = json_data['sing_time']

    result = {}

    print "1"

    cursor1 = connection.cursor()

    print " SELECT * FROM Songs WHERE u_id = '" + str(u_id) + "' AND sing_time = '" + str(sing_time) + "';"
    cursor1.execute(" SELECT * FROM Songs WHERE u_id = '" + str(u_id) + "' AND sing_time = '" + str(sing_time) + "';")

    print "23333"
    user_info = cursor1.fetchall()
    if not user_info:
        return JsonResponse(result)

    print "2"

    user_info = user_info[0]

    print user_info
    link = user_info[3]

    result['link'] = link

    print result
    return JsonResponse(result)
