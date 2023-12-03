from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class BeneficiaryModel(models.Model):
    name = models.CharField(max_length=64,null=True, blank=True)
    gender_choices = (('Male','Male'), ('Female', 'Female'), ('Others', 'Others'))
    gender = models.CharField(max_length=8, choices=gender_choices, blank=True)
    father_name_spouse_name = models.CharField(max_length=64,null=True, blank=True)
    house_bldg_apt = models.CharField(max_length=32,null=True, blank=True)
    street_road_lane = models.CharField(max_length=64,null=True, blank=True)
    landmark = models.CharField(max_length=68,null=True, blank=True)
    area_locality_sector = models.CharField(max_length=64,null=True, blank=True)
    village_town_city = models.CharField(max_length=64,null=True, blank=True)
    block = models.CharField(max_length=64, null=True, blank=True)
    district = models.CharField(max_length=32,null=True, blank=True)
    post_office = models.CharField(max_length=64,null=True, blank=True)
    state = models.CharField(max_length=32,null=True, blank=True)
    pincode = models.CharField(max_length=6, validators=[
        RegexValidator(r'^\d{6}$', 'Enter a valid 6-digit PIN code.')
    ], null=True, blank=True)
    identity_proof = models.CharField(max_length=32, blank=True, null=True)
    type_beneficiary = models.CharField(max_length=16,null=True, blank=True)
    mobile = PhoneNumberField(region='IN', null=True, blank=True)

    def __str__(self):
        return self.name

class InstallerModel(models.Model):
    installer = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=64, null=True, blank=True)
    agency = models.CharField(max_length=64, null=True, blank=True)
    house_bldg_apt = models.CharField(max_length=32,null=True, blank=True)
    street_road_lane = models.CharField(max_length=64,null=True, blank=True)
    landmark = models.CharField(max_length=68,null=True, blank=True)
    area_locality_sector = models.CharField(max_length=64,null=True, blank=True)
    village_town_city = models.CharField(max_length=64,null=True, blank=True)
    district = models.CharField(max_length=32,null=True, blank=True)
    post_office = models.CharField(max_length=64,null=True, blank=True)
    state = models.CharField(max_length=32,null=True, blank=True)
    pincode = models.CharField(max_length=6, validators=[
        RegexValidator(r'^\d{6}$', 'Enter a valid 6-digit PIN code.')
    ], null= True, blank=True)
    identity_proof = models.CharField(max_length=32, blank=True, null=True)
    mobile = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.installer.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        InstallerModel.objects.create(installer=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        setup_installer_model = InstallerModel.objects.get(installer=instance)
        setup_installer_model.save()
    except InstallerModel.DoesNotExist:
        pass

class TaskAssigned(models.Model):
    installer = models.ForeignKey(User,on_delete=models.CASCADE)
    beneficiary = models.OneToOneField(BeneficiaryModel, on_delete=models.CASCADE)
    task_choices = (('Assigned','Assigned'), ('Intrans-it','Intrans-it'),('Initiated', 'Initiated'), ('Installation Done!', 'Installation Done!'))
    completion = models.CharField(max_length=64, choices=task_choices, default='Assigned')

    def __str__(self):
        return f"{self.installer} - {self.beneficiary} - task status {self.completion}"


class SetupBoxInfo(models.Model):
    sr_no = models.CharField(max_length=64)
    passcode =  models.CharField(max_length=6, validators=[
        RegexValidator(r'^\d{4}$', 'Enter a valid 6-digit PASSCODE code.')
    ], null= True, blank=True)
    beneficiary_registered = models.OneToOneField(BeneficiaryModel, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.sr_no

class Installed_Box_Info(models.Model):
    installer = models.ForeignKey(User, on_delete=models.CASCADE)
    beneficiary = models.ForeignKey(BeneficiaryModel, on_delete=models.CASCADE)
    device_info = models.CharField(max_length=255)
    device_location = models.CharField(max_length=255)
    picture = models.FileField()





