# Generated by Django 4.2.5 on 2023-09-18 23:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddApp', '0002_alter_beneficiarymodel_mobile'),
    ]

    operations = [
        migrations.CreateModel(
            name='SetupInstallerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('address', models.CharField(max_length=128)),
                ('pincode', models.CharField(max_length=6, validators=[django.core.validators.RegexValidator('^\\d{6}$', 'Enter a valid 6-digit PIN code.')])),
                ('identity_proof', models.ImageField(upload_to='')),
            ],
        ),
        migrations.AlterField(
            model_name='beneficiarymodel',
            name='pincode',
            field=models.CharField(max_length=6, validators=[django.core.validators.RegexValidator('^\\d{6}$', 'Enter a valid 6-digit PIN code.')]),
        ),
    ]
