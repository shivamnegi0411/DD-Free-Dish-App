from ddApp.models import BeneficiaryModel

aru  = BeneficiaryModel.objects.filter(state = 'NAGALAND\n')

for obj in aru:
    obj.state = 'NAGALAND'
    obj.save()
