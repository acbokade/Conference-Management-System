import numpy as np

from accounts.models import User
from gsp.models import PaperSubmission, AuthorResponseSubmission
from .models import AreaChair, AssignedAreaChairs

from collections import defaultdict


def get_reviewer_constraints(conf_name):

    conf_area_chairs = AreaChair.objects.get(conference__name=conf_name)
    ac_email2object = get_ac_email2object(conf_area_chairs)
    conf_area_chairs = list(conf_area_chairs)

    ac2subject = defaultdict(list)
    subject2ac = defaultdict(list)

    reviewer_remaining_count = dict()

    for area_chair in conf_area_chairs:
        reviewer_details = Reviewer.objects.get(user=area_chair, conference__name=conf_name)
        subjects = reviewer_details.area_expertise
        subjects = subjects.split(',')
        ac2subject[area_chair.email] = subjects
        for subject in subjects:
            subject2ac[subject].append(area_chair)

    return ac2subject, subject2ac, ac_email2object

def get_acs(subject2ac, paper_subject_area, acs_not_allowed):

    candidates = subject2ac[paper_subject_area] - acs_not_allowed
    
    if len(candidates) == 0:
        for i in range(50):
            candicates = subject2ac[np.random.choice(subject2ac.keys())] - acs_not_allowed
            if len(candicates) > 0:
                return np.random.choice(candidates)
            
        return None
    else:
        return np.random.choice(candidates)

def get_ac_email2object(query):

    email2object = dict()
    for q in query:
        email2object[q.email] = q
    return email2object

def assign_area_chairs(conf_name):

    ac2subject, subject2ac, ac_email2object = get_reviewer_constraints(conf_name)

    conf_papers = PaperSubmission.objects.get(conference__name=conf_name)
    for conf_paper in conf_papers:
        paper_subject_areas = conf_paper.subject_areas
        paper_subject_areas = paper_subject_areas.split(',')

        ac = None
        for paper_subject_area in paper_subject_areas:

            acs_not_allowed = list()
            ac = get_acs(ac2subject, paper_subject_area, acs_not_allowed)

            if ac is not None:
                AssignedAreaChairs(area_chair=ac_email2object[ac], paper_submission=conf_paper).save()
        
        assert ac is not None

    
    return redirect('/conferences/list_conferences')