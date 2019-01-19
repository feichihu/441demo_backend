# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json

# Create your views here.
def getchatts(request):
    if request.method != 'GET':
        return HttpResponse(status=404)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM chatts;')
    rows = cursor.fetchall()
    row = [[item[0],item[1],item[2]] for item in rows]
    result = {}
    result['chatts'] = row
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
