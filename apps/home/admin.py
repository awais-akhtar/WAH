
from django.contrib import admin

from .models import *
# Register your models here.

class SessionAdmin(admin.ModelAdmin):
    list_display = ['manufacturer', 'data_limit', 'location','isp']
    # readonly_fields = ['imei','msisdn']
    list_filter = ('location', 'isp')
    search_fields = ('location', 'isp')

admin.site.register(device_inventory, SessionAdmin)
# admin.site.register(location)
# admin.site.register(type)
# admin.site.register(isp)
# admin.site.register(data_limit)

admin.site.register(AddRequest)