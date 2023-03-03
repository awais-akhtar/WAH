from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class employee_data(models.Model):
    StartTime = models.DateField()
    LoginId = models.IntegerField()

    def __str__(self):
        return str(self.LoginId)
    class Meta:  
        db_table = "employee_data"
        verbose_name = 'employee_data'
        verbose_name_plural = 'employee_data'