from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from . import utils
from . import models
import hashlib


def index(request):
    is_logged_in = utils.check_login(request)
    return render(request, "index.html", {"is_logged_in": is_logged_in})


def signup(request):
    is_logged_in = utils.check_login(request)
    return render(request, "signup.html", {"is_logged_in": is_logged_in})


def singup_process(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            check_user = models.User.objects.get(email=email)
        except Exception:
            name = request.POST.get('name')
            password = request.POST.get('password').encode('utf-8')
            hashed_password = hashlib.sha224(password).hexdigest()
            user = models.User(email=email, password=hashed_password, name=name)
            user.save()

            context = {"is_logged_in": False, "user_message": "Account Successfully Created"}
            response = render(request, "login.html", context)
            # utils.create_user_cookies(response, email, user.password)
            return response

        if check_user:
            return render(request, "login.html", {"is_logged_in": False, "user_message": "Email already exists"})


def login(request):
    is_logged_in = utils.check_login(request)
    return render(request, "login.html", {"is_logged_in": is_logged_in, "user_message": ""})


def login_process(request):
    if request.method == "POST":
        email = request.POST.get('email')
        email_validation = utils.check_email_validity(email)
        if not email_validation:
            return render(request, "login.html", {"is_logged_in": False, "user_message": "Incorrect E-mail address"})

        password = request.POST.get('password').encode('utf-8')
        hashed_password = hashlib.sha224(password).hexdigest()
        password_validation = utils.check_password_validity(hashed_password)
        if not password_validation:
            return render(request, "login.html", {"is_logged_in": False, "user_message": "Incorrect password"})

        response = render(request, "index.html", {"is_logged_in": False})
        utils.create_user_cookies(response, email, hashed_password)
        return response