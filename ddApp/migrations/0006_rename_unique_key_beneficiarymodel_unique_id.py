# Generated by Django 4.2.5 on 2023-09-18 23:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ddApp', '0005_alter_beneficiarymodel_unique_key_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='beneficiarymodel',
            old_name='unique_key',
            new_name='unique_id',
        ),
    ]