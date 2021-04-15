from heapq import heapify, heappop, heappush
from .constants import MIN_PAPER_REVIEW_LIMIT


def assign_reviewers(reviewers, paper_submissions):
    paper_reviewer_mapping = {}
    reviewer_paper_mapping = {}
    paper_review_limit_heap = heapify([
        [MIN_PAPER_REVIEW_LIMIT, paper_submission] for paper_submission in paper_submissions])
    # assigning each reviewer a set of papers according to his/her paper review limit
    for reviewer in reviewers:
        max_review_limit = min(
            reviewer.paper_review_limit, len(paper_review_limit_heap))
        while len(paper_review_limit_heap) > 0 and max_review_limit > 0:
            paper_rem_reviews, paper_submission = heappop(
                paper_review_limit_heap)

            # assign the paper to reviewer
            if paper_submission not in paper_reviewer_mapping:
                paper_reviewer_mapping[paper_submission] = [reviewer.email]
            else:
                paper_reviewer_mapping[paper_submission].append(reviewer.email)
            if paper_submission not in reviewer_paper_mapping:
                reviewer_paper_mapping[reviewer.email] = [paper_submission]
            else:
                reviewer_paper_mapping[reviewer.email].append(paper_submission)
            paper_rem_reviews -= 1
            if paper_rem_reviews > 0:
                heappush(paper_review_limit_heap,
                         (paper_rem_reviews, paper_submission))
            reviewer.paper_limit -= 1
            reviewer.save()

            max_review_limit = min(
                reviewer.paper_review_limit, len(paper_review_limit_heap))

    return paper_reviewer_mapping
