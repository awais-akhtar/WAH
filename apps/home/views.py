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






@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

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

def test(request):
    return render(request,"home/wizard-build-profile.html")




def add_request(request):
    if request.method == "POST":
        text = request.POST.get('text')
        print(text)
        id = int(text)
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
        if data2 == 'Active':
            ss= json.loads(response.text)
            data=ss['data']['PointsData']
            for details in data:
                print(details['Location'])
                f = (details['Location'])
            print("ttttttttttttttt",f)

            if AddRequest.objects.filter(employee_id=f'{id}').exists():
                find = AddRequest.objects.filter(employee_id=f'{id}').values()
                print(find)
            unapproved_requests = AddRequest.objects.filter(is_approved=False).values()
            approved_requests = AddRequest.objects.filter(is_approved=True).values()
            context = {'obj':data, 'data2':data2, 'find':find, 'id':id,
                'unapproved_requests': unapproved_requests,
                'approved_requests': approved_requests,}

            return render(request, "home/add_request.html", context)
        else:
            ss= json.loads(response.text)
            data=ss['data']['PointsData']
            for details in data:
                print(details['Current_Designation'])
            unapproved_requests = AddRequest.objects.filter(is_approved=False).values()
            approved_requests = AddRequest.objects.filter(is_approved=True).values()
            context = {'obj':data, 'data2':data2,
                               'unapproved_requests': unapproved_requests,
        'approved_requests': approved_requests,}
            return render(request, "home/add_request.html", context)
    unapproved_requests = AddRequest.objects.filter(is_approved=False).values()
    approved_requests = AddRequest.objects.filter(is_approved=True).values()
    context = {
        'unapproved_requests': unapproved_requests,
        'approved_requests': approved_requests,
    }
    return render(request, "home/add_request.html", context)

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
        print(name)
        # if request.user.get_full_name:
        #     employee = AddRequest(employee_id=id,request_by=request.user,device_type=isp,name=name)
        #     employee.save() 
        # else:
        employee = AddRequest(employee_id=id,request_by=request.user,device_type=isp,name=name)
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


# def approve_request(request, request_id):
#     request = AddRequest.objects.get(pk=request_id)
#     request.is_approved = True
#     request.approved_date = timezone.now()
#     request.save()
#     return redirect('list_unapproved_requests')
@csrf_exempt
def approve_request(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        isp = request.POST.get('isp')
        print(request_id)
        request = AddRequest.objects.get(pk=request_id)
        request.is_approved = True
        request.approved_date = timezone.now()
        request.approved_by = request.user
        request.save()
        return JsonResponse({'success': True})
        
@csrf_exempt
def reject_request(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        print(request_id)
        # Logic to reject the request
        return JsonResponse({'success': True})



def stock(request):
    if request.method == "POST":
        location=request.POST['location']
        type=request.POST['type']
        isp=request.POST['isp']
        data_limit=request.POST['data_limit']
        manufacturer=request.POST['manufacturer']
        device_model=request.POST['device_model']
        imei=request.POST['imei']
        msisdn=request.POST['msisdn']
        sim_card=request.POST['sim_card']
        device_status=request.POST['device_status']
        remarks=request.POST['remarks']
        stock = device_inventory(remarks=remarks,punched_by=request.user,device_status=device_status,sim_card=sim_card,msisdn=msisdn,imei=imei,device_model=device_model,manufacturer=manufacturer,data_limit=data_limit,isp=isp,type=type,location=location)
        stock.save()
        messages.info(request,"New Record has been added!")
        return render(request, "home/stock.html")
    s = device_inventory.objects.filter(id=1).values()
    context= {
        's':s
    }
    return render(request, "home/stock.html", context)


def stock_record(request):
    if request.method == "POST":
        location=request.POST['location']
        type=request.POST['type']
        isp=request.POST['isp']
        data_limit=request.POST['data_limit']
        print(data_limit)
        manufacturer=request.POST['manufacturer']
        device_model=request.POST['device_model']
        imei=request.POST['imei']
        msisdn=request.POST['msisdn']
        sim_card=request.POST['sim_card']
        device_status=request.POST['device_status']
        if device_inventory.objects.filter(Q(device_status__contains=f'{device_status}') | Q(sim_card__contains=f'{sim_card}') | Q(msisdn__contains=f'{msisdn}') | Q(imei__contains=f'{imei}') | Q(device_model__contains=f'{device_model}') | Q(manufacturer__contains=f'{manufacturer}') | Q(type__contains=f'{type}') | Q(location__contains=f'{location}') | Q(data_limit__contains=f'{data_limit}') | Q(isp__contains=f'{isp}')).exists():
            s = device_inventory.objects.filter(Q(device_status__contains=f'{device_status}') & Q(sim_card__contains=f'{sim_card}') & Q(msisdn__contains=f'{msisdn}') & Q(imei__contains=f'{imei}') & Q(device_model__contains=f'{device_model}') & Q(manufacturer__contains=f'{manufacturer}') & Q(type__contains=f'{type}') & Q(location__contains=f'{location}') & Q(data_limit__contains=f'{data_limit}') & Q(isp__contains=f'{isp}')).values()
            print(s)
            context= {'s':s}
            return render(request, "home/record.html", context)
        else:
            messages.info(request,"No Record has been found!")
    s = device_inventory.objects.all()
    context= {'s':s}
    return render(request, "home/record.html", context)



def assign_device(request):
    if request.method == "POST":
        location=request.POST['location']
        type=request.POST['type']
        isp=request.POST['isp']
        data_limit=request.POST['data_limit']
        manufacturer=request.POST['manufacturer']
        device_model=request.POST['device_model']
        imei=request.POST['imei']
        msisdn=request.POST['msisdn']
        sim_card=request.POST['sim_card']
        device_status=request.POST['device_status']
        device_picture=request.POST['devicephoto']
        assign = device_assign(punched_by=request.user,device_picture=device_picture,device_status=device_status,sim_card=sim_card,msisdn=msisdn,imei=imei,device_model=device_model,manufacturer=manufacturer,data_limit=data_limit,isp=isp,type=type,location=location)
        assign.save()
        return render(request, "home/stock.html")
    return render(request, "home/stock.html")



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
        'msisdn': device.msisdn,
        'sim_card': device.sim_card,
        'device_status': device.device_status,
        'punched_by': device.punched_by,
        'instock_date': device.instock_date,
        'remarks': device.remarks,
        'id': device.id,
    }

    return JsonResponse(data)


@csrf_exempt
def update_device_data(request):
    if request.method == 'POST':
        id = request.POST['id']
        user = request.user.username
        try:
            device = device_inventory.objects.get(id=id)
            # history = device.history.all()
            # print("history=======",     history)
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
            device.instock_date = datetime.now()
            device.punched_by = user
            device.remarks = request.POST.get('remarks')
            device.save()

        # Create a DeviceHistory record
            # DeviceHistory.objects.create(
            #     device=device,
            #     location=device.location,
            #     type=device.type,
            #     isp=device.isp,
            #     data_limit=device.data_limit,
            #     manufacturer=device.manufacturer,
            #     device_model=device.device_model,
            #     imei=device.imei,
            #     msisdn=device.msisdn,
            #     sim_card=device.sim_card,
            #     device_status=device.device_status,
            #     instock_date=device.instock_date,
            #     punched_by=device.punched_by,
            #     remarks=device.remarks,
            #     updated_date=timezone.now(),
            # )
            return redirect('stock_record')
            # return JsonResponse({'success': True, 'device': {
            #     'location': device.location,
            #     'type': device.type,
            #     'isp': device.isp,
            #     'data_limit': device.data_limit,
            #     'manufacturer': device.manufacturer,
            #     'device_model': device.device_model,
            #     'imei': device.imei,
            #     'msisdn': device.msisdn,
            #     'sim_card': device.sim_card,
            #     'device_status': device.device_status,
            #     'instock_date': device.instock_date,
            #     'punched_by': device.punched_by,
            #     'remarks': device.remarks,
            # }})
        except device_inventory.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'device_inventory does not exist'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})



