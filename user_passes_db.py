from ddApp.models import User
import pandas as pd


df = pd.read_csv('user_passes.csv')

for i in range(len(df)):
    user = df.iloc[i]['users']
    password = df.iloc[i]['passwords']
    User.objects.create_user(username=user, password=password)



