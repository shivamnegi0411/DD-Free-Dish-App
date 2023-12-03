from django.db.models.functions import Upper

from ddApp.models import InstallerModel, BeneficiaryModel

InstallerModel.objects.update(state=Upper('state'))
BeneficiaryModel.objects.update(state=Upper('state'))
BeneficiaryModel.objects.update(district=Upper('district'))
BeneficiaryModel.objects.update(block=Upper('block'))
print('done')
