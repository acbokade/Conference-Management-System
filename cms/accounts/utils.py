import smtplib
import datetime
from . import models


def check_login(request):
    if request.COOKIES.get('password'):
        return True
    return False


def create_user_cookies(response, email, hashed_password):
    max_limit = 24*60 * 60
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_limit),
                                         "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key="email", value=email, max_age=max_limit, expires=expires)
    response.set_cookie(key="password", value=hashed_password, max_age=max_limit, expires=expires)


def check_email_validity(email):
    try:
        check_user = models.User.objects.get(email=email)
    except Exception:
        return False
    return True


def check_password_validity(email, hashed_password):
    check_user = models.User.objects.get(email=email)
    if hashed_password == check_user.password:
        return True
    return False

