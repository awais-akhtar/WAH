from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class device_inventory(models.Model):
    location = models.CharField(max_length=25)
    type = models.CharField(max_length=25)
    isp = models.CharField(max_length=25)
    data_limit = models.CharField(max_length=25)
    manufacturer = models.CharField(max_length=25)
    device_model = models.CharField(max_length=20)
    imei = models.CharField(max_length=25)
    device_status = models.CharField(max_length=25)
    instock_date = models.DateTimeField(auto_now_add=True)
    punched_by = models.CharField(max_length=20)
    remarks = models.CharField(max_length=200)
    status = models.CharField(max_length=50, default='NotAssigned')
    assigned_to = models.CharField(null=True, blank=True, max_length=20)

    def __str__(self):
        return str(self.location)
    class Meta:
        db_table = "device_inventory"
        verbose_name = 'device_inventory'
        verbose_name_plural = 'device_inventory'


class sim_inventory(models.Model):
    msisdn = models.CharField(max_length=25)
    sim_card = models.CharField(max_length=30)
    location = models.CharField(max_length=25)
    isp = models.CharField(max_length=25)
    data_limit = models.CharField(max_length=25)
    instock_date = models.DateTimeField(auto_now_add=True)
    added_by = models.CharField(max_length=20)
    sim_status = models.CharField(max_length=25)
    status = models.CharField(max_length=50, default='NotAssigned')
    assigned_to = models.CharField(null=True, blank=True, max_length=20)

    def __str__(self):
        return str(self.sim_card)
    class Meta:
        db_table = "sim_inventory"
        verbose_name = 'sim_inventory'
        verbose_name_plural = 'sim_inventory'

class AddRequest(models.Model):
    ticket_id = models.CharField(max_length=20, unique=True, editable=False)
    employee_id = models.CharField(max_length=20)
    employee_email = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    request_date = models.DateTimeField(auto_now_add=True)
    request_by = models.CharField(max_length=40)
    isp = models.CharField(max_length=20)
    approved_date = models.DateTimeField(null=True, blank=True)
    approved_by = models.CharField(max_length=20, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    assigned_device_imei = models.CharField(max_length=50, null=True, blank=True)
    # Generate a unique ticket ID on save
    def save(self, *args, **kwargs):
        if not self.ticket_id:
            self.ticket_id =str(uuid.uuid4().fields[-1])[:6]
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = 'Add_Request'
        verbose_name_plural = 'Add_Requests'
    def __str__(self):
        return self.ticket_id

class DeviceAllocation(models.Model):
    assigned_device = models.ForeignKey(device_inventory, on_delete=models.CASCADE)
    assigned_sim = models.ForeignKey(sim_inventory, on_delete=models.CASCADE)
    ticket = models.ForeignKey(AddRequest, on_delete=models.CASCADE)
    allocated_date = models.DateTimeField(auto_now_add=True)
    allocated_by = models.CharField(max_length=20)
    remarks = models.CharField(max_length=300)

    class Meta:
        verbose_name = 'Device_Allocation'
        verbose_name_plural = 'Device_Allocations'

    def __str__(self):
        return f"{self.assigned_device} - {self.ticket} - {self.allocated_date}"




# class assigned_device(models.Model):
#     ticket_id = models.CharField(max_length=50)
#     employee_name = models.CharField(max_length=50)
#     employee_id = models.CharField(max_length=20)
#     employee_email = models.CharField(max_length=30)
#     request_by = models.CharField(max_length=40)
#     request_date = models.DateTimeField()
#     approved_by = models.CharField(max_length=20)
#     approved_date = models.DateTimeField(auto_now_add=True)
#     is_approved = models.BooleanField(default=False)
#     assigned_device_id = models.CharField(max_length=50)
#     location = models.CharField(max_length=25)
#     type = models.CharField(max_length=25)
#     isp = models.CharField(max_length=25)
#     data_limit = models.CharField(max_length=25)
#     manufacturer = models.CharField(max_length=25)
#     device_model = models.CharField(max_length=20)
#     imei = models.CharField(max_length=25)
#     msisdn = models.CharField(max_length=25)
#     sim_card = models.CharField(max_length=30)
#     device_status = models.CharField(max_length=25)
#     instock_date = models.DateTimeField()
#     punched_by = models.CharField(max_length=20)
#     remarks = models.CharField(max_length=200)
#     status = models.CharField(max_length=50, default='Assigned')



# class DeviceHistory(models.Model):
#     device = models.ForeignKey(device_inventory, on_delete=models.CASCADE)
#     updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     updated_date = models.DateTimeField(default=timezone.now)
#     location = models.CharField(max_length=25)
#     type = models.CharField(max_length=25)
#     isp = models.CharField(max_length=25)
#     data_limit = models.CharField(max_length=25)
#     manufacturer = models.CharField(max_length=25)
#     device_model = models.CharField(max_length=20)
#     imei = models.CharField(max_length=25)
#     msisdn = models.CharField(max_length=25)
#     sim_card = models.CharField(max_length=30)
#     device_status = models.CharField(max_length=25)
#     remarks = models.CharField(max_length=200)

#     class Meta:
#         db_table = "device_history"
#         verbose_name = 'device_history'
#         verbose_name_plural = 'device_history'