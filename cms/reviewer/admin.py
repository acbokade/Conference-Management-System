from django.contrib import admin
from .models import Reviewer, Review, InvitedReviewers, AssignedReviewers

admin.site.register(Reviewer)
admin.site.register(Review)
admin.site.register(InvitedReviewers)
admin.site.register(AssignedReviewers)
