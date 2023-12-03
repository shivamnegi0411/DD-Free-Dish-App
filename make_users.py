from ddApp.models import User
import re, random, string, pandas as pd

df = pd.read_excel('IT.xlsx')

total = len(df)
periods = []
checkpoint = 0
all_values = pd.DataFrame()
for i in range(len(df)):
    if i == checkpoint:
        periods.append(checkpoint)
        checkpoint += 5000
    elif (len(df) - checkpoint) < 5000:
        periods.append(len(df))
        break
print(periods)
try:
    done = 0
    for check in periods:
        passes = {}
        state = []
        agency = []
        name = []
        mobile = []
        pincode = []
        for i in range(done, check):

            if re.search('[A-Za-z]{4,10}', df.iloc[i]['ASSOCIATE_NAME']):
                f = re.search('[A-Za-z]{3,10}', df.iloc[i]['ASSOCIATE_NAME']).group().lower()
            else:
                f = 'user'
            if df.iloc[i]['MOBILE_PHONE'] == '':
                l = str(df.iloc[i]['MOBILE_PHONE'][-4:])
            else:
                l = str(random.randint(1000, 9999))
            username = f + '@' + l

            n = random.choice([3, 4, 5])

            p1 = ''.join(random.choices(string.ascii_uppercase, k=1))

            p2 = ''.join(random.choices(string.ascii_lowercase, k=4))

            p3 = str(''.join(random.choices([str(i) for i in range(10)], k=n)))

            password = p1 + p2 + p3

            passes[username] = password
            state.append(df.iloc[i]['New Circle Name'])
            agency.append(df.iloc[i]['AGENCY'])
            name.append(df.iloc[i]['ASSOCIATE_NAME'])
            mobile.append((df.iloc[i]['MOBILE_PHONE']))
            pincode.append(df.iloc[i]['Pin Code'])



            done += 1
            print(done)
            print(username + ' : ' + password)
        data = pd.DataFrame()
        data['users'] = pd.Series(passes.keys())
        data['passwords'] = pd.Series(passes.values())
        data['name'] = pd.Series(name)
        data['agency'] = pd.Series(agency)
        data['state'] = pd.Series(state)
        data['mobile'] = pd.Series(mobile)
        data['pincode'] = pd.Series(pincode)
        all_values = pd.concat([all_values, data])


        #
except Exception as e:
    print(e)
#data.to_csv(f"users {done}.csv", index=True)
all_values.to_csv('user_passes.csv', index=True)
