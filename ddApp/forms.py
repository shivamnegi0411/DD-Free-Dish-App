import pandas as pd
from django import forms
from .models import TaskAssigned
from .models import SetupBoxInfo
from .models import InstallerModel, BeneficiaryModel
from django.contrib.auth.forms import AuthenticationForm


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'id': 'custom_username', 'placeholder': 'Enter Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'custom_password', 'placeholder': 'Enter Password'}))


class TaskAssignedForm(forms.ModelForm):
    class Meta:
        model = TaskAssigned
        fields = ['installer', 'beneficiary']


class SetupBoxInfoForm(forms.Form):
    task_field = forms.CharField(max_length=64, widget=forms.HiddenInput)
    beneficiary = forms.CharField(max_length=64)

    setup_box = forms.CharField(
        max_length=32,
        required=True,
        label='Enter New Setup Box Serial No.',
        widget=forms.TextInput(attrs={'placeholder': 'Enter New Setup Box Serial No.'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['beneficiary'].widget.attrs['id'] = 'beneficiary-field'
        self.fields['setup_box'].widget.attrs['id'] = 'setup-box-field'



class verify_passcode(forms.Form):
    task_field = forms.CharField(max_length=64, widget=forms.HiddenInput)
    beneficiary = forms.CharField(max_length=64)

    setup_box = forms.CharField(
        max_length=32,
        required=True,
        label='Enter New Setup Box Serial No.',
    )
    otp = forms.CharField(
        max_length=64,
        widget=forms.NumberInput(attrs={'placeholder':'Enter OTP'})
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['beneficiary'].widget.attrs['id'] = 'beneficiary-field'
        self.fields['setup_box'].widget.attrs['id'] = 'setup-box-field'
        self.fields['otp'].widget.attrs['id'] = 'otp'


class final_form(forms.Form):
    time = forms.TimeField()
    date = forms.DateField()
    installer_name = forms.CharField(max_length=128)
    installer_address = forms.CharField(max_length=128)
    installer_mobile = forms.CharField(max_length=13)
    beneficiary_name = forms.CharField(max_length=128)
    beneficiary_address = forms.CharField(max_length=128)
    beneficiary_mobile = forms.CharField(max_length=13)
    device_info = forms.CharField(max_length=255)
    device_location = forms.CharField(max_length=255)
    picture = forms.ImageField(
        label='Take a picture',
        # help_text='Allowed formats: JPG, PNG, GIF',
        widget=forms.ClearableFileInput(attrs={'accept': 'image/*', 'capture': 'camera'}),
    )

    def __init__(self, *args, **kwargs):
        super(final_form, self).__init__(*args, **kwargs)
        self.fields['device_location'].widget.attrs['id'] = 'id_device_location'
        self.fields['picture'].widget.attrs['id'] = 'picture'


installer_objects = InstallerModel.objects.all()
beneficiary_objects = BeneficiaryModel.objects.all()
df = pd.DataFrame(list(installer_objects.values()))
df_b = pd.DataFrame(list(beneficiary_objects.values()))


class StateForm(forms.Form):
    # installer_choices = ( (f'{user}', f'{user}') for user in df['name'] )
    # installers = forms.ChoiceField(choices = installer_choices)
    state_choices = ((f'{state}', f'{state}') for state in df_b['state'].unique())
    state = forms.ChoiceField(choices=state_choices, required=True, initial=[])


class DistrictForm(forms.Form):
    district = forms.ChoiceField(choices=(), required=True, initial=[])



class BlockForm(forms.Form):
    blocks = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=[],
        required=True
    )


class BesForm(forms.Form):
    bes = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=[], required=True
    )


class InstallerForm(forms.Form):
    installer = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=(), required=True
    )
