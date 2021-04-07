import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Thread
import datetime
import re
from . import models
from . import constants
from . import data_access_layer


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
        check_user = data_access_layer.obtain_user_by_email(email)
    except Exception as e:
        return False
    return True


def check_password_validity(email, hashed_password):
    check_user = data_access_layer.obtain_user_by_email(email)
    if hashed_password == check_user.password:
        return True
    return False


def check_email_regex(email):
    if re.search(constants.VALID_EMAIL_REGEX, email):
        return True
    return False


def send_email(subject, message, to, email_lock):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = constants.CMS_EMAIL
    msg['To'] = to

    # The main body is just another attachment
    body = MIMEText(message)
    msg.attach(body)
    # print("message created")
    # print(message)
    # print("attachments attached")

    email_lock.acquire()
    try:
        s = smtplib.SMTP('smtp-mail.outlook.com', 587)
        print("connected to smtp")
        s.starttls()
        s.login(constants.CMS_EMAIL, constants.CMS_PASSWORD)
        print("logged in to smtp")
        s.sendmail(constants.CMS_EMAIL, to, msg.as_string())
        print("e mail sent")
        s.quit()
        email_lock.release()
    except Exception as e:
        print(e)
        email_lock.release()
    print("connection exited")
