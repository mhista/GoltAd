# Generated by Django 3.2.5 on 2022-08-25 10:39

import GoltUser.files
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GoltUser', '0002_auto_20220825_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=GoltUser.files.uploaded_files_directory),
        ),
    ]
