# Generated by Django 4.2.5 on 2023-09-20 00:24

import django.core.validators
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('ddApp', '0018_remove_taskassigned_beneficiary_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeneficiaryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=64)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], max_length=8)),
                ('father_name', models.CharField(max_length=64)),
                ('address', models.CharField(max_length=128)),
                ('pincode', models.CharField(max_length=6, validators=[django.core.validators.RegexValidator('^\\d{6}$', 'Enter a valid 6-digit PIN code.')])),
                ('identity_proof', models.CharField(blank=True, max_length=32, null=True)),
                ('type_beneficiary', models.CharField(max_length=16)),
                ('mobile', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='IN')),
            ],
        ),
    ]
