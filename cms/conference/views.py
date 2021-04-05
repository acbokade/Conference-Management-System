from django.shortcuts import render
from cms.accounts import utils
from datetime import datetime
from . import models
from cms.accounts import models as accounts_models

def create_conference(request):
    if request.method == "POST":
        name = request.POST.get('name')
        short_name = request.POST.get('short_name')
        
        email = request.COOKIES.get('email')
        ca = accounts_models.User.objects.get(email=request.COOKIES.get('email'))



        start_date = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%dT%H:%M')
        end_date = datetime.strptime(request.POST.get('end_date'), '%Y-%m-%dT%H:%M')
        logo = None
        url = None
        subject_areas = request.POST.get('subject_areas')
        expected_submissions = request.POST.get('expected_submissions')
        conference = models.Conference(name=name, short_name=short_name,
                                       ca=ca, start_date=start_date,
                                       end_date=end_date, logo=logo,
                                       url=url, subject_areas=subject_areas,
                                       expected_submissions=expected_submissions)
        conference.save()
        return render(request, "list_conferences.html", {"is_logged_in": is_logged_in})


def update_conference(request):
    pass


def create_workshop(request):
    pass
