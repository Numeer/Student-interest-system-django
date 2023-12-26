from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Student)
admin.site.register(ActivityLog)
admin.site.register(Permission)

@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display=('name',)
    search_fields=('name',)
