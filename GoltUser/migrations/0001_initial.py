# Generated by Django 3.2.5 on 2022-08-25 00:27

import GoltUser.files
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('percentage_per_ref', models.FloatField()),
                ('percentage_per_comp_ref', models.FloatField()),
                ('max_ad_per_day', models.CharField(max_length=20)),
                ('package_point', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_profile', models.BooleanField(default=False)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=150, null=True)),
                ('country', models.CharField(max_length=150, null=True)),
                ('zip', models.CharField(max_length=150, null=True)),
                ('phone', models.CharField(max_length=150, null=True)),
                ('points_earned', models.IntegerField(default=0)),
                ('clicks_per_day', models.IntegerField(default=0)),
                ('has_company', models.BooleanField(default=False)),
                ('total_ads', models.IntegerField(default=0)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=GoltUser.files.uploaded_files_directory)),
                ('package', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userprofile', to='GoltUser.package')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='GoltUser.profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=150)),
                ('company_address', models.CharField(max_length=150)),
                ('company_url', models.CharField(max_length=150, verbose_name='website address')),
                ('state', models.CharField(blank=True, max_length=150)),
                ('country', models.CharField(blank=True, max_length=150)),
                ('zip', models.CharField(blank=True, max_length=150)),
                ('use_profile', models.BooleanField(default=False)),
                ('phone', models.CharField(blank=True, max_length=150)),
                ('email', models.CharField(max_length=150)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=GoltUser.files.company_files_directory)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='GoltUser.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='AdType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('user', models.ManyToManyField(blank=True, to='GoltUser.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='AdRange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_clicks', models.IntegerField(default=0, verbose_name='number of visit')),
                ('ad_price', models.IntegerField(default=0)),
                ('package', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='range', to='GoltUser.package')),
            ],
        ),
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Ad name')),
                ('ad_description', models.TextField(verbose_name='your advert description')),
                ('ad_link', models.CharField(max_length=250, verbose_name='ad link')),
                ('photo', models.ImageField(blank=True, null=True, upload_to=GoltUser.files.ad_files_directory)),
                ('ad_range', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GoltUser.adrange')),
                ('ad_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GoltUser.adtype')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GoltUser.company')),
                ('package_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GoltUser.package')),
                ('users', models.ManyToManyField(blank=True, to='GoltUser.UserProfile')),
            ],
        ),
    ]
