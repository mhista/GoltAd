from django.contrib import admin
from . models import( AdType, UserProfile,
Company,
Package,
Ad,
AdRange,
Profile
)
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Package)
admin.site.register(Company)
admin.site.register(AdType)
admin.site.register(Ad)
admin.site.register(AdRange)
admin.site.register(Profile)


# admin.site.register(AdCategories)


