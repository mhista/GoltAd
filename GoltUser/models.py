from django.db import models
# from django_countries.fields import CountryField
from django.contrib.auth import get_user_model
from django.conf import settings
from .files import profile_upload,ad_uploads,company_upload, generate_ref_code
from django.db.models.signals import post_save
from django.shortcuts import reverse,redirect

User = settings.AUTH_USER_MODEL

user = get_user_model()
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    has_company = models.BooleanField(default=False)
    has_profile = models.BooleanField(default=False)
    recommended_by = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name='ref_by')
    code = models.CharField(max_length=12,blank=True)
       
    def __str__(self):
        return f'{self.user.username} - {self.code}'
    def get_recommend_profiles(self):
        return self.recommended_by
    
    def save(self,*args,**kwargs):
        if self.code == '':
            code = generate_ref_code()
            self.code = code
        super().save(*args,**kwargs)
   
  
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile = models.OneToOneField(Profile,on_delete=models.CASCADE,related_name='profile')
    package = models.ForeignKey('Package',on_delete=models.SET_NULL, blank=True,null=True,related_name='package')
    state = models.CharField(max_length=150,null=True)
    country = models.CharField(max_length=150,null=True)
    zip = models.CharField(max_length=150,null=True)
    phone = models.CharField(max_length=150,null=True)
    points_earned = models.IntegerField(default=0)
    clicks_per_day = models.IntegerField(default=0)
    total_ads = models.IntegerField(default=0)
    photo = models.ImageField(upload_to=profile_upload,null=True)
    # updated = models.DateTimeField(auto_now = True)
    # created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.user.username
    def name(self):
        return self.user.username

    
    
class Company(models.Model):
    userprofile = models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    company_name = models.CharField(max_length=150)
    company_address = models.CharField(max_length=150)
    company_url = models.CharField(max_length=150, verbose_name='website address')
    state = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=150, blank=True)
    zip = models.CharField(max_length=150, blank=True)
    use_profile = models.BooleanField(default=False)
    phone = models.CharField(max_length=150, blank=True)
    email =  models.CharField(max_length=150)
    photo = models.ImageField(upload_to=company_upload, null=True)
    
    # def get_absolute_url(self):
    #     return reverse('golt:create-company', kwargs={'pk':self.pk})
        
    
    
    def __str__(self):
        return f'{self.company_name} by {self.userprofile.user.username}'
    
# the different kinds 
class AdType(models.Model):
    name = models.CharField(max_length=200) 
    user = models.ManyToManyField(UserProfile, blank=True)
   
    def __str__(self):
        return self.name 
    def get_count(self):
        return self.user.count()
    

class Ad(models.Model):
    name = models.CharField('Ad name' ,max_length=100)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    ad_description = models.TextField(verbose_name='your advert description')
    ad_type = models.ForeignKey(AdType,on_delete=models.CASCADE)
    users = models.ManyToManyField(UserProfile,blank=True)
    ad_link = models.CharField(max_length=250,verbose_name='ad link')
    ad_range = models.ForeignKey('AdRange', on_delete=models.CASCADE)
    package_type = models.ForeignKey('Package', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=ad_uploads, null=True)
    
    
    def get_ad_company(self):
        return self.company.company_name
    def get_ad_count(self):
        return self.users.count()
    def ad_name(self):
        if len(self.name) > 40:
            return self.name[0:40]
        return self.name
    

class AdRange(models.Model):
    package = models.OneToOneField('Package',on_delete=models.CASCADE,related_name='range')
    number_of_clicks = models.IntegerField('number of visit', default=0)
    ad_price = models.IntegerField(default=0)
    
    
    def __str__(self):
        return f'{self.package.name} Ads    '
    
    
        
class Package(models.Model):
    name = models.CharField(max_length=50)
    percentage_per_ref = models.FloatField()
    percentage_per_comp_ref = models.FloatField()
    max_ad_per_day = models.CharField(max_length=20)
    package_point = models.IntegerField(default=0)
    # user_target = models.IntegerField(default=0)
    
    
    
    def __str__(self):
        return self.name
    
class Coupon(models.Model):
    refCode = None
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)

def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User)