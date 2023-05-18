from django.contrib import admin

# Register your models here.

from .models import PayModel
admin.site.register(PayModel)