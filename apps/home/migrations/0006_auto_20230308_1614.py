# Generated by Django 3.2.16 on 2023-03-08 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_addrequest_ticket_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceAllocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allocated_date', models.DateTimeField(auto_now_add=True)),
                ('allocated_by', models.CharField(max_length=20)),
                ('assigned_device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.device_inventory')),
            ],
            options={
                'verbose_name': 'Device_Allocation',
                'verbose_name_plural': 'Device_Allocations',
            },
        ),
        migrations.AddField(
            model_name='addrequest',
            name='employee_email',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='addrequest',
            name='ticket_id',
            field=models.CharField(editable=False, max_length=20, unique=True),
        ),
        migrations.DeleteModel(
            name='DeviceHistory',
        ),
        migrations.AddField(
            model_name='deviceallocation',
            name='ticket_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.addrequest'),
        ),
    ]