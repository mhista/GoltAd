# Generated by Django 3.2.5 on 2022-08-25 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GoltUser', '0003_alter_ad_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Ad name'),
        ),
    ]