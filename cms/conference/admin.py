from django.contrib import admin
from .models import Conference


class PortalAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Conference, PortalAdmin)
