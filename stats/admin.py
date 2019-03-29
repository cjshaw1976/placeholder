from django.contrib import admin

from .models import DataLog, LocationLog, VisitorLog

admin.site.register(DataLog)
admin.site.register(LocationLog)
admin.site.register(VisitorLog)
