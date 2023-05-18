from django.forms import ModelForm, Form
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import AdType, Company, Ad, UserProfile
from django_countries.fields import CountryField
from allauth.account.forms import SignupForm
user = get_user_model()

class CreateCompany(ModelForm):
    country = CountryField()
    class Meta:
        model = Company
        fields = ['company_name','company_address','company_url', 'state', 'country','zip','use_profile','phone','email','photo']
    
class CreateAd(ModelForm):
    class Meta:
        model  = Ad
        fields = ('name','ad_description','ad_link','ad_type','ad_range','photo')

class CreateProfile(ModelForm):
    class Meta:
        model  = UserProfile
        fields = ['state','country','zip','phone','photo']

