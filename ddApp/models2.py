
class BeneficiaryModel(models.Model):
    name = models.CharField(max_length=64)
    gender_choices = (('Male','Male'), ('Female', 'Female'), ('Others', 'Others'))
    gender = models.CharField(max_length=8, choices=gender_choices, blank=True)
    father_name = models.CharField(max_length=64)
    address = models.CharField(max_length=128)
    pincode = models.CharField(max_length=6, validators=[
        RegexValidator(r'^\d{6}$', 'Enter a valid 6-digit PIN code.')
    ])
    identity_proof = models.CharField(max_length=32, blank=True, null=True)
    type_beneficiary = models.CharField(max_length=16)
    mobile = PhoneNumberField(region='IN')

    def __str__(self):
        return self.name

class InstallerModel(models.Model):
    installer = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=128, null=True)
    pincode = models.CharField(max_length=6, validators=[
        RegexValidator(r'^\d{6}$', 'Enter a valid 6-digit PIN code.')
    ], null= True)
    identity_proof = models.CharField(max_length=32, blank=True, null=True)
    mobile = PhoneNumberField(region='IN')
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
    installer = models.OneToOneField(User,on_delete=models.CASCADE)
    beneficiary = models.OneToOneField(BeneficiaryModel, on_delete=models.CASCADE)
    task_choices = (('Initiated','Initiated'), ('In Progress','In Progress'), ('Completed', 'Completed'))
    completion = models.CharField(max_length=16, choices=task_choices, default='Initiated')
