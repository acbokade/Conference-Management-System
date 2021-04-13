from django.shortcuts import render
from .models import Reviewer
from .forms import ReviewerForm
from accounts import utils


def apply_as_a_reviewer(request):
    is_logged_in = utils.check_login(request)
    if request.method == "GET":
        form = ReviewerForm()
        return render(request, "apply_as_a_reviewer.html", {"is_logged_in": is_logged_in, "form": form})
    if request.method == "POST":
        form = ReviewerForm(request.POST)
        if form.is_valid():
            form.save(commit=True)


def make_review(request):
    pass


def edit_review(request):
    pass


def reviewer_assignment(request):
    pass
