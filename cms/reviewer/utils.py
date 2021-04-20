from heapq import heapify, heappop, heappush
from .constants import MIN_PAPER_REVIEW_LIMIT
import pandas as pd
from reviewer import data_access_layer as reviewer_dao
from conference import data_access_layer as conference_dao
from gsp import data_access_layer as gsp_dao


class RemReviewsAndPaperPair(object):
    def __init__(self, rem_reviews, paper):
        self.rem_reviews = rem_reviews
        self.paper = paper

    def __repr__(self):
        return f"({self.rem_reviews}, {self.paper.title})"

    def __lt__(self, other):
        return self.rem_reviews > other.rem_reviews


def check_paper_conflicts(reviewer, paper_submission):
    reviewer_email = reviewer.user_id
    if reviewer_email == paper_submission.main_author_id:
        return False
    for other_authors in paper_submission.authors:
        if reviewer_email == other_authors.user_id:
            return False
    return True


def assign_reviewers(reviewers, paper_submissions):
    # TODO: handle conflicts
    paper_reviewer_mapping = {}
    reviewer_paper_mapping = {}
    paper_rem_reviews_heap = [
        RemReviewsAndPaperPair(MIN_PAPER_REVIEW_LIMIT, paper_submission) for paper_submission in paper_submissions]
    heapify(paper_rem_reviews_heap)
    # assigning each reviewer a set of papers according to his/her paper review limit
    for reviewer in reviewers:
        iter_no = 0
        # remove next line after testing
        reviewer_paper_review_limit = reviewer.paper_review_limit
        max_review_limit = min(
            reviewer_paper_review_limit, len(paper_rem_reviews_heap))
        while len(paper_rem_reviews_heap) > 0 and max_review_limit > 0:
            rem_reviews_paper_pair = heappop(
                paper_rem_reviews_heap)
            paper_rem_reviews, paper_submission = rem_reviews_paper_pair.rem_reviews, rem_reviews_paper_pair.paper

            # to prevent infinite looping
            if iter_no > len(paper_rem_reviews_heap):
                break

            # checking conflicts
            if check_paper_conflicts(reviewer, paper_submission):
                heappush(paper_rem_reviews_heap,
                         RemReviewsAndPaperPair(paper_rem_reviews, paper_submission))
                continue

            iter_no += 1
            # assign the paper to reviewer
            if paper_submission not in paper_reviewer_mapping:
                paper_reviewer_mapping[paper_submission] = [
                    reviewer]
            else:
                paper_reviewer_mapping[paper_submission].append(
                    reviewer)
            if paper_submission not in reviewer_paper_mapping:
                reviewer_paper_mapping[reviewer] = [
                    paper_submission]
            else:
                reviewer_paper_mapping[reviewer].append(
                    paper_submission)
            paper_rem_reviews -= 1
            if paper_rem_reviews > 0:
                heappush(paper_rem_reviews_heap,
                         RemReviewsAndPaperPair(paper_rem_reviews, paper_submission))
            reviewer_paper_review_limit -= 1
            # reviewer.save()

            # max_review_limit = min(
            #     reviwer_paper_review_limit, len(paper_rem_reviews_heap))
            max_review_limit -= 1
            print(paper_rem_reviews_heap, reviewer.user.name,
                  reviewer_paper_review_limit)
    print(paper_reviewer_mapping)
    return paper_reviewer_mapping


# def prepare_paper_assignment_file(all_paper_submissions, conf_name):
#     all_titles = [
#         paper_submission.title for paper_submission in all_paper_submissions]
#     column_names = [f"Reviewer_{i}" for i in range(MIN_PAPER_REVIEW_LIMIT)]
#     df = pd.DataFrame(index=all_titles, columns=column_names)
#     df = df.fillna('')
#     for i in range(len(all_paper_submissions)):
#         cur_paper = all_paper_submissions[i]
#         assigned_reviewers_list = list(
#             cur_paper.assignedreviewers_set.all())
#         for j in range(len(assigned_reviewers_list)):
#             df.iloc[i, j] = assigned_reviewers_list[j].reviewer.user_id

#     print(df)
#     file_name = f"{conf_name}_Paper_assignment.tsv"
#     paper_assignment_file = df.to_csv(file_name, sep="\t")
#     return paper_assignment_file


# def prepare_reviewer_details_file(all_reviewers, conf_name):
#     column_names = ["Reviewer_email", "Review_limit"]
#     data = [[reviewer.user_id, reviewer.paper_review_limit]
#             for reviewer in all_reviewers]
#     df = pd.DataFrame(data=data, columns=column_names)
#     file_name = f"{conf_name}_Reviewer_details.tsv"
#     reviewer_details_file = df.to_csv(file_name, sep="\t")
#     return reviewer_details_file


def sufficient_reviewers_check_of_conf(conf_name):
    conf_subject_areas = conference_dao.get_conference_subject_areas(
        conf_name)
    for conf_subject_area in conf_subject_areas:
        n_reviewers = reviewer_dao.get_n_reviewers_of_conf_and_subject_area(
            conf_name, conf_subject_area)
        n_paper_submissions = gsp_dao.get_number_of_papers_of_a_conf_in_an_area(
            conf_name, conf_subject_area)
        required_invitations = n_paper_submissions//MIN_PAPER_REVIEW_LIMIT
        if n_reviewers < required_invitations or n_reviewers < MIN_PAPER_REVIEW_LIMIT:
            return False
    return True
