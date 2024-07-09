from django.shortcuts import render
from django.http import HttpResponse
import json
import re
from django.shortcuts import redirect
from datetime import datetime
# Create your views here.

def registerUsers(request):
    global dictionary
    if(request.method == 'POST'):
        dictionary = {}
        title = request.POST.get('title')
        description = request.POST.get('description')
        totalparticipants = request.POST.get('totalparticipants')
        startdate = request.POST.get('startdate')
        enddate = request.POST.get('enddate')
        if(re.search('^[a-zA-Z ]+$',title)):
            dictionary['title'] = title
        if(re.search('^[a-zA-Z_. ]+$', description)):
            dictionary['description'] = description
        if(re.match(r'^([\s\d]+)$', totalparticipants)):
            dictionary['totalparticipants'] = totalparticipants
        if(startdate):
            dictionary['startdate'] = startdate
        if(enddate):
            dictionary['enddate'] = enddate
          
        stringjson = json.dumps(dictionary) 
        # print(dictionary)
        with open('data.json', 'r') as file:
            readlines = file.read()
            data = json.loads(readlines)
        # print(list(data))
        data= list(data).__add__([dictionary])
        datastring = json.dumps(data)
        # print(data)
        with open('data.json', 'w') as file:
            writeInto = file.write(datastring)
            
        return redirect('show')
    else:
        return render(request, 'regist_form.html')
    
def getDataFromUser(request):
    global dictionary
    if(request.method == 'POST'):
        dictionary = {}
        title = request.POST.get('title')
        description = request.POST.get('description')
        totalparticipants = request.POST.get('totalparticipants')
        startdate = request.POST.get('startdate')
        enddate = request.POST.get('enddate')
        if(re.search('^[a-zA-Z ]+$',title)):
            dictionary['title'] = title
        if(re.search('^[a-zA-Z0-9_.-]+$', description)):
            dictionary['description'] = description
        if(re.match(r'^([\s\d]+)$', totalparticipants)):
            dictionary['totalparticipants'] = totalparticipants
        if(startdate):
            dictionary['startdate'] = startdate
        if(enddate):
            dictionary['enddate'] = enddate
          
        stringjson = json.dumps(dictionary) 
        print('Type of String Json',type(stringjson))
        with open('data.json', 'a+') as file:
            file.writelines(stringjson)
        file.close()
        return HttpResponse(json.dumps(dictionary))
        # return render(request, 'register_details.html', {'details': dictionary })
    
    else:
        return render(request, 'regist_form.html')

dictionary = '[{"name":"Prahlad"}]'
from . import ExtraMenthods
def showRegisteredUser(request):
    i = 0
    file = open("data.json", "r")
    x = file.read()
    # print(x)
    data = json.loads(x)
    file.close()
    return render(request, 'register_details.html', {'details': data, 'i':i })

from . import ExtraMenthods
def updateUser(request, id:int):
    id = id-1
    with open('data.json', 'r') as file:
        x = file.read()
    data = json.loads(x)
    print(data)
    # print(datadic['title'])
    if (request.method == 'POST'):
        title = request.POST.get('title')
        description = request.POST.get('description')
        totalparticipants = request.POST.get('totalparticipants')
        startdate = request.POST.get('startdate')
        enddate = request.POST.get('enddate')
        if(title):
            update = data[id]['title'] = title
        if(description):
            update = data[id]['description'] = description
        if(totalparticipants):
            update = data[id]['totalparticipants'] = totalparticipants
        if(startdate):
            update = data[id]['startdate'] = startdate
        if(enddate):
            update = data[id]['enddate'] = enddate
        # print(update)
        # print(data)
        datastring = json.dumps(data)
        
        with open('data.json', 'w') as file:
            file.writelines(datastring)
        # return HttpResponse(f'updated successfull {datastring} ')
        return redirect('show')
            
    context = {'data': data[id], 'index': x[int(id)]}
    return render(request, 'edit.html', context)

def deleteUser(request, id:int):
    with open('data.json', 'r') as file:
        readfile = file.read()
        data = json.loads(readfile)
    # print(data)
    # if(request.method == 'POST'):
    if(data[id-1]):
        del data[id-1]
        data = json.dumps(data)
        with open('data.json', 'w') as file:
            x = file.write(data)
        print(data)
        return redirect('show')
    return render(request, 'register_details.html', {'details': data})

from uuid import uuid4
import requests
from django.contrib.sessions.models import Session
class UserLoginView():
    
    def userCreate(request):
        dictitem = {}
        if(request.method == 'POST'):
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            username = request.POST.get('username')
            password = request.POST.get('password1')
            hidden = request.POST.get('hidden')
            dictitem.update({'firstname':firstname, 'lastname': lastname, 'username':username, 'password':password, 'hidden': hidden})
            
            data = json.dumps([dictitem], indent=4)
            
            with open('logins.json', 'r+') as file:
                r = file.read()
                if(r == ''):
                    w = file.write(data)
                    # return HttpResponse(data)
                    return redirect('home')
                else:
                    # print('not empty', r)
                    readdata = json.loads(r)
                    readdata = readdata.__add__([dictitem])
                    readdata = json.dumps(readdata, indent=4)
                    seek = file.seek(0)
                    dele = file.truncate()
                    w = file.write(readdata)
                    isLoggedIn = True
                    # return HttpResponse(readdata)
                    return redirect('home')
        return render(request, 'user-logins-tmp/user_create.html')
    
    def userLogin(request):
        if(request.method == 'POST'):
            username = request.POST.get('username')
            password = request.POST.get('password')
            with open('logins.json', 'r') as file:
                read = file.read()
            jsondata = json.loads(read)
            for items in jsondata:
                if(username == items['username'] and password == items['password']):
                    #  session
                    sessusername = request.session['username'] = username
                    sessuserkey = request.session['userkey'] = str(uuid4())
                    expiry = request.session.set_expiry(0)
                    return redirect('home')
                
            return HttpResponse(f"'You are not Register. <a href = '#'>Rgister Here</a>")
        return render(request, 'user-logins-tmp/user_login.html')
    
    def userHome(request):
        if(request.session.get('userkey')):
            isLoggedIn = True
            return render(request, 'user-logins-tmp/user_home.html', {'isLoggedIn': isLoggedIn})
        else:
            isLoggedIn = False
            return render(request, 'user-logins-tmp/user_home.html', {'isLoggedIn': isLoggedIn})
    
    def userLogout(request):
        Session.objects.all().delete()
        return redirect('home')
        