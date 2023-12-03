from ddApp.models import BeneficiaryModel
import pandas as pd

names = pd.read_csv('beneficiay_names.csv')
names = names.sort_values('Father Name')
addresses = pd.read_csv('state_data.csv')
done = 0
for line in range(len(addresses)):
    num = addresses.iloc[line]['Assigned ']
    for i in range(done, done + num):
        instance = BeneficiaryModel(name=names.iloc[i]['Name'], father_name_spouse_name=names.iloc[i]['Father Name'],
                         state=addresses.iloc[line]['Name of State'], district= addresses.iloc[line]['Name of District'],
                         block= addresses.iloc[line]['Name of Block'])
        instance.save()
    done += num
    print(done)
