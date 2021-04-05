from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from . import utils
from . import models
import hashlib
from threading import Lock
from threading import Thread


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

            email_send_thread = Thread(target=utils.send_email,
                                       args=("About your registration to conference management system",
                                             "You have been registered successfully",
                                             email, email_lock))
            email_send_thread.start()

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
            return render(request, "login.html", {"is_logged_in": False, "user_message": "Incorrect E-mail address"})

        password = request.POST.get('password').encode('utf-8')
        hashed_password = hashlib.sha224(password).hexdigest()
        password_validation = utils.check_password_validity(email, hashed_password)
        if not password_validation:
            return render(request, "login.html", {"is_logged_in": False, "user_message": "Incorrect password"})

        response = render(request, "userpage.html", {"is_logged_in": True})
        utils.create_user_cookies(response, email, hashed_password)
        return response


def delete_cookies(response):
    response.delete_cookie('email')
    response.delete_cookie('password')


def logout(request):
    response = render(request, "index.html", {"is_logged_in": False})
    delete_cookies(response)
    return response


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
        user = models.User.objects.get(email=request.COOKIES.get('email'))

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
        return render(request, "complete_research_profile.html", {"is_logged_in": is_logged_in, "user_message": ""})
    return render(request, "index.html", {"is_logged_in": False})


def complete_research_profile_process(request):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        pass
    return render(request, "index.html", {"is_logged_in": False})
