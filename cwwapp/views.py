from . import models
import json
import datetime
import requests
from django.http import HttpResponse
from cwwapp.Form import StoryForm
from django.views.decorators.csrf import csrf_exempt
import simplejson

@csrf_exempt
def login(request):
    http_response = HttpResponse()
    http_response["Content-Type"] = 'text-plain'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            author = models.Author.objects.get(username=username)
            if password == author.password:
                request.session['is_login'] = 'true'
                request.session['loginname'] = author.username
                request.session.set_expiry(86400)
                http_response.status_code = 200
                http_response.content = 'Login success, Welcome!'
            else:
                http_response.status_code = 401
                http_response.content = 'Password incorrect!'
        except:
            http_response.status_code = 401
            http_response.content = "Username not found!"
            return http_response

        return http_response

    else:
        http_response.status_code = 405
        http_response.content = "Error when call the method."
        return http_response

@csrf_exempt
def logout(request):
    http_response = HttpResponse()
    http_response["Content-Type"] = 'text-plain'
    if request.method == 'POST':
        try:
            if request.session['is_login'] == 'true':
                http_response.status_code = 200
                http_response.content = 'Log out success! Good Bye!'
                request.session.clear()
                return http_response
            else:
                http_response.status_code = 401
                http_response.content = 'Error! Please login first!'
                return http_response
        except:
            http_response.status_code = 401
            http_response.content = 'Error! Please login first!'
            return http_response
    else:
        http_response.status_code = 405
        http_response.content = "Error when call the method."
        return http_response

@csrf_exempt
def poststory(request):
    http_response = HttpResponse()
    http_response["Content-Type"] = 'text-plain'
    http_response.status_code = 503
    if request.method == 'POST':
        if request.session['is_login'] == 'true':
            new_story = StoryForm(simplejson.loads(request.body)).save(commit = False)
            author = models.Author.objects.get(username=request.session['loginname'])
            new_story.author = author
            new_story.save()
            http_response.status_code = 201
            http_response.content = "CREATED"
        else:
            http_response.content = "Please login first."
    else:
        http_response.status_code = 503
        http_response.content = "Error when call the method."
    return http_response

def getStories(request):
    http_response = HttpResponse()
    http_response["Content-Type"] = 'text-plain'
    if request.method == 'GET':
        filter_dict = simplejson.loads(request.body)
        search_dict = dict()
        if filter_dict["story_cat"] != "*":
            search_dict["category"] = filter_dict["story_cat"]
        if filter_dict['story_region'] != "*":
            search_dict["region"] = filter_dict['story_region']
        if filter_dict["story_date"] != "*":
            day, month, year = filter_dict["story_date"].split('/')
            date = datetime.datetime(int(year), int(month), int(day))
            search_dict["date"] = date

        stories = models.Story.objects.filter(**search_dict).all()
        if len(stories) == 0:
            http_response.status_code = 404
            http_response.content = "No story found"
        else:
            story_json = [story.to_json() for story in stories]
            return_response = {"stories": story_json}
            http_response["Content-Type"] = "application/json"
            http_response.content = json.dumps(return_response)
            http_response.status_code = 200
        return http_response
    else:
        http_response.status_code = 405
        http_response.content = "Error when call the method."
        return http_response

@csrf_exempt
def deleteStory(request):
    http_response = HttpResponse()
    http_response["Content-Type"] = 'text-plain'
    http_response.status_code = 503
    if request.method == 'POST':
        if request.session['is_login'] == 'true':
            key = int(simplejson.loads(request.body)["story_key"])
            try:
                story = models.Story.objects.get(id=key)
            except:
                http_response.content = "Story with id " + str(key) + " no found"
                return http_response
            story.delete()
            http_response.status_code = 201
            http_response.content = "CREATED"
        else:
            http_response.content = "Please Login first!"
    else:
        http_response.content = "Method error, only POST!!!"
    return http_response
