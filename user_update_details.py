from ddApp.models import User, InstallerModel

users = User.objects.all()

for user in users:
    if user.is_superuser :
        pass
    else:
        instance = InstallerModel.objects.get(installer=user)
