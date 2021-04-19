from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Reviewer, InvitedReviewers, AssignedReviewers
from .forms import ReviewerForm, ReviewForm, InviteReviewersForm
from accounts import utils
from . import data_access_layer as reviewer_dao
from accounts import data_access_layer as accounts_dao
from conference import data_access_layer as conference_dao
from area_chair.models import AssignedAreaChairs, AreaChair
from gsp import data_access_layer as gsp_dao
from conference import views as conf_views
from .utils import assign_reviewers
from .constants import REVIEWER_APPLICATION_DEADLINE, INVITE_REVIEWERS_DEADLINE


def redirect_signup(request):
    return redirect('/accounts/signup')


def redirect_login(request):
    return redirect('/accounts/login')


def redirect_logout(request):
    return redirect('/accounts/logout')


def redirect_userpage(request):
    return redirect('/accounts/userpage')


def apply_as_a_reviewer(request, conf_name):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        conf = conference_dao.get_conference_by_name(conf_name)
        cur_user_email = request.COOKIES.get('email')
        # check if user is in the list of invited reviewers
        invited_reviewers_emails = reviewer_dao.get_invited_reviewers_emails_of_conf(
            conf_name)
        if cur_user_email not in invited_reviewers_emails:
            messages.error(
                request, f"Sorry, you are not invited reviewer for this conference")
            return redirect(conf_views.list_conferences)
        # reviewer application deadline check
        cur_time = timezone.now()
        if (cur_time - conf.paper_submission_deadline).days > REVIEWER_APPLICATION_DEADLINE:
            messages.error(
                request, f"Sorry, Reviewer application deadline has been elapsed")
            return redirect(conf_views.list_conferences)
        if request.method == "POST":
            form = ReviewerForm(request.POST)
            if form.is_valid():
                reviewer = form.save(commit=False)
                reviewer.conference = conference_dao.get_conference_by_name(
                    conf_name)
                reviewer.user = accounts_dao.obtain_user_by_email(
                    request.COOKIES.get('email'))
                reviewer.save()
                messages.info(
                    request, f"You have sucessfully applied for the reviewer")
                # pass messages to list conf
                return redirect(conf_views.list_conferences)
            return render(request, "apply_as_a_reviewer.html", {"is_logged_in": is_logged_in, "form": form, "name": conf_name})
        else:
            conf_subject_areas = conf.subject_areas.split(',')
            form = ReviewerForm(conf_subject_areas=conf_subject_areas)
        return render(request, "apply_as_a_reviewer.html", {"is_logged_in": is_logged_in, "form": form, "name": conf_name})
    return redirect('/accounts/login')


def assigned_papers(request):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        current_reviewer_confs = Reviewer.objects.all().filter(
            user=request.COOKIES.get('email'))
        conf_assignments = []
        for cf in current_reviewer_confs:
            current_conf_assignment = AssignedReviewers.objects.all().filter(reviewer=cf)
            current_conf_assigned_papers = [
                a.paper_submission for a in current_conf_assignment]
            conf_assignments.extend(current_conf_assigned_papers)

        # code for Area Chair assignments
        current_ac_confs = AreaChair.objects.all().filter(
            user=request.COOKIES.get('email'))
        ac_assignments = []
        for ac in current_ac_confs:
            ac_current_conf_assignment = AssignedAreaChairs.objects.all().filter(area_chair=ac)
            ac_current_conf_assigned_papers = [
                a.paper_submission for a in ac_current_conf_assignment]
            ac_assignments.extend(ac_current_conf_assigned_papers)

        return render(request, "assigned_papers.html", {"is_logged_in": is_logged_in,
                                                        "conf_assignments": conf_assignments,
                                                        "ac_assignments": ac_assignments})
    return redirect('/accounts/login')


def make_review(request, conf_name, title):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        cur_user_email = request.COOKIES.get('email')
        # check if reviewer is assigned to review the paper
        try:
            reviewer = Reviewer.objects.get(
                user=cur_user_email, conference=conf_name)
        except:
            messages.error(
                request, f"Sorry, you are not a reviewer for {conf_name} conference")
            return redirect(conf_views.list_conferences)
        try:
            paper_submission = gsp_dao.get_paper_submission_by_title(
                title)
        except:
            messages.error(
                request, f"Paper {title} doesn't exist")
            return redirect(conf_views.list_conferences)
        try:
            assigned_reviewer_found = AssignedReviewers.objects.find(reviewer=reviewer,
                                                                     paper_submission=paper_submission)
        except:
            messages.error(
                request, f"Sorry, you are not a reviewer for {title} paper")
            return redirect(conf_views.list_conferences)
        # review submission deadline check
        conf = conference_dao.get_conference_by_name(conf_name)
        cur_time = timezone.now()
        if cur_time > conf.review_submission_deadline:
            messages.error(
                request, f"Sorry, review submission deadline has been elapsed")
            return redirect(conf_views.list_conferences)
        if request.method == "POST":
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.reviewer = reviewer_dao.get_reviewer_by_email_and_conf(
                    request.COOKIES.get('email'), conf_name)
                # paper_submissions = subject_area_submissions_dict[subject_area] = reviewer_dao.get_reviewer_by_email(
                #     request.COOKIES.get('email'))
                review.paper_submission = gsp_dao.get_paper_submission_by_title(
                    title)
                review.save()
                return redirect(conf_views.list_conferences)
        else:
            form = ReviewForm()
        return render(request, "make_review.html", {"is_logged_in": is_logged_in, "form": form})
    return redirect('/accounts/login')


def edit_review(request, conf_name, title):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        cur_user_email = request.COOKIES.get('email')
        # check if reviewer is assigned to review the paper
        try:
            reviewer = Reviewer.objects.get(
                user=cur_user_email, conference=conf_name)
        except:
            messages.error(
                request, f"Sorry, you are not a reviewer for {conf_name} conference")
            redirect(conf_views.list_conferences)
        try:
            paper_submission = gsp_dao.get_paper_submission_by_title(
                title)
        except:
            messages.error(
                request, f"Paper {title} doesn't exist")
            redirect(conf_views.list_conferences)
        try:
            assigned_reviewer_found = AssignedReviewers.objects.find(reviewer=reviewer,
                                                                     paper_submission=paper_submission)
        except:
            messages.error(
                request, f"Sorry, you are not a reviewer for {title} paper")
            redirect(conf_views.list_conferences)
        # review submission deadline check
        conf = conference_dao.get_conference_by_name(conf_name)
        cur_time = timezone.now()
        if cur_time > conf.review_submission_deadline:
            messages.error(
                request, f"Sorry, review submission deadline has been elapsed")
            redirect(conf_views.list_conferences)
        review = reviewer_dao.get_review_by_paper_title_and_reviewer(
            title, cur_user_email)
        if request.method == "POST":
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                review = form.save(commit=False)
                review.save()
                return redirect(conf_views.list_conferences)
            return render(request, "edit_review.html", {"is_logged_in": is_logged_in, "form": form})
        else:
            form = ReviewForm(instance=review)
        return render(request, "edit_review.html", {"is_logged_in": is_logged_in, "form": form})
    return redirect('/accounts/login')


def invite_reviewers(request, conf_name):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        cur_user_email = request.COOKIES.get('email')
        # check if user is CA of the conference or not
        conf_ca_emails = conference_dao.get_a_conference_ca_emails(conf_name)
        if cur_user_email not in conf_ca_emails:
            messages.error(
                request, f"Sorry, you are not a conference admin for {conf_name} conference")
            redirect(conf_views.list_conferences)
        # invite reviewers deadline check
        conf = conference_dao.get_conference_by_name(conf_name)
        cur_time = timezone.now()
        if (cur_time - conf.paper_submission_deadline).days > INVITE_REVIEWERS_DEADLINE:
            messages.error(
                request, f"Sorry, invite reviewer deadline has been elapsed")
            redirect(conf_views.list_conferences)
        if request.method == "POST":
            selected_users_emails = request.POST.getlist('checked_users')
            for selected_user_email in selected_users_emails:
                selected_user = accounts_dao.obtain_user_by_email(
                    selected_user_email)
                invited_reviewer = InvitedReviewers.objects.create(
                    user=selected_user, conference=conf)
                invited_reviewer.save()
            # TODO: send emails to invited reviewers
            return redirect(conf_views.list_conferences)
        else:
            all_conf_paper_submissions = conf.papersubmission_set.all()
            conf_users = set()
            for paper_submission in all_conf_paper_submissions:
                conf_users.add(paper_submission.main_author)
            conf_users = list(conf_users)
            return render(request, "invite_reviewers.html", {"is_logged_in": is_logged_in, "conf_users": conf_users})
    return redirect('/accounts/login')


def automated_reviewer_assignment(request, conf_name):
    # area chairs already separated from this reviewers' list
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        cur_user_email = request.COOKIES.get('email')
        # check if user is CA of the conference or not
        conf_ca_emails = conference_dao.get_a_conference_ca_emails(conf_name)
        if cur_user_email not in conf_ca_emails:
            messages.error(
                request, f"Sorry, you are not a conference admin for {conf_name} conference")
            return redirect(conf_views.list_conferences)
        if request.method == "POST":
            reviewers_list = reviewer_dao.get_all_reviewers_of_conf(conf_name)
            paper_submissions_list = gsp_dao.get_all_paper_submissions_of_conf(
                conf_name)

            conf_subject_areas = conference_dao.get_conference_subject_areas(
                conf_name)

            subject_area_reviewer_dict = {}
            for reviewer in reviewers_list:
                if reviewer.area_expertise not in subject_area_reviewer_dict:
                    subject_area_reviewer_dict[reviewer.area_expertise] = [
                        reviewer]
                else:
                    subject_area_reviewer_dict[reviewer.area_expertise].append(
                        reviewer)

            subject_area_submissions_dict = {}
            for paper_submission in paper_submissions_list:
                if paper_submission.subject_area not in subject_area_submissions_dict:
                    subject_area_submissions_dict[paper_submission.subject_area] = [
                        paper_submission]
                else:
                    subject_area_submissions_dict[paper_submission.subject_area].append(
                        paper_submission)

            # reviewer assignment done for each subject area independently
            print(conf_subject_areas)
            for subject_area in conf_subject_areas:
                print(subject_area)
                reviewers = subject_area_reviewer_dict[subject_area]
                paper_submissions = subject_area_submissions_dict[subject_area]
                paper_reviewer_mapping = assign_reviewers(
                    reviewers, paper_submissions)

                for paper_submission in paper_reviewer_mapping.keys():
                    assigned_reviewers = paper_reviewer_mapping[paper_submission]
                    for assigned_reviewer in assigned_reviewers:
                        assigned_reviewer_obj = AssignedReviewers.objects.create(
                            reviewer=assigned_reviewer, paper_submission=paper_submission)
                        assigned_reviewer_obj.save()
            
            messages.info(
                request, f"Automated reviewer assignment succesfully completed for {conf_name} conference")
            return redirect(conf_views.list_conferences)
        else:
            return render(request, "automated_reviewer_assignment.html", {'is_logged_in': is_logged_in})
    return redirect('/accounts/login')


def manual_reviewer_assignment(request, conf_name):
    is_logged_in = utils.check_login(request)
    if is_logged_in:
        cur_user_email = request.COOKIES.get('email')
        # check if user is CA of the conference or not
        conf_ca_emails = conference_dao.get_a_conference_ca_emails(conf_name)
        if cur_user_email not in conf_ca_emails:
            messages.error(
                request, f"Sorry, you are not a conference admin for {conf_name} conference")
            redirect(conf_views.list_conferences)
        if request.method == "POST":
            pass
        else:
            all_reviewers = reviewer_dao.get_all_reviewers_of_conf(conf_name)
            all_paper_submissions = gsp_dao.get_all_paper_submissions_of_conf(
                conf_name)
            context = {
                "all_reviewers": all_reviewers,
                "all_paper_submissions": all_paper_submissions,
            }
            return render(request, "manual_reviewer_assignment.html", context)
    return redirect('/accounts/login')
