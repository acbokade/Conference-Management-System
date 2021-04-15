import hashlib

from threading import Lock
from threading import Thread
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from . import utils
from . import models
from . import data_access_layer


email_lock = Lock()


def index(request):
    is_logged_in = utils.check_login(request)
    return render(request, "index.html", {"is_logged_in": is_logged_in})


def signup(request):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        logout(request)
    else:
        return render(request, "signup.html", {"is_logged_in": is_logged_in})


def singup_process(request):
    if request.method == "POST":
        email = request.POST.get('email')
        valid_email_regex = utils.check_email_regex(email)
        if not valid_email_regex:
            return render(request, "signup.html", {"is_logged_in": False,
                                                   "user_message": "invalid email address format"})

        try:
            check_user = data_access_layer.obtain_user_by_email(email)
        except Exception:
            name = request.POST.get('name')
            password = request.POST.get('password').encode('utf-8')
            confirm_password = request.POST.get('confirm password').encode('utf-8')
            if password != confirm_password:
                return render(request, "signup.html", {"is_logged_in": False,
                                            "user_message": "password and confirm password don't match"})

            hashed_password = hashlib.sha224(password).hexdigest()
            user = models.User(email=email, password=hashed_password, name=name)
            user.save()

            context = {"is_logged_in": False, "user_message": "Account Successfully Created"}
            response = render(request, "login.html", context)
            # utils.create_user_cookies(response, email, user.password)

            # email_send_thread = Thread(target=utils.send_email,
            #                            args=("About your registration to conference management system",
            #                                  "You have been registered successfully",
            #                                  email, email_lock))
            # email_send_thread.start()

            return response

        return render(request, "login.html", {"is_logged_in": False, "user_message": "Email already exists"})


def login(request):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        logout(request)
    else:
        return render(request, "login.html", {"is_logged_in": is_logged_in, "user_message": ""})


def login_process(request):
    if request.method == "POST":
        email = request.POST.get('email')
        email_validation = utils.check_email_validity(email)
        if not email_validation:
            return render(request, "login.html", {"is_logged_in": False, "user_message": "E-mail address doesn't exist"})

        password = request.POST.get('password').encode('utf-8')
        hashed_password = hashlib.sha224(password).hexdigest()
        password_validation = utils.check_password_validity(email, hashed_password)
        if not password_validation:
            return render(request, "login.html", {"is_logged_in": False, "user_message": "Incorrect password"})

        response = render(request, "userpage.html", {"is_logged_in": True})
        utils.create_user_cookies(response, email, hashed_password)
        return response


def delete_account(request):
    if request.method == "GET":
        is_logged_in = utils.check_login(request)
        if is_logged_in:
            return render(request, "delete_account.html", {"is_logged_in": is_logged_in, "user_message": ""})
        return render(request, "login.html", {"is_logged_in": is_logged_in, "user_message": ""})
    elif request.method == "POST":
        is_logged_in = utils.check_login(request)
        if is_logged_in:
            user = data_access_layer.obtain_user_by_email(request.COOKIES.get('email'))
            user.delete()
            response = render(request, "signup.html", {"is_logged_in": False, "user_message": ""})
            delete_cookies(response)
            return response
        return render(request, "login.html", {"is_logged_in": is_logged_in, "user_message": ""})


def delete_cookies(response):
    response.delete_cookie('email')
    response.delete_cookie('password')


def logout(request):
    response = render(request, "index.html", {"is_logged_in": False})
    delete_cookies(response)
    return response


def userpage(request):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        return render(request, "userpage.html", {"is_logged_in": is_logged_in, "user_message": ""})
    return render(request, "index.html", {"is_logged_in": False})


def profile(request):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        return render(request, "user_profile.html", {"is_logged_in": is_logged_in, "user_message": ""})
    return render(request, "index.html", {"is_logged_in": False})


def change_password(request):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        return render(request, "change_password.html", {"is_logged_in": is_logged_in, "user_message": ""})
    return render(request, "index.html", {"is_logged_in": False})


def change_password_process(request):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        user = data_access_layer.obtain_user_by_email(request.COOKIES.get('email'))

        oldpassword = request.POST['old_password']
        newpassword = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        hashed_old_password = hashlib.sha224(oldpassword.encode('utf-8')).hexdigest()
        old_password_validation = utils.check_password_validity(user.email, hashed_old_password)
        if not old_password_validation:
            return render(request, "change_password.html", {"is_logged_in": is_logged_in,
                                                "user_message": "incorrect old password"})
        else:
            if newpassword == confirm_password:
                context = {"is_logged_in": False, "user_message": "Password Successfully Changed"}
                response = render(request, "login.html", context)
                delete_cookies(response)
                user.password = hashlib.sha224(newpassword.encode('utf-8')).hexdigest()
                user.save()
                return response
            else:
                return render(request, "change_password.html", {"is_logged_in": is_logged_in,
                                    "user_message": "new password and confirm password do not match"})

    return render(request, "index.html", {"is_logged_in": False})


def complete_research_profile(request):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        try:
            user_research_profile = data_access_layer.obtain_research_profile(request.COOKIES.get('email'))
            context = {"is_logged_in": is_logged_in, "institution": user_research_profile.institution,
                   "research_interests": user_research_profile.research_interests,
                   "highest_degree": user_research_profile.highest_degree,
                   "google_scholar": user_research_profile.google_scholar}
        except Exception as e:
            context = {"is_logged_in": is_logged_in, "institution": "",
                       "research_interests": "", "highest_degree": "", "google_scholar": ""}
        return render(request, "complete_research_profile.html", context)
    return render(request, "index.html", {"is_logged_in": False})


def complete_research_profile_process(request):
    is_logged_in = utils.check_login(request)
    if is_logged_in and request.method == "POST":
        institution = request.POST['institution']
        research_interests = request.POST['research_interests']
        highest_degree = request.POST['highest_degree']
        google_scholar = request.POST['google_scholar']
        person = data_access_layer.obtain_user_by_email(request.COOKIES.get('email'))

        try:
            user_research_profile = data_access_layer.obtain_research_profile(request.COOKIES.get('email'))
            if institution != "":
                user_research_profile.institution = institution
            if research_interests != "":
                user_research_profile.research_interests = research_interests
            if highest_degree != "":
                user_research_profile.highest_degree = highest_degree
            if google_scholar != "":
                user_research_profile.google_scholar = google_scholar
            user_research_profile.save()
        except Exception as e:
            user_research_profile = models.ResearchProfile(person=person, institution=institution,
                                    research_interests=research_interests, highest_degree=highest_degree,
                                    google_scholar=google_scholar)
            user_research_profile.save()
        return render(request, "userpage.html", {"is_logged_in": True})

    return render(request, "index.html", {"is_logged_in": False})


def redirect_conference(request):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        return redirect('/conference/list_conferences')
    return render(request, "index.html", {"is_logged_in": False})


def redirect_my_conference(request):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        return redirect('/conference/list_my_conferences')
    return render(request, "index.html", {"is_logged_in": False})


def redirect_assigned_papers(request):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        return redirect('/reviewer/assigned_papers')
    return render(request, "index.html", {"is_logged_in": False})
