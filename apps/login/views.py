# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
import bcrypt
from .models import Users


# Create your views here.
def index(request):
    if 'errors' not in request.session:
        request.session['errors'] = []
    if 'logerrors' not in request.session:
        request.session['logerrors'] = []
    context = {
        "errors": request.session['errors']
    }
    return render(request, 'login/index.html', context)

def register(request):
    request.session['errors'] = Users.objects.validator(request.POST)
    if 'email' not in request.session:
        request.session['email'] = request.POST['email']
    else:
        request.session['email'] = request.POST['email']
    if request.session['errors']['fn'] == "" and request.session['errors']['ln'] == "" and request.session['errors']['email'] == "" and request.session['errors']['pw'] == "" and request.session['errors']['cpw'] == "": 
        Users.objects.create(first_name=request.POST['fn'],last_name=request.POST['ln'],email=request.POST['email'],password=bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()))
        return redirect('/success')
    else: 
        return redirect('/')

def login(request):
    request.session['errors'] = Users.objects.logincheck(request.POST)
    request.session['email'] = request.POST['email']
    if request.session['errors']['login'] == "":
        return redirect('/success')
    else: 
        return redirect('/')

def success(request):
    context = {
        "name": Users.objects.get(email=request.session['email']).first_name
    }
    return render(request, 'login/success.html', context)