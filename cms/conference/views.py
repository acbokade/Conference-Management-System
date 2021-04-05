from django.shortcuts import render
from accounts import utils
from datetime import datetime
from . import models
from accounts import models as accounts_models
from .forms import ConferenceForm

def create_conference(request):
    is_logged_in = utils.check_login(request)
    if request.method == "GET":
        form = ConferenceForm()
        return render(request, "create_conference.html", {"is_logged_in": is_logged_in, "form": form})
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        short_name = request.POST.get('short_name')
        
        email = request.COOKIES.get('email')
        created_by = accounts_models.User.objects.get(email=request.COOKIES.get('email'))

        # TODO: handle errors
        ca1 = accounts_models.User.objects.get(email=request.POST.get('ca1_email'))
        ca2 = accounts_models.User.objects.get(email=request.POST.get('ca2_email'))
        ca3 = accounts_models.User.objects.get(email=request.POST.get('ca3_email'))

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
        conference.ca.add(ca1)
        conference.ca.add(ca2)
        conference.ca.add(ca3)
        conference.save()
        # afterwards portal admin validates it and sets is_valid field accordingly
        return render(request, "list_conferences.html", {"is_logged_in": is_logged_in})


def update_conference(request):
    pass


def create_workshop(request):
    pass
