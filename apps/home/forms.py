# from django import forms
# from .models import device_inventory, location, type, isp, data_limit

# class CreateInventoryForm(forms.ModelForm):
#     class Meta:
#         model = device_inventory
#         fields = ['manufacturer', 'device_model', 'imei', 'msisdn', 'sim_card', 'device_status', 'location', 'type', 'isp', 'data_limit']
#         widgets = {
#             'location': forms.Select(attrs={'class': 'form-control'}),
#             'type': forms.Select(attrs={'class': 'form-control'}),
#             'isp': forms.Select(attrs={'class': 'form-control'}),
#             'data_limit': forms.Select(attrs={'class': 'form-control'}),
#         }

        
# class DeviceInventoryForm(forms.ModelForm):
#     manufacturer = forms.CharField(max_length=20)
#     device_model = forms.CharField(max_length=20)
#     imei = forms.IntegerField()
#     msisdn = forms.IntegerField()
#     sim_card = forms.CharField(max_length=30)
#     device_status = forms.CharField(max_length=20)
#     punched_by = forms.CharField(max_length=20)
#     location = forms.ModelChoiceField(queryset=location.objects.all(), empty_label="Select location", required=True)
#     type = forms.ModelChoiceField(queryset=type.objects.all(), empty_label="Select type", required=False)
#     isp = forms.ModelChoiceField(queryset=isp.objects.none(), empty_label="Select ISP", required=False)
#     data_limit = forms.ModelChoiceField(queryset=data_limit.objects.none(), empty_label="Select data limit", required=False)

#     class Meta:
#         model = device_inventory
#         fields = ['manufacturer', 'device_model', 'imei', 'msisdn', 'sim_card', 'device_status', 'punched_by', 'location', 'type', 'isp', 'data_limit']

#     def __init__(self, *args, **kwargs):
#         super(DeviceInventoryForm, self).__init__(*args, **kwargs)
#         self.fields['type'].queryset = type.objects.none()
#         self.fields['isp'].queryset = isp.objects.none()
#         self.fields['data_limit'].queryset = data_limit.objects.none()

#         if 'location' in self.data:
#             try:
#                 location_id = int(self.data.get('location'))
#                 self.fields['type'].queryset = type.objects.filter(location_id=location_id).order_by('name')
#             except (ValueError, TypeError):
#                 pass
#         elif self.instance.pk:
#             self.fields['type'].queryset = self.instance.location.type_set.order_by('name')

#         if 'type' in self.data:
#             try:
#                 type_id = int(self.data.get('type'))
#                 self.fields['isp'].queryset = isp.objects.filter(type_id=type_id).order_by('name')
#             except (ValueError, TypeError):
#                 pass
#         elif self.instance.pk:
#             self.fields['isp'].queryset = self.instance.type.isp_set.order_by('name')

#         if 'isp' in self.data:
#             try:
#                 isp_id = int(self.data.get('isp'))
#                 self.fields['data_limit'].queryset = data_limit.objects.filter(isp_id=isp_id).order_by('name')
#             except (ValueError, TypeError):
#                 pass
#         elif self.instance.pk:
#             self.fields['data_limit'].queryset = self.instance.isp.data_limit_set.order_by('name')
