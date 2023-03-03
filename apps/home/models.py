from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class device_inventory(models.Model):
    location = models.CharField(max_length=25)
    type = models.CharField(max_length=25)
    isp = models.CharField(max_length=25)
    data_limit = models.CharField(max_length=25)
    manufacturer = models.CharField(max_length=25)
    device_model = models.CharField(max_length=20)
    imei = models.CharField(max_length=25)
    msisdn = models.CharField(max_length=25)
    sim_card = models.CharField(max_length=30)
    device_status = models.CharField(max_length=25)
    instock_date = models.DateTimeField(auto_now_add=True)
    punched_by = models.CharField(max_length=20)
    remarks = models.CharField(max_length=200)
    def __str__(self):
        return str(self.location)
    class Meta:  
        db_table = "device_inventory"
        verbose_name = 'device_inventory'
        verbose_name_plural = 'device_inventory'

class DeviceHistory(models.Model):
    device = models.ForeignKey(device_inventory, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_date = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=25)
    type = models.CharField(max_length=25)
    isp = models.CharField(max_length=25)
    data_limit = models.CharField(max_length=25)
    manufacturer = models.CharField(max_length=25)
    device_model = models.CharField(max_length=20)
    imei = models.CharField(max_length=25)
    msisdn = models.CharField(max_length=25)
    sim_card = models.CharField(max_length=30)
    device_status = models.CharField(max_length=25)
    remarks = models.CharField(max_length=200)

    class Meta:
        db_table = "device_history"
        verbose_name = 'device_history'
        verbose_name_plural = 'device_history'

# class device_inventory(models.Model):
#     manufacturer = models.CharField(max_length=20)
#     device_model = models.CharField(max_length=20)
#     imei = models.IntegerField()
#     msisdn = models.IntegerField()
#     sim_card = models.CharField(max_length=30)
#     device_status = models.CharField(max_length=20)
#     instock_date = models.DateTimeField(auto_now_add=True)
#     punched_by = models.CharField(max_length=20)
#     location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True, blank=True)
#     type = models.ForeignKey('Type', blank=True, on_delete=models.SET_NULL, null=True)
#     isp = models.ForeignKey('Isp', on_delete=models.SET_NULL, null=True, blank=True)
#     data_limit = models.ForeignKey('Data_limit', on_delete=models.SET_NULL, null=True, blank=True)
#     class Meta:  
#         db_table = "device_inventory"
#         verbose_name = 'device_inventory'
#         verbose_name_plural = 'device_inventory'

# class location(models.Model):
#     location_CATEGORIES=(
#         ('LHR', ('LHR')),
#         ('KHR', ('KHR')),
#         ('ISL', ('ISL')),
#     )
#     name = models.CharField(max_length=20, blank=True, null=True, choices=location_CATEGORIES)
#     def __str__(self):
#         return self.name
#     class Meta:
#         ordering = ["-name"]


# class type(models.Model):
#     type_CATEGORIES=(
#         ('No Info Available', ('No Info Available')),
#         ('MIFI', ('MIFI')),
#         ('CAT6', ('CAT6')),
#         ('CharJi', ('CharJi')),
#         ('Router', ('Router')),
#         ('Wingle', ('Wingle')),
#         ('Bolt/Bolt+', ('Bolt/Bolt+')),
#         ('SIM Only', ('SIM Only')),
#     )
#     name = models.CharField(max_length=20, blank=True, null=True, choices=type_CATEGORIES, default=1)
#     location = models.ForeignKey(
#         'Location', on_delete=models.CASCADE, blank=True, null=True)
#     def __str__(self):
#         return self.name
#     class Meta:
#         ordering = ["-name"]

# class isp(models.Model):
#     isp_CATEGORIES=(
#         ('No Info Available', ('No Info Available')),
#         ('Telenor', ('Telenor')),
#         ('Zong', ('Zong')),
#         ('Jazz', ('Jazz')),
#         ('PTCL', ('PTCL')),
#     )
#     name = models.CharField(max_length=20, blank=True, null=True, choices=isp_CATEGORIES, default=1)
#     type = models.ForeignKey(
#         'Type', on_delete=models.CASCADE, blank=True, null=True)
#     def __str__(self):
#         return self.name
#     class Meta:
#         ordering = ["-name"]

# class data_limit(models.Model):
#     data_limit_CATEGORIES=(
#         ('No Info Available', ('No Info Available')),
#         ('75GB', ('75GB')),
#         ('85GB', ('85GB')),
#         ('100GB', ('100GB')),
#         ('150GB', ('150GB')),
#         ('160GB', ('160GB')),
#         ('275GB', ('275GB')),
#     )
#     name = models.CharField(max_length=20, blank=True, null=True, choices=data_limit_CATEGORIES, default=1)
#     isp = models.ForeignKey(
#         'Isp', on_delete=models.CASCADE, blank=True, null=True)
#     def __str__(self):
#         return self.name
#     class Meta:
#         ordering = ["-name"]



class AddRequest(models.Model):
    # name = models.CharField(max_length=255)
    # email = models.EmailField()
    # current_designation = models.CharField(max_length=255)
    # joining_date = models.DateField()
    # department = models.CharField(max_length=255)
    # location = models.CharField(max_length=255)
    # legal_entity = models.CharField(max_length=255)
    # team = models.CharField(max_length=255)
    # supervisor = models.CharField(max_length=255)
    # supervisor_email = models.EmailField()
    # lev1_mgr = models.CharField(max_length=255)
    # lev1_mgr_email = models.EmailField()
    # lev2_mgr = models.CharField(max_length=255)
    # lev2_mgr_email = models.EmailField()

    employee_id = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    request_date = models.DateTimeField(auto_now_add=True)
    request_by = models.CharField(max_length=40)
    device_type = models.CharField(max_length=20)
    approved_date = models.DateTimeField(null=True, blank=True)
    approved_by = models.CharField(max_length=20, null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Add_Request'
        verbose_name_plural = 'Add_Requests'

    def __str__(self):
        return self.user_name