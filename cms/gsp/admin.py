from django.contrib import admin
from .models import AuthorResponseSubmission, PaperSubmission, CamPosSubmission

# Register your models here.
admin.site.register(AuthorResponseSubmission)
admin.site.register(PaperSubmission)
admin.site.register(CamPosSubmission)