from django.contrib import admin
from .models import *
# Register your models here.

class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']
    list_filter = ('title', 'description')
    search_fields = ('title', 'description')

admin.site.register(employee_data, SessionAdmin)