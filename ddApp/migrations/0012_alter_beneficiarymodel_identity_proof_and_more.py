# Generated by Django 4.2.5 on 2023-09-19 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddApp', '0011_alter_beneficiarymodel_identity_proof_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiarymodel',
            name='identity_proof',
            field=models.CharField(blank=True, default=None, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='installermodel',
            name='identity_proof',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
