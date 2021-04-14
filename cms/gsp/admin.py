from django.contrib import admin
from .models import PaperSubmission #, CamPosSubmission, AuthorResponseSubmission

# Register your models here.
admin.site.register(PaperSubmission)
# admin.site.register(AuthorResponseSubmission)
# admin.site.register(CamPosSubmission)