from heapq import heapify, heappop, heappush
from .constants import MIN_PAPER_REVIEW_LIMIT


class RemReviewsAndPaperPair(object):
    def __init__(self, rem_reviews, paper):
        self.rem_reviews = rem_reviews
        self.paper = paper

    def __repr__(self):
        return f"({self.rem_reviews}, {self.paper.title})"

    def __lt__(self, other):
        return self.rem_reviews > other.rem_reviews


def assign_reviewers(reviewers, paper_submissions):
    paper_reviewer_mapping = {}
    reviewer_paper_mapping = {}
    paper_rem_reviews_heap = [
        RemReviewsAndPaperPair(MIN_PAPER_REVIEW_LIMIT, paper_submission) for paper_submission in paper_submissions]
    heapify(paper_rem_reviews_heap)
    # assigning each reviewer a set of papers according to his/her paper review limit
    for reviewer in reviewers:
        # remove next line after testing
        reviwer_paper_review_limit = reviewer.paper_review_limit
        max_review_limit = min(
            reviwer_paper_review_limit, len(paper_rem_reviews_heap))
        while len(paper_rem_reviews_heap) > 0 and max_review_limit > 0:
            rem_reviews_paper_pair = heappop(
                paper_rem_reviews_heap)
            paper_rem_reviews, paper_submission = rem_reviews_paper_pair.rem_reviews, rem_reviews_paper_pair.paper

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
            reviwer_paper_review_limit -= 1
            # reviewer.save()

            # max_review_limit = min(
            #     reviwer_paper_review_limit, len(paper_rem_reviews_heap))
            max_review_limit -= 1
            print(paper_rem_reviews_heap, reviewer.user.name,
                  reviwer_paper_review_limit)
    print("***************")
    print(paper_reviewer_mapping)
    return paper_reviewer_mapping
