from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.BeneficiaryModel)
admin.site.register(models.InstallerModel)
admin.site.register(models.TaskAssigned)
admin.site.register(models.SetupBoxInfo)
