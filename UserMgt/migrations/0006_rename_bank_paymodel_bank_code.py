# Generated by Django 3.2.5 on 2022-09-14 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserMgt', '0005_auto_20220914_1635'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paymodel',
            old_name='bank',
            new_name='bank_code',
        ),
    ]