from ddApp.models import BeneficiaryModel
import random

all = BeneficiaryModel.objects.all()
num=0
for obj in all:
    mob = random.randint(9000000000, 9999999999)
    mob = str(mob)
    obj.mobile = mob
    pin = random.randint(111199, 999999)
    obj.pincode = pin
    num+=1
    print(obj, mob, pin, num)
    obj.save()