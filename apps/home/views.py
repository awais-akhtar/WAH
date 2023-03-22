from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
import requests
import json
from datetime import date, datetime
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .forms import SetPasswordForm
from rest_framework.views import APIView
from rest_framework.response import Response

# from .forms import DeviceInventoryForm, CreateInventoryForm

# def create_device(request):
#     form = CreateInventoryForm()
#     if request.method == 'POST':
#         form = CreateInventoryForm(request.POST)
#         if form.is_valid():
#             device = form.save(commit=False)
#             device.save()
#             form.save_m2m()
#     return render(request, 'home/create_device.html', {'form': form})

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format = None):
        labels = [
            'Requests',
            'Sim Cards',
            'Devices',
            ]
        request_unapproved = AddRequest.objects.filter(is_approved=False).count()
        sim_stock = sim_inventory.objects.filter(status__contains = 'NotAssigned').count()
        device_stock = device_inventory.objects.filter(status__contains = 'NotAssigned').count()
        chartLabel = " data"
        chartdata = [ request_unapproved, sim_stock, device_stock]
        data ={
                "labels":labels,
                "chartLabel":chartLabel,
                "chartdata":chartdata,
             }
        return Response(data)
    
class ChartData2(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format = None):
        labels = [
            'Requests',
            'Sim Cards',
            'Devices',
            ]
        request_approved = AddRequest.objects.filter(is_approved=True).count()
        sim_stock = sim_inventory.objects.filter(status__contains = 'Assigned').count()
        device_stock = device_inventory.objects.filter(status__contains = 'Assigned').count()
        chartLabel = " data"
        chartdata = [request_approved, sim_stock, device_stock]
        data ={
                "labels":labels,
                "chartLabel":chartLabel,
                "chartdata":chartdata,
             }
        return Response(data)



@login_required
def index(request):
    request_approved = AddRequest.objects.filter(is_approved=True).count()
    request_unapproved = AddRequest.objects.filter(is_approved=False).count()
    sim_stock = sim_inventory.objects.filter(status__contains = 'NotAssigned').count()
    device_stock = device_inventory.objects.filter(status__contains = 'NotAssigned').count()
    us = User.objects.filter(is_active=True).values()
    print(us)
    context ={
        'us': us,
        'request_approved' : request_approved,
        'request_unapproved' : request_unapproved,
        'device_stock' : device_stock,
        'sim_stock' : sim_stock,
        'segment': 'index'
    }
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

# profile page
def profile(request):
    user=request.user
    if request.method=='POST':
        user.first_name=request.POST['firstname']
        user.last_name=request.POST['lastname']
        user.email=request.POST['email']
        user.save()
        messages.info(request,"Updated Successfully")
        return redirect('profile')
    context={
        'segment': 'profile'
    }
    return render(request,"home/profile.html", context)


def password_change(request):
    if request.user.is_authenticated or request.user.is_superuser or request.user.is_staff:
        try:
                user = request.user
                if request.method == 'POST':
                                form = SetPasswordForm(user, request.POST)
                                if form.is_valid():
                                                form.save()
                                                messages.success(request, "Your password has been changed")
                                                return redirect('profile')
                                else:
                                        for error in list(form.errors.values()):
                                                messages.error(request, error)
                form = SetPasswordForm(user)
                return render(request, 'password_reset_confirm.html', {'form': form})
        except:
                messages.warning(request,"An Error is occurred!")
                return redirect("/")
    else:
        return HttpResponse("You are not Authorized")

def add_request(request):
    if request.method == "POST":
        text = request.POST.get('text')
        print(text)
        id = int(text)
        if AddRequest.objects.filter(Q(is_approved=False) & Q(employee_id=id)).exists():
            messages.error(request, "A Request with the same details already exists in the database.")
            db = AddRequest.objects.filter(Q(is_approved=False) & Q(employee_id=id)).values()
            print("details already exists=======", db)
            context={
                'unapproved_requests': db
            }
            return render(request, "home/add_request.html", context)
        elif AddRequest.objects.filter(Q(is_approved=True) & Q(employee_id=id)).exists():
            messages.error(request, "A Request with the same details already Approved.")
            db2 = AddRequest.objects.filter(Q(is_approved=True) & Q(employee_id=id))
            print("Same details with user is existing in database=====", db2)
            request_device = device_inventory.objects.get(assigned_to=id)
            print("the assigned device details=========", request_device)
            context={
                'approved_requests': db2,
                'request_device': request_device
            }
            return render(request, "home/add_request.html", context)
        else:
            api_key = 'Basic Att3nd@nc3'
            api_url = f'http://portal.ibexglobal.com/AttendancePointsService/api/values/getemployeehierarchy?portalid={id}'
            headers = {
            'Authorization': api_key}
            response = requests.get(api_url, headers=headers)
            # print(json.loads(response.text))
            api_key2 = 'Basic Tk$PkD@taMast3r'
            # mm/dd/y
            d3 = date.today()
            checktoday = d3.strftime("%m/%d/%y")
            print("checktoday =", checktoday)
            api_url2 = f'http://portal.ibexglobal.com:88/AttendancePointsService/api/values/GetLeavesBalance?portalid={id}&year={checktoday}'
            headers2 = {
            'Authorization': api_key2}
            responsestatus = requests.get(api_url2, headers=headers2)
            dd= json.loads(responsestatus.text)
            data2=dd['data']['EmployeeStatus']
            print(data2)
            ss= json.loads(response.text)
            data=ss['data']['PointsData']
            print(data)
            context = {'obj':data, 'data2':data2}
            return render(request, "home/add_request.html", context)
    return render(request, "home/add_request.html")



def request_status(request):
    unapproved_requests = AddRequest.objects.filter(is_approved=False).values()
    approved_requests = AddRequest.objects.filter(is_approved=True).values()
    context = {
        'unapproved_requests': unapproved_requests,
        'approved_requests': approved_requests,
    }
    return render(request, "home/request_status.html", context)



def request_data(request):
    if request.method == "POST":
        employee_id = request.POST['employee_id']
        # cnic = request.POST['cnic']
        # number = request.POST['number']
        isp = request.POST['isp']
        id = int(employee_id)
        api_key = 'Basic Att3nd@nc3'
        api_url = f'http://portal.ibexglobal.com/AttendancePointsService/api/values/getemployeehierarchy?portalid={id}'
        headers = {
        'Authorization': api_key}
        response = requests.get(api_url, headers=headers)
        ss= json.loads(response.text)
        data=ss['data']['PointsData']
        for details in data:
            print(details)
            name = (details['Name'])
            employee_email = (details['Email'])
        print(name)
        # if request.user.get_full_name:
        #     employee = AddRequest(employee_id=id,request_by=request.user,device_type=isp,name=name)
        #     employee.save() 
        # else:
        employee = AddRequest(employee_id=id,request_by=request.user,isp=isp,name=name,employee_email=employee_email)
        employee.save() # save the instance to the database
        messages.warning(request,"Request has been created")
        MESSAGE_TAGS = 'alert-danger'
        context = {
            'MESSAGE_TAGS':MESSAGE_TAGS
        }
        return redirect('request_data')
    return redirect('add_request')




def assignment(request):
    if request.method == "POST":
        employee_id = request.POST['employee_id']
        print(employee_id)
        unapproved_requests = AddRequest.objects.filter(is_approved=False).values()
        # find = device_inventory.objects.filter(employee_id=employee_id).values()
        # print(find)
        context = {
        'unapproved_requests': unapproved_requests,

        }
        return render(request, "home/form_elements.html", context)
    unapproved_requests = AddRequest.objects.filter(is_approved=False).values()
    context = {
        'unapproved_requests': unapproved_requests,
    }
    return render(request, "home/form_elements.html", context)

# this will post data to approved request
@csrf_exempt
def get_approved_request_details(request):
    if request.method=="POST":
        ticket_id = request.POST['ticket_id']
        request = AddRequest.objects.get(id=ticket_id) # get all request data here
        print(request)
        employee_id = request.employee_id
        print(employee_id)
        device = device_inventory.objects.get(assigned_to=employee_id) # get complete device data here
        sim = sim_inventory.objects.get(assigned_to=employee_id) # get complete sim data here
        allocation = DeviceAllocation.objects.get(assigned_to=employee_id) # get complete allocation data here
        # Create a dictionary containing the data
        data = {
                'id': request.id,
                'name': request.name,
                'employee_id': request.employee_id,
                'employee_email': request.employee_email,
                'ticket_id' : request.ticket_id,
                'request_by': request.request_by,
                'request_date': request.request_date,
                'approved_by': request.approved_by,
                'approved_date': request.approved_date,
                'allocate_date': allocation.allocated_date,
                'allocated_by' : allocation.allocated_by,
                'device_type': device.type,
                'isp': request.isp,
                'sim_number' : sim.sim_card,
                'data_limit' : sim.data_limit,
        }
        return JsonResponse(data)

# device request approving here
@csrf_exempt
def approve_request(request):
    try:
        if request.method == 'POST':
            user = request.user.username
            ticket_id = request.POST['ticket']
            device_imei = request.POST['imei']
            sim_num = request.POST['sim_num']
            remarks = request.POST['remarks']

            if device_inventory.objects.filter(imei=device_imei).exists() and sim_inventory.objects.filter(sim_card=sim_num).exists():
                device = device_inventory.objects.get(imei=device_imei)
                request_sim = sim_inventory.objects.get(sim_card=sim_num)
                if device.status == 'NotAssigned' and request_sim.status == 'NotAssigned':
                    if device.isp == request_sim.isp:
                        request_ticket = AddRequest.objects.get(ticket_id=ticket_id)
                        request_ticket.approved_date = timezone.now()
                        request_ticket.is_approved = True
                        request_ticket.approved_by = user
                        request_ticket.assigned_device_imei = device_imei
                        request_ticket.save()
                        print("request approved")

                        request_device = device_inventory.objects.get(imei=device_imei)
                        request_device.status = 'Assigned To'
                        request_device.assigned_to = request_ticket.employee_id
                        request_device.save()
                        print("device allocated")

                        request_sim = sim_inventory.objects.get(sim_card=sim_num)
                        request_sim.status = 'Assigned To'
                        request_sim.assigned_to = request_ticket.employee_id
                        request_sim.save()
                        print("sim allocated")

                        device = device_inventory.objects.get(imei=device_imei)
                        sim = sim_inventory.objects.get(sim_card=sim_num)
                        ticket = AddRequest.objects.get(ticket_id=ticket_id)
                        allocation = DeviceAllocation.objects.create(assigned_device=device,
                                                                    assigned_sim=sim,
                                                                    ticket=ticket,
                                                                    allocated_date=timezone.now(),
                                                                    allocated_by=user, remarks=remarks)
                        allocation.save()
                        print("allocation done!")
                        messages.success(request,"Request has been Approved")
                        return redirect('form')
                    else:
                        messages.error(request, "Different ISP of Sim or Device, it must be same")
                        return redirect('form')
                else:
                    messages.error(request, "Device or sim is already assigned!")
                    return redirect('form')
            else:
                messages.error(request, "Sim or Device Does not exist!")
                return redirect('form')
    except:
        messages.error(request, "An error has been occurred!")
        return render(request, "home/page-404.html", status=400)




# the reject method is not done yet. 
@csrf_exempt
def reject_request(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        print(request_id)
        # Logic to reject the request
        return JsonResponse({'success': True})


# rendering Stock page
def stock(request):
    return render(request, "home/stock.html")


def add_device(request):
    if request.method == "POST":
        data = request.POST.dict()
        imei = data.pop('imei')
        isp = data.pop('isp')
        device_type = data.pop('type')
        data.pop('csrfmiddlewaretoken', None)  # Remove the csrfmiddlewaretoken field
        if device_inventory.objects.filter(imei=imei).exists():
            messages.error(request, "A Device with the same details already exists in the database.")
        else:
            device = device_inventory(punched_by=request.user, imei=imei, isp=isp, type=device_type, **data)
            device.save()
            messages.info(request, "Device Record has been added!")
    return render(request, "home/stock.html")


@csrf_exempt
def add_sim(request):
    if request.method == "POST":
        data = request.POST.dict()
        try:
            sim = sim_inventory.objects.get(sim_card=data['sim_card'])
            messages.error(request, "A SIM with the same Number already exists in the database.")
            return render(request, "home/page-404.html", status=400)
        except sim_inventory.DoesNotExist:
            sim = sim_inventory(
                added_by=request.user,
                sim_status=data['device_status'],
                sim_card=data['sim_card'],
                msisdn=data['msisdn'],
                data_limit=data['data_limit'],
                isp=data['isp'],
                location=data['location']
            )
            sim.save()
            messages.info(request, "Sim has been added in Record")
            return render(request, "home/stock.html")
    else:
        return render(request, "home/page-404.html", status=400)
# def add_sim(request):
#     if request.method == "POST":
#         msisdn = request.POST['msisdn']
#         location = request.POST['location']
#         isp = request.POST['isp']
#         data_limit = request.POST['data_limit']
#         sim_card = request.POST['sim_card']
#         sim_status = request.POST['device_status']
#         print("===================", sim_status)
#         # Check if a SIM with the same details already exists in the database
#         if sim_inventory.objects.filter(sim_card=sim_card).exists():
#             messages.error(request, "A SIM with the same details already exists in the database.")
#             return render(request, "home/stock.html")
#         # Create and save the new SIM object
#         sim = sim_inventory(
#             added_by=request.user,
#             sim_status=sim_status,
#             sim_card=sim_card,
#             msisdn=msisdn,
#             data_limit=data_limit,
#             isp=isp,
#             location=location
#         )
#         sim.save()
#         messages.info(request, "Sim has been added in Record")
#     return render(request, "home/stock.html")




# filtering device record here
def stock_record(request):
    if request.method == "POST":
        location=request.POST['location']
        type=request.POST['type']
        isp=request.POST['isp']
        data_limit=request.POST['data_limit']
        manufacturer=request.POST['manufacturer']
        device_model=request.POST['device_model']
        imei=request.POST['imei']
        device_status=request.POST['device_status']
        if device_inventory.objects.filter(Q(device_status__contains=f'{device_status}') | 
                                           Q(imei__contains=f'{imei}') | Q(device_model__contains=f'{device_model}') | 
                                           Q(manufacturer__contains=f'{manufacturer}') | Q(type__contains=f'{type}') | 
                                           Q(location__contains=f'{location}') | Q(data_limit__contains=f'{data_limit}') | 
                                           Q(isp__contains=f'{isp}')).exists():
            s = device_inventory.objects.filter(Q(device_status__contains=f'{device_status}') & Q(imei__contains=f'{imei}') & 
                                                Q(device_model__contains=f'{device_model}') & Q(manufacturer__contains=f'{manufacturer}') & 
                                                Q(type__contains=f'{type}') & Q(location__contains=f'{location}') & 
                                                Q(data_limit__contains=f'{data_limit}') & Q(isp__contains=f'{isp}')).values()
            print(s)
            context= {'s':s}
            return render(request, "home/record.html", context)
        else:
            messages.info(request,"No Record has been found!")
    s = device_inventory.objects.filter(status='NotAssigned').all()
    context= {'s':s}
    return render(request, "home/record.html", context)

# filter sim record here
def sim_record(request):
    if request.method == "POST":
        location=request.POST['location']
        isp=request.POST['isp']
        data_limit=request.POST['data_limit']
        msisdn=request.POST['msisdn']
        sim_card=request.POST['sim_card']
        device_status=request.POST['device_status']
        if sim_inventory.objects.filter(Q(sim_status__contains=f'{device_status}') | Q(sim_card__contains=f'{sim_card}') | Q(msisdn__contains=f'{msisdn}') | Q(location__contains=f'{location}') | Q(data_limit__contains=f'{data_limit}') | Q(isp__contains=f'{isp}')).exists():
            s = sim_inventory.objects.filter(Q(sim_status__contains=f'{device_status}') & Q(sim_card__contains=f'{sim_card}') & Q(msisdn__contains=f'{msisdn}') & Q(location__contains=f'{location}') & Q(data_limit__contains=f'{data_limit}') & Q(isp__contains=f'{isp}')).values()
            print(s)
            context= {'s':s}
            return render(request, "home/record_sim.html", context)
        else:
            messages.info(request,"No Record has been found!")
    s = sim_inventory.objects.filter(status='NotAssigned').all()
    context= {'s':s}
    return render(request, "home/record_sim.html", context)




@csrf_exempt
def find_isp(request):
    if request.method=="POST":
        isp=request.POST['ispf']
        print("======================",isp)
        if device_inventory.objects.filter(isp__contains=f'{isp}').exists():
            find = device_inventory.objects.filter(isp__contains=f'{isp}').values()
            print(find[:1])
            m = "Available"
            return JsonResponse(m,safe=False, content_type='text/plain')
        else:
            m= "OutofStock"
            return JsonResponse(m,safe=False, content_type='text/plain')

@csrf_exempt
def findQuota(request):
    if request.method=="POST":
        findQuota=request.POST['findQuotaf']
        isp=request.POST['ispf']
        loc=request.POST['locc']
        print("++++++++++++++++++++",loc)
        print("++++++++++++++++++++",findQuota)
        print("++++++++++++++++++++",isp)
        find = device_inventory.objects.filter(Q(location__contains=f'{loc}') & Q(data_limit__contains=f'{findQuota}') & Q(isp__contains=f'{isp}')).values()
        print(find)
        if find.count() != 0:
            t = "available"
            return JsonResponse(t,safe=False, content_type='text/plain')
        else:
            m= "Out of Stock"
            return JsonResponse(m,safe=False, content_type='text/plain')


def filter_dropdown(request):

    selected_value = request.GET.get('original_dropdown')

    # create a queryset with the selected value
    filtered_queryset = device_inventory.objects.filter(field=selected_value)

    # create a list of filtered options
    filtered_options = []
    for item in filtered_queryset:
        filtered_options.append({'id': item.id, 'name': item.name})

    # return filtered options as JSON
    return JsonResponse({'filtered_options': filtered_options})



# def device_update(request, pk):
#     # device = get_object_or_404(Device, pk=pk)
#     if request.method == 'POST':
#         location = request.POST.get('location')
#         type = request.POST.get('type')
#         isp = request.POST.get('isp')
#         data_limit = request.POST.get('data_limit')
#         manufacturer = request.POST.get('manufacturer')
#         device_model = request.POST.get('device_model')
#         imei = request.POST.get('imei')
#         msisdn = request.POST.get('msisdn')
#         sim_card = request.POST.get('sim_card')
#         device_status = request.POST.get('device_status')
#         instock_date = request.POST.get('instock_date')
#         punched_by = request.POST.get('punched_by')
#         remarks = request.POST.get('remarks')
#         save()
#         return JsonResponse({'status': 'success'})
#     return render(request, 'device_update.html', {'device': device})

# def device_delete(request, pk):
#     device = get_object_or_404(Device, pk=pk)
#     if request.method == 'POST':
#         device.delete()
#         return JsonResponse({'status': 'success'})
#     return render(request, 'device_confirm_delete.html', {'device': device})



@csrf_exempt
def delete_device(request,pk):
    if request.method == 'POST':
        pk=pk
        print("...................",pk)
        try:
            device = device_inventory.objects.filter(id=pk).values()
            print(device)
            device_inventory.objects.get(id=pk).delete()
            print("deleted", )
            return JsonResponse(safe=False, content_type='text/plain')
        except device_inventory.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Device does not exist'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


def edit_device(request):
    if request.method == 'POST':
        device_id = request.POST.get('id')
        try:
            device = device_inventory.objects.get(id=device_id)
            device.location = request.POST.get('location')
            device.type = request.POST.get('type')
            device.isp = request.POST.get('isp')
            device.data_limit = request.POST.get('data_limit')
            device.manufacturer = request.POST.get('manufacturer')
            device.device_model = request.POST.get('device_model')
            device.imei = request.POST.get('imei')
            device.msisdn = request.POST.get('msisdn')
            device.sim_card = request.POST.get('sim_card')
            device.device_status = request.POST.get('device_status')
            device.instock_date = request.POST.get('instock_date')
            device.punched_by = request.POST.get('punched_by')
            device.remarks = request.POST.get('remarks')
            device.save()
            return JsonResponse({'success': True, 'device': {
                'location': device.location,
                'type': device.type,
                'isp': device.isp,
                'data_limit': device.data_limit,
                'manufacturer': device.manufacturer,
                'device_model': device.device_model,
                'imei': device.imei,
                'msisdn': device.msisdn,
                'sim_card': device.sim_card,
                'device_status': device.device_status,
                'instock_date': device.instock_date,
                'punched_by': device.punched_by,
                'remarks': device.remarks,
            }})
        except device_inventory.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'device_inventory does not exist'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})




@csrf_exempt
def get_request_data(request, id):
    try:
        request = AddRequest.objects.get(id=id)
    except AddRequest.DoesNotExist:
        # Return a 404 error if the requested object doesn't exist
        return render(request, 'home/page-404.html', status=404)
    # Create a dictionary containing the device data
    data = {
        'id': request.id,
        'employee_idd': request.employee_id,
        'name': request.name,
        'request_date': request.request_date,
        'request_by': request.request_by,
        'device_type': request.isp,
        'ticket_id' : request.ticket_id,
    }
    return JsonResponse(data)



@csrf_exempt
def update_device_data(request):
    if request.method == 'POST':
        data = request.POST.dict()
        device_id = data.pop('id')
        user = request.user.username
        device = get_object_or_404(device_inventory, id=device_id)
        # Update device data with new values
        for field, value in data.items():
            setattr(device, field, value)
        device.punched_by = user
        device.instock_date = datetime.now()
        device.save()
        messages.info(request, "Record has been updated")
        return redirect('stock_record')
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
# @csrf_exempt
# def update_device_data(request):
#     if request.method == 'POST':
#         id = request.POST['id']
#         user = request.user.username
#         try:
#             device = device_inventory.objects.get(id=id)
#             device.location = request.POST.get('location')
#             device.type = request.POST.get('type')
#             device.isp = request.POST.get('isp')
#             device.data_limit = request.POST.get('data_limit')
#             device.manufacturer = request.POST.get('manufacturer')
#             device.device_model = request.POST.get('device_model')
#             device.imei = request.POST.get('imei')
#             device.device_status = request.POST.get('device_status')
#             device.instock_date = datetime.now()
#             device.punched_by = user
#             device.remarks = request.POST.get('remarks')
#             device.save()
#             messages.info(request,"Record has been Updated")
#             return redirect('stock_record')
#         except device_inventory.DoesNotExist:
#             messages.info(request,"Record  does not exist")
#             return JsonResponse({'success': False, 'error': 'device does not exist'})
#     else:
#         return JsonResponse({'success': False, 'error': 'Invalid request method'})



@csrf_exempt
def get_device_data(request, id):
    id=id
    device = device_inventory.objects.get(id=id)
    # device = get_object_or_404(Device, id=id)
    print("/////////////////////////////",id)
    print(device)
    # Create a dictionary containing the device data
    data = {
        'location': device.location,
        'type': device.type,
        'isp': device.isp,
        'data_limit': device.data_limit,
        'manufacturer': device.manufacturer,
        'device_model': device.device_model,
        'imei': device.imei,
        'device_status': device.device_status,
        'punched_by': device.punched_by,
        'instock_date': device.instock_date,
        'remarks': device.remarks,
        'id': device.id,
    }

    return JsonResponse(data)



@csrf_exempt
def get_sim_data(request, id):
    id=id
    device = sim_inventory.objects.get(id=id)
    # device = get_object_or_404(Device, id=id)
    print("/////////////////////////////",id)
    print(device)
    # Create a dictionary containing the device data
    data = {
        'location': device.location,
        'isp': device.isp,
        'data_limit': device.data_limit,
        'msisdn': device.msisdn,
        'sim_card': device.sim_card,
        'device_status': device.sim_status,
        'punched_by': device.added_by,
        'instock_date': device.instock_date,
        'id': device.id,
    }

    return JsonResponse(data)


@csrf_exempt
def update_sim_data(request):
    if request.method == 'POST':
        id = request.POST['id']
        print("========================",id)
        try:
            device = sim_inventory.objects.get(id=id)
            device.location = request.POST.get('location')
            device.isp = request.POST.get('isp')
            device.data_limit = request.POST.get('data_limit')
            device.msisdn = request.POST.get('msisdn')
            device.sim_card = request.POST.get('sim_card')
            device.sim_status = request.POST.get('device_status')
            device.instock_date = datetime.now()
            device.added_by = request.user.username
            device.save()
            messages.info(request,"Record has been Updated")
            return redirect('sim_record')
        except device_inventory.DoesNotExist:
            messages.info(request,"Record  does not exist")
            return JsonResponse({'success': False, 'error': 'device does not exist'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})



