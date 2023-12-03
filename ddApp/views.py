import pandas as pd
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.core.files.storage import FileSystemStorage
from ddProject import settings
import uuid
import bleach
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

from .models import TaskAssigned, BeneficiaryModel,SetupBoxInfo, InstallerModel, User



from django import forms
from .forms import TaskAssignedForm
from .forms import SetupBoxInfoForm
from .forms import final_form
from .forms import StateForm, DistrictForm, BlockForm, BesForm, InstallerForm, CustomLoginForm


from .forms import verify_passcode
from twilio.rest import Client
import random
import requests
import datetime
import platform
import geocoder
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import inch  # Used for converting inches to points
from reportlab.pdfbase.ttfonts import TTFont

# Get system information
system_info = platform.uname()


def Index(request):
    total_ins = InstallerModel.objects.all().count()
    total_bes = BeneficiaryModel.objects.all().count()
    total_workdone = TaskAssigned.objects.filter(completion='Installation Done!').count()
    inprocess_work = TaskAssigned.objects.all().count()
    print(total_bes, total_workdone, inprocess_work)


    return render(request, 'index.html', {'total_ins': total_ins, 'total_bes': total_bes, 'total_workdone': total_workdone, 'inprocess_work': inprocess_work})

def aboutView(request):
    return render(request, 'about.html')

def contactView(request):
    return render(request, 'contact.html')


def Profile(request):
    user = request.user
    if user.is_superuser:
        user_details = user
    else:
        user_details = InstallerModel.objects.get(installer = user)
    return render(request, 'profile.html', {'user_details': user_details})



def superuser_dashboard(request):
    totals = []
    completed = []
    not_assigned = []
    states = BeneficiaryModel.objects.values('state').distinct()
    all_states = [s['state'] for s in states]
    request.session['all_states'] = all_states
    num_states = len(all_states)
    states_ids = list(range(num_states))

    for state in all_states:
        totals.append(TaskAssigned.objects.filter(beneficiary__state= state).count())
        completed.append(TaskAssigned.objects.filter(beneficiary__state= state, completion= 'Installation Done!').count())
        bes_count = BeneficiaryModel.objects.filter(state= state).count()
        not_assigned.append(bes_count - totals[-1])
    zipped = zip(states_ids, all_states, totals, completed, not_assigned)


    total_ins = InstallerModel.objects.filter().count()
    total_bes = BeneficiaryModel.objects.filter().count()

    total = TaskAssigned.objects.filter().count()
    completed_tasks = TaskAssigned.objects.filter(completion = 'Installation Done!').count()


    return render(request, 'superuser.html', {'total': total, 'completed_tasks':completed_tasks, 'zipped': zipped, 'total_bes': total_bes, 'total_ins': total_ins })

def DistrictState(request, id):
    states = request.session.get('all_states')
    state = states[int(id)]
    request.session['state'] = state
    districts = BeneficiaryModel.objects.filter(state= state).values('district').distinct()
    all_districts = [d['district'] for d in districts]
    request.session['all_districts'] = all_districts
    print(all_districts)
    num_districts = len(all_districts)
    districts_ids = list(range(num_districts))
    totals = []
    completed = []
    not_assigned = []


    for district in all_districts:

        totals.append(TaskAssigned.objects.filter(beneficiary__district= district).count())
        completed.append(TaskAssigned.objects.filter(beneficiary__district= district, completion= 'Installation Done!').count())
        bes_count = BeneficiaryModel.objects.filter(state= state, district= district).count()
        not_assigned.append(bes_count - totals[-1])


    zipped = zip(districts_ids, all_districts, totals, completed, not_assigned)


    return render(request, 'district_state_data.html', {'zipped': zipped, 'state': state})

def BlockDistrict(request, id):
    state = request.session.get('state')
    districts = request.session.get('all_districts')
    district = districts[int(id)]
    request.session['district'] = district
    blocks = BeneficiaryModel.objects.filter(district= district).values('block').distinct()
    all_blocks = [b['block'] for b in blocks]
    request.session['all_blocks'] = all_blocks
    print(all_blocks)
    num_blocks = len(all_blocks)
    blocks_ids = list(range(num_blocks))
    totals = []
    completed = []
    not_assigned = []


    for block in all_blocks:
        totals.append(TaskAssigned.objects.filter(beneficiary__block= block).count())
        completed.append(TaskAssigned.objects.filter(beneficiary__block= block, completion= 'Installation Done!').count())
        bes_count = BeneficiaryModel.objects.filter(state= state, block= block, district= district).count()
        not_assigned.append(bes_count - totals[-1])

    zipped = zip(blocks_ids, all_blocks, totals, completed, not_assigned)




    return render(request, 'block_district_state_data.html', {'zipped': zipped, 'state': state, 'district': district})

# def BesBlock(request, id):
#     state = request.session.get('state')
#     district = request.session.get('district')
#     blocks = request.session.get('all_blocks')
#     block = blocks[int(id)]
#     bes = BeneficiaryModel.objects.filter(district= district, block= block).values('id','name')
#     print(bes)
#     return render(request, 'bes_blocks.html')






def BesBlock(request, id):
    state = request.session.get('state')
    district = request.session.get('district')
    blocks = request.session.get('all_blocks')
    print(blocks)
    block = blocks[int(id)]
    request.session['block'] = block
    print(block)
    bes = BeneficiaryModel.objects.filter(district= district, block= block).values('id')
    all_bes = [b['id'] for b in bes]
    request.session['all_bes'] = all_bes
    print(all_bes)
    num_bes = len(all_bes)
    bes_ids = list(range(num_bes))
    pending = []
    pen_ins = []
    completed = []
    by_ins = []
    not_assigned = []

    for bes in all_bes:
        count = TaskAssigned.objects.filter(beneficiary__id= bes, completion='Installation Done!').count()
        if count == 1:
            ins = TaskAssigned.objects.filter(beneficiary__id= bes, completion='Installation Done!')
            by_ins.append(ins[0].installer.username)
            completed.append(bes)
        else:
            count = TaskAssigned.objects.filter(beneficiary__id= bes).count()
            if count == 1:
                pending.append(bes)
                ins = TaskAssigned.objects.filter(beneficiary__id= bes)
                pen_ins.append(ins[0].installer.username)
            else:
                not_assigned.append(bes)

    print('inses', by_ins)
    print('completed', completed)
    print('pending', pending)
    zipped = zip(completed, by_ins)
    zipped2 = zip(pending, pen_ins)

    return render(request, 'bes_blocks.html', {'zipped':zipped, 'zipped2': zipped2, 'completed': completed, 'pending': pending, 'not_assigned': not_assigned, 'state': state, 'district': district, 'block_name': block})

def filtered_Bes_block(request, status):
    if request.method == 'POST':
        all_bes = request.session.get('all_bes')
        state = request.session.get('state')
        district = request.session.get('district')
        block =  request.session.get('block')
        if status == 'Completed':
            complete = []
            for bes in all_bes:
                if TaskAssigned.objects.filter(beneficiary__id = bes,completion='Installation Done!').count() == 1:
                    complete.append(TaskAssigned.objects.filter(beneficiary__id = bes,completion='Installation Done!'))

            tasks_bes = []
            tasks_ins = []
            for queryset in complete:
                for task in queryset:
                    tasks_bes.append(task.beneficiary)
                    ins = InstallerModel.objects.filter(installer= task.installer)[0]
                    tasks_ins.append(ins)
            bes_ins = zip(tasks_bes, tasks_ins)
            print('task_bes', tasks_bes)
            print('task_ins', tasks_ins)
            return render(request, 'bes_blocks.html', {'complete': bes_ins,'state': state, 'district': district, 'block_name': block })
        elif status == 'Pending':
            pending = []
            for bes in all_bes:
                if TaskAssigned.objects.filter(beneficiary__id = bes).exclude(completion='Installation Done!').count() == 1:
                    pending.append(TaskAssigned.objects.filter(beneficiary__id=bes).exclude(completion='Installation Done!'))
            tasks_bes = []
            tasks_ins = []
            for queryset in pending:
                for task in queryset:
                    tasks_bes.append(task.beneficiary)
                    ins = InstallerModel.objects.filter(installer= task.installer)[0]
                    tasks_ins.append(ins)
            bes_ins = zip(tasks_bes, tasks_ins)
            return render(request, 'bes_blocks.html', {'pendings': bes_ins, 'state': state, 'district': district, 'block_name': block })
        else:
            not_assigned = []
            for bes in all_bes:
                if TaskAssigned.objects.filter(beneficiary__id = bes).count() == 0:
                    not_assigned.append(BeneficiaryModel.objects.filter(id= bes))
            tasks_bes = [queryset[0] for queryset in not_assigned]
            return render(request, 'bes_blocks.html', {'unassigned': tasks_bes, 'state': state, 'district': district, 'block_name': block})

def aboutBesView(request, bes_id):
    bes = BeneficiaryModel.objects.get(id= bes_id)
    return render(request, 'about_user.html', {'bes': bes})

def aboutInsView(request, ins_id):
    ins = InstallerModel.objects.get(id= ins_id)
    return render(request, 'about_user.html', {'ins': ins})


class UserLoginView(LoginView):
    template_name = 'registration/login.html'  # Customize this template as needed
    form_class = CustomLoginForm

    def get_success_url(self):
        # Check if the user is a superuser
        if self.request.user.is_superuser:
            return reverse('superuser_dashboard')
            print('a superuser')
        return reverse('user_dashboard')

def is_superuser(user):
    return user.is_authenticated and user.is_superuser

def Assign(request):
    if request.method == 'POST':
        selected_installer = request.session.get('selected_installer')
        form = BesForm(request.POST)
        bes_choices = request.session.get('bes_choices')
        form.fields['bes'].choices = bes_choices
        if form.is_valid():
            try:
                selected_bes = form.cleaned_data['bes']

                installer_model = InstallerModel.objects.get(name = selected_installer)
                for bes in selected_bes:
                    beneficiary = BeneficiaryModel.objects.get(name= bes)
                    user = User.objects.get(username= installer_model)

                    task = TaskAssigned(installer= user, beneficiary= beneficiary)
                    task.save()

                messages.success(request, 'Tasks are assigned successfully')
            except Exception as e:
                messages.error(request,'beneficiary is already assigned')
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Error in field {field}: {error}")
            messages.error(request, 'some error occured, please try again later')
            return redirect('dashboard')

    else:

        return redirect('dashboard')
        #model = TaskAssigned(installer= , beneficiary= )
        #return HttpResponse(f'{installer.id}, {installer.name}, {installer}')

@method_decorator(login_required, name='dispatch')
class HomePage(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            tasks_data = TaskAssigned.objects.all()
            data = pd.DataFrame(list(tasks_data.values()))
            print(data.head())
            total_assigned_tasks = len(data)
            print('superuser')
            return render(request, 'superuser.html', {'total': total_assigned_tasks})
        else:
            print(self.request.user.username)
            task = TaskAssigned.objects.filter(installer=request.user)
            return render(request, 'home.html', {'tasks': task})

    def post(self, request, task_id,  *args, **kwargs):
        task = TaskAssigned.objects.get(id = task_id)
        return render(request, 'home.html')






# Installer views


class ProcessPage(View):
    def get(self, request, task_id, *args, **kwargs):
        task = TaskAssigned.objects.get(id = task_id)
        initial_data = {
            'task_field': task_id,
            'beneficiary': task.beneficiary.name
        }
        try:
            beneficiary_registered = SetupBoxInfo.objects.get(beneficiary_registered = task.beneficiary)
        except Exception as e:
            beneficiary_registered = None

        form = SetupBoxInfoForm(initial= initial_data)
        installer_details = InstallerModel.objects.get(installer = request.user)
        client_ip = request.META.get('REMOTE_ADDR')
        g = geocoder.ip('me')
        if g.status == 'OK':
            lat, lng = g.latlng
            print(f"Latitude: {lat}, Longitude: {lng}")
        else:
            print("Failed to retrieve geolocation information.")
        print(g)
        try:
            location_info = g.json
            city = location_info.get('city')
            region = location_info.get('state')
            country = location_info.get('country')
            lat = location_info.get('lat')
            lng = location_info.get('lng')
        except Exception as e:
            city, region, country, latitude,longitude, lat, lng= 'No Value', 'No Value', 'No Value','No Value','No Value', 'No Value', 'No Value'
        initial_data_2 = {
            #'time': datetime.datetime.now().strftime("%I:%M:%S %p"),
            'time': datetime.datetime.now().time(),
            'date': datetime.date.today(),
            'installer_name': installer_details.name,#f"{request.user.first_name} {request.user.last_name}",
            'installer_address': installer_details.state,
            'installer_mobile': installer_details.mobile,
            'beneficiary_name': task.beneficiary.name,
            'beneficiary_address': task.beneficiary.state,
            'beneficiary_mobile': task.beneficiary.mobile,
            'device_info':
                f"System: {system_info.system} "
                f"Version: {system_info.version} "
                f"Machine: {system_info.machine} "
                f"Processor: {system_info.processor} ",

            'device_location' : f"{city} - {region} - {country} - latitude: {lat} - longitude: {lng}",

        }
        form_2 = final_form(initial=initial_data_2)
        form.fields['beneficiary'].widget.attrs['disabled'] = True
        form_2_fields = ['time','date','installer_name','installer_address','installer_mobile','beneficiary_name','beneficiary_address','beneficiary_mobile','device_info','device_location']
        for field in form_2_fields:
            form_2.fields[field].widget = forms.HiddenInput()
            #form_2.fields[field].widget.attrs['disabled'] = True





        return render(request, 'process_page.html', {'task_id':task.id, 'form':form, 'beneficiary_registered': beneficiary_registered,
                                                     'form_2': form_2})
    def post(self, request, task_id, *args, **kwargs):
        sr = request.POST.get('setup_box')
        task = TaskAssigned.objects.get(id = task_id)
        try:
            boxes = SetupBoxInfo.objects.all()
            initial_data = {
                'task_field': task_id,
                'beneficiary': task.beneficiary.name,
                'setup_box': sr,
            }
            form = SetupBoxInfoForm(initial= initial_data)
            form.fields['task_field'].widget.attrs['disabled'] = True
            form.fields['beneficiary'].widget.attrs['disabled'] = True
            form.fields['setup_box'].widget.attrs['disabled'] = True

            verify = verify_passcode()
            verify.fields['otp'].widget = forms.TextInput(attrs={'placeholder':'Enter PASSCODE'})
            return render(request, 'process_page.html', {'task_id':task_id, 'form':form})
        except SetupBoxInfo.DoesNotExist:
            form = SetupBoxInfoForm()
            return render(request, 'process_page.html', {'task_id':task.id, 'form':form})
        else:
            return HttpResponse(f'box {sr} is not present')

def verify_otp(request, task_id):
    sr = request.POST.get('setup_box')
    #task_id = request.POST.get('task_field')ssss
    print(task_id)
    task = TaskAssigned.objects.get(id=task_id)
    try:
        boxes = SetupBoxInfo.objects.get(sr_no= sr, beneficiary_registered = None)
        initial_data = {
            'task_field': task_id,
            'beneficiary': task.beneficiary.name,
            'setup_box': sr,
        }
        form = verify_passcode(initial= initial_data)
        form.fields['task_field'].widget.attrs['disabled'] = True
        form.fields['beneficiary'].widget.attrs['disabled'] = True
        form.fields['setup_box'].widget.attrs['disabled'] = True
        task_id_sr = str(task.id) + '_' + str(sr)


        account_sid = 'AC4c9bfc6f4103167c9f3b877fa6a17ef9'
        auth_token = 'e54483ea0c5268452daf8dab376fdfd7'
        twilio_phone_number = '+15128656284'

        client = Client(account_sid, auth_token)

        otp  = str(random.randint(100000, 999999))

        phone_number = str(task.beneficiary.mobile)

        try:
            message = client.messages.create(
                body=f'Your OTP is: {boxes.passcode}. Do not share your OTP.',
                from_=twilio_phone_number,
                to=phone_number)
            print('success', message.sid)
        except Exception as e:
            print('exception occured')
        messages.success(request, f'OTP sent successfully to {task.beneficiary.name} for setup box {sr}')
        return render(request, 'otp.html', {'task_id':task_id_sr,'verify':form, 'task':task, 'sr': sr})



    except SetupBoxInfo.DoesNotExist:
        initial_data = {
            'task_field': task_id,
            'beneficiary': task.beneficiary.name,
        }
        form = SetupBoxInfoForm(initial=initial_data)
        form.fields['beneficiary'].widget.attrs['disabled'] = True
        messages.error(request, 'Wrong Serial Number Entered')
        return render(request, 'process_page.html', {'task_id':task.id, 'form':form})

def confirm_passcode(request, task_id):
    given_passcode = request.POST.get('otp')
    #task_id = request.POST.get('task_field')
    task_id_sr = task_id.split('_')
    id = task_id_sr[0]
    serial = task_id_sr[1]
    print('id', id)
    print('serial',serial)


    print('task_id',task_id)
    print('task_id_sr', task_id_sr)

    task = TaskAssigned.objects.get(id = id)
    print('t.b.name',task.beneficiary.name)
    sr = request.POST.get('setup_box')
    print('sr', sr)
    box_info = SetupBoxInfo.objects.get(sr_no = serial,beneficiary_registered = None)
    original_passcode = box_info.passcode
    if given_passcode == original_passcode:
        if box_info.beneficiary_registered is None:
            print('beneficiary_id', task.beneficiary.id)
            print('beneficiary_name', task.beneficiary.name)
            box_info.beneficiary_registered = task.beneficiary
            box_info.save()
            task.completion = 'Initiated'
            task.save()
            messages.success(request, 'Beneficiary added successfully')
            return redirect('user_dashboard')
            #return render(request, 'process_page.html', {'task_id': task.id})
        else:
            messages.error(request,'beneficiary already registered' )
            return redirect('user_dashboard')

    else:
        return HttpResponse('wrong passcode')





def logout_view(request):
    return render(request, 'logout.html')


class CreateTask(View):
    def get(self, request, *args, **kwargs):
        form = TaskAssignedForm()
        return render(request, 'create_task.html', {'form':form})

def make_task(request):
    if request.method == 'POST':
        form = TaskAssignedForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Task Assigned Succesfully')
            return redirect('CreateTask')

def change_task_status(request, task_id):
    try:
        task = TaskAssigned.objects.get(id=task_id)
        if task.completion == 'Assigned':
            task.completion = 'Intrans-it'
            task.save()
    except TaskAssigned.DoesNotExist:
        pass

    return redirect('user_dashboard')

def get_geo(request: HttpRequest) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        print('remote')
        ip = request.META.get('REMOTE_ADDR')
    # Make an HTTP GET request to ipinfo.io
    response = requests.get(f"https://ipinfo.io/{ip}/json")

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        location = data.get('city', '')  # You can retrieve other location information like state, country, etc.
        region = data.get('region', '')
        country = data.get('country', '')
        postal = data.get('postal', '')
        org = data.get('org', '')
        return HttpResponse(f"Location: {location}, Region: {region}, Country: {country}, Postal: {postal}, Organization: {org}")
    else:
        return HttpResponse("Failed to retrieve location information.")



#@user_passes_test(is_superuser)
class Dashboard(View):
    def get(self, request, *args, **kwargs):
        form = StateForm(initial=[])
        district_form = DistrictForm()
        district_form.fields['district'].disabled = True
        form.fields['state'].widget.attrs['id'] = 'inputfield'
        district_form.fields['district'].widget.attrs['id'] = 'inputfield'
        return render(request, 'installer_dashboard.html',{'form':form, 'district_form': district_form})

class State(View):
    def get(self, request, *args, **kwargs):
        return redirect('dashboard')
    def post(self, request, *args, **kwargs):
        state = request.POST.get('state')
        request.session['state'] = state
        initials = {'state': state}
        state_form = StateForm(initial=initials)
        bbs = BeneficiaryModel.objects.all()
        data = pd.DataFrame(list(bbs.values()))
        print(state)
        print('check', state in data['state'].unique())
        selected_state_data = data[data['state'] == state]
        districts = [ (f'{district}',f'{district}') for district in selected_state_data['district'].unique()]
        print('districts', districts)
        district_form = DistrictForm()
        district_form.fields['district'].choices = districts
        request.session['district_choices'] = districts
        state_form.fields['state'].widget.attrs['id'] = 'inputfield'
        district_form.fields['district'].widget.attrs['id'] = 'inputfield'
        return render(request, 'district.html', {'state_form':state_form, 'district_form':district_form})

class Blocks(View):
    def get(self, request, *args, **kwargs):
        return redirect('dashboard')
    def post(self, request, *args, **kwargs):
        district = request.POST.get('district')
        request.session['district'] = district
        state = request.session.get('state')
        bbs = BeneficiaryModel.objects.all()
        data = pd.DataFrame(list(bbs.values()))
        selected_district_data = data[data['district'] == district]
        blocks = [(f'{block}', f'{block}') for block in selected_district_data['block'].unique()]
        request.session['block_choices'] = blocks
        initial_state = {'state': state}
        state_form = StateForm(initial=initial_state)

        initial_district = {'district': district}
        districts = request.session.get('district_choices')
        district_form = DistrictForm(initial_district)
        district_form.fields['district'].choices = districts



        block_form = BlockForm()

        block_form.fields['blocks'].choices = blocks
        state_form.fields['state'].widget.attrs['id'] = 'inputfield'
        district_form.fields['district'].widget.attrs['id'] = 'inputfield'
        block_form.fields['blocks'].widget.attrs['id'] = 'inputfield'


        return render(request, 'blocks.html', {'district_form':district_form, 'state_form': state_form, 'block_form':block_form })

def Ins(request):
    if request.method == 'POST':
        state = request.session.get('state')
        district = request.session.get('district')
        block_choices = request.session.get('block_choices')
        districts = request.session.get('district_choices')


        form = BlockForm(request.POST)
        form.fields['blocks'].choices = block_choices
        if form.is_valid():
            print('valid')
            selected_blocks = form.cleaned_data['blocks']
            request.session['selected_blocks'] = selected_blocks


            bbs = BeneficiaryModel.objects.all()
            data = pd.DataFrame(list(bbs.values()))



            installers_model = InstallerModel.objects.all()
            installers = pd.DataFrame(list(installers_model.values()))
            #filtered_installers = installers[installers['state'] == state]
            filtered_installers_names = installers['name']
            print(filtered_installers_names)
            installers_form = InstallerForm()
            installers_choices = [(f'{ins}', f'{ins}') for ins in filtered_installers_names]
            installers_form.fields['installer'].choices = installers_choices
            request.session['installer_choices'] = installers_choices


            state_initials = {'state': state}
            state_form = StateForm(initial=state_initials)
            # state_form.fields['state'] = state

            district_initials = {'district': district}
            district_form = DistrictForm(initial=district_initials)
            district_form.fields['district'].choices = districts

            block_initials = selected_blocks
            block_form = BlockForm(initial={'blocks': selected_blocks})
            block_form.fields['blocks'].choices = block_choices
            state_form.fields['state'].widget.attrs['id'] = 'inputfield'
            district_form.fields['district'].widget.attrs['id'] = 'inputfield'
            block_form.fields['blocks'].widget.attrs['id'] = 'inputfield'
            installers_form.fields['installer'].widget.attrs['id'] = 'inputfield'
            installers_form.fields['installer'].widget.attrs['class'] = 'radio-field'




            return render(request, 'ins.html', {'installers_form': installers_form, 'state_form': state_form, 'district_form': district_form, 'block_form':block_form} )
        return HttpResponse('form is invalid')
    return redirect('dashboard')

def Bes(request):
    if request.method == 'POST':
        state = request.session.get('state')
        district = request.session.get('district')
        block_choices = request.session.get('block_choices')
        selected_installer = request.POST.get('installer')
        print(selected_installer)
        request.session['selected_installer'] = selected_installer
        bbs = BeneficiaryModel.objects.all()
        assigned = TaskAssigned.objects.all()
        assigned_bes = []
        for i in assigned:
            assigned_bes.append(i.beneficiary.name)
        for i in assigned_bes:
            bbs = bbs.exclude(name = i)
        data = pd.DataFrame(list(bbs.values()))
        installers_model = InstallerModel.objects.all()
        installers = pd.DataFrame(list(installers_model.values()))
        #form = BlockForm(request.POST)
        #form.fields['blocks'].choices = block_choices
        form = InstallerForm(request.POST)
        installer_choices = request.session.get('installer_choices')
        form.fields['installer'].choices = installer_choices
        print('post yes')
        if form.is_valid():
            print('valid')
            #selected_blocks = form.cleaned_data['blocks']
            #for block in selected_blocks:
            #    print(f"Selected Block: {block}")
            filtered_installers = installers[installers['state']== state]
            filtered_installers_names = filtered_installers['name'][:20]
            selected_blocks = request.session.get('selected_blocks')
            state_filtered = data[data['state']== state]
            district_filtered = state_filtered[state_filtered['district']== district]
            condition = data['block'] == selected_blocks[0]
            for value in selected_blocks[1:]:
                condition |= data['block'] == value
            filtered_df = data[condition]
            bes_names = list(filtered_df['name'])
            bes_choices = [ (f'{name}', f'{name}') for name in bes_names]

            bes_form = BesForm()
            bes_form.fields['bes'].choices = bes_choices
            request.session['bes_choices'] = bes_choices

            installer_initials = {'installer': f'{selected_installer}'}
            installers_form = InstallerForm(initial=installer_initials)
            installers_form.fields['installer'].choices = [(f'{selected_installer}', f'{selected_installer}')]
            #installers_choices = [(f'{ins}', f'{ins}') for ins in filtered_installers_names]
            #installers_form.fields['installer'].choices = installers_choices


            state_initials = {'state':state}
            state_form = StateForm(initial=state_initials)
            #state_form.fields['state'] = state


            district_initials = {'district': district}
            district_form = DistrictForm(initial=district_initials)

            block_initials = selected_blocks
            block_form = BlockForm(initial={'blocks': selected_blocks})
            block_form.fields['blocks'].choices = block_choices
            state_form.fields['state'].widget.attrs['id'] = 'inputfield'
            district_form.fields['district'].widget.attrs['id'] = 'inputfield'
            block_form.fields['blocks'].widget.attrs['id'] = 'inputfield'
            installers_form.fields['installer'].widget.attrs['id'] = 'inputfield'
            bes_form.fields['bes'].widget.attrs['id'] = 'inputfield'

            return render(request, 'bes.html', {'installers_form': installers_form, 'state_form': state_form, 'district_form': district_form, 'block_form':block_form, 'bes_form':bes_form})
        else:
            print('invalid')
            # Form is invalid, handle the errors
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Error in field {field}: {error}")
            return HttpResponse('form is invalid')
    else:
        return redirect('dashboard')

def create_pdf(request, task_id):
    if request.method == 'POST':
        form = final_form(request.POST, request.FILES)

        if form.is_valid():
            task = TaskAssigned.objects.get(pk= task_id)
            uploaded_file = request.FILES['picture']
            #fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            #filename = fs.save(uploaded_file.name, uploaded_file)
            unique_filename = str(uuid.uuid4()) + os.path.splitext(uploaded_file.name)[1]
            bes_mobile = request.POST.get('beneficiary_mobile')
            print('bes mobile', bes_mobile)
            request.session['bes_mobile'] = bes_mobile
            # Define the storage location (change as needed)
            storage_location = os.path.join(settings.MEDIA_ROOT, 'temp_images')

            # Create the storage location directory if it doesn't exist
            os.makedirs(storage_location, exist_ok=True)

            # Save the uploaded image to the temporary location
            with open(os.path.join(storage_location, unique_filename), 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Pass the URL of the temporary image to the template
            temp_image_url = os.path.join(settings.MEDIA_URL, 'temp_images', unique_filename)
            data = form.cleaned_data.items()
            print(data)


            otp = random.randint(1000, 9999)
            account_sid = 'AC4c9bfc6f4103167c9f3b877fa6a17ef9'
            auth_token = 'e54483ea0c5268452daf8dab376fdfd7'
            twilio_phone_number = '+15128656284'

            client = Client(account_sid, auth_token)

            otp = str(random.randint(100000, 999999))

            phone_number = str(task.beneficiary.mobile)

            try:
                message = client.messages.create(
                    body=f'Your Passcode is: {otp}',
                    from_=twilio_phone_number,
                    to=phone_number)
                print('success', message.sid)
            except Exception as e:
                print('exception occured')


            request.session['required_otp'] = str(otp)
            print('otp', otp)

            messages.success(request, f'OTP sent successfully')
            return render(request, 'create_pdf.html', {'data': data, 'temp_image_url': temp_image_url})

        else:
            print('invalid')
            # Form is invalid, handle the errors
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Error in field {field}: {error}")
            messages.error(request,'error in creating pdf')
        return redirect('user_dashboard')
    else:
        messages.error(request,'request Method is get')
        return redirect('user_dashboard')

def final_verification(request):
    if request.method == 'POST':
        bes_mob = request.session.get('bes_mobile')
        bes = BeneficiaryModel.objects.get(mobile = bes_mob)
        print('bes', bes)

        entered_otp = request.POST.get('entered_otp')
        otp = request.session.get('required_otp')
        print(otp)
        print(entered_otp)
        if entered_otp == otp:
            object = TaskAssigned.objects.get(beneficiary=bes)
            print('object', object)
            object.completion = 'Installation Done!'
            object.save()
            installer = object.installer
            installer_obj = InstallerModel.objects.get(installer=installer)
            # del request.session['otp']


            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="sample.pdf"'
            pdf_path = os.path.join(settings.MEDIA_ROOT, 'sample.pdf')
            with open(pdf_path, 'wb') as pdf_file:
                c = canvas.Canvas(pdf_file, pagesize=letter)
                default_margin = 0.10 * inch
                c.topMargin = default_margin
                c.bottomMargin = default_margin
                c.leftMargin = default_margin
                c.rightMargin = default_margin

                c.setFont("Times-Roman", 20)
                c.drawString(50, 700, "Beneficiary Data")

                c.setFont("Times-Roman", 12)
                c.drawString(80, 670, f"Name : {object.beneficiary.name}")
                c.drawString(80, 650, f"Mobile: {object.beneficiary.mobile}")
                c.drawString(80, 630, f"Pincode: {object.beneficiary.pincode}")

                c.setFont("Times-Roman", 20)
                c.drawString(50, 600, "Installer Data")

                c.setFont("Times-Roman", 12)
                c.drawString(80, 570, f"Name : {installer_obj.name}")
                c.drawString(80, 550, f"Mobile: {installer_obj.mobile}")
                c.drawString(80, 530, f"Pincode: {installer_obj.pincode}")
                c.save()

            messages.success(request, 'Installation Successfully Done!')
            return redirect('user_dashboard')
        else:
            messages.error(request, 'otp is wrong please try again')
            return redirect('user_dashboard')
    else:
        return HttpResponse('get method')















