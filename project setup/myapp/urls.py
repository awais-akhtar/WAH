from django.urls import path
from .import views 
from django.contrib.auth import views as auth_view
from django.contrib import admin


admin.site.site_header = "Portal Admin"
admin.site.site_title = "Portal Admin"
admin.site.index_title = "Welcome to Portal Administration"

urlpatterns = [
    path('',views.home,name="home"),
]

