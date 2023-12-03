from ddApp.models import User, InstallerModel
import pandas as pd

df = pd.read_csv('installers.csv')
users = User.objects.all()
supers = ['ashb8925', 'gautam', 'shivam', 'chirag2406']
done = 1
df = df.sort_values('users')

for line in range(len(df)):
    user = df.iloc[line]['users']
    user_instance = User.objects.get(username=user)
    instance = InstallerModel.objects.get(installer=user_instance)
    instance.name=df.iloc[line]['name']
    instance.agency=df.iloc[line]['agency']
    instance.state=df.iloc[line]['state']
    instance.mobile=df.iloc[line]['mobile']
    instance.pincode=df.iloc[line]['pincode']
    instance.save()
    print(f"{done} : {user}")
    done +=1
