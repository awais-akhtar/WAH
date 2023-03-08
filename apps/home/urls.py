from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    # path('', views.index, name='home'),
    path('form/', views.assignment, name='form'),
    path('request_data/', views.request_data, name='request_data'),
    path('add_request/', views.add_request, name='add_request'),
    path('request_status/', views.request_status, name='request_status'),
    path('stock/', views.stock, name='stock'),
    path('stock_record/', views.stock_record, name='stock_record'),
    path('find_isp/',views.find_isp,name='find_isp'),
    path('findQuota/',views.findQuota,name='findQuota'),
    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),
    # path('create_device/', views.create_device, name='create_device'),
    path('filter-dropdown/', views.filter_dropdown, name='filter_dropdown'),
    path('edit/<pk>', views.edit_device, name='edit'),
    path('delete/<pk>', views.delete_device, name='delete'),
    path('get_device_data/<int:id>', views.get_device_data, name='get_device_data'),
    path('get_request_data/<int:id>', views.get_request_data, name='get_request_data'),
    path('update_device_data/', views.update_device_data, name='update_device_data'),
    # path('update_device_data/<int:id>/', views.update_device_data, name='update_device_data')

    path('test/', views.test, name='test'),

    path('approve_request/', views.approve_request, name='approve_request'),
    path('reject_request/', views.reject_request, name='reject_request'),

]
