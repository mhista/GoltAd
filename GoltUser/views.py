from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,reverse,redirect
from django.urls import reverse_lazy
from .forms import CreateCompany, CreateProfile, CreateAd
from django.views import View, generic
from .models import AdType, Ad, Company,UserProfile,Package,AdRange,Profile
from .mixins import AdCreatePerm,CompanyAccessPerm
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from allauth.account.views import SignupView
from django.contrib.auth.models import User


# landing page
class LandingPage(generic.TemplateView):
    template_name = 'landing.html'

# for referred users
class RefSignupView(SignupView):
    def get(self, request, *args, **kwargs):
        ref_code = kwargs['ref_code']
        self.ref_code.append(ref_code)
        print(self.ref_code[0])
        context = {'ref_code':ref_code}
        return render(request,'account/ref-signup.html',context)
    def form_valid(self, form):
        self.user=form.save(self.request)
        return self.get_success_url()
    def get_success_url(self):
        user_ref = User.objects.get(profile__code=self.ref_code[0])
        print(self.ref_code[0])
        print(self.user.username)
        new_user_profile = Profile.objects.get(user__id=self.user.id)
        new_user_profile.recommended_by = user_ref
        print(new_user_profile.recommended_by)
        new_user_profile.save()
        return redirect(reverse_lazy("golt:create-profile"))
    # def ad_user_ref(self):
        
    #     new_user = User.objects.get(id=self.instance.id)
    #     ref_user = Profile.objects.get(code=ref_code)
    #     print(ref_user)
    #     new_profile = Profile.objects.get(user=new_user)
    #     print(new_profile)
    #     new_profile.recommended_by = ref_user
    #     print(new_profile.recommende_byp)
    #     new_profile.save()
    #     return self.get_success_url()
        
        
        
# homepage
class indexView(LoginRequiredMixin, View):
    def get(self,request,*args,**kwargs):
        query = Ad.objects.all()
        context={'query':query}
        # userprofile = UserProfile

        return render(request,'index.html',context)

# viewing the ads
class AdTypeView(LoginRequiredMixin, generic.ListView):
    template_name = 'cat_choice.html'
    context_object_name = 'adtype'
    
    def get_queryset(self):
        self.queryset = AdType.objects.reverse()
        return self.queryset
    def get_context_data(self,**kwargs):
        request = self.request.user.userprofile
        context = super(AdTypeView,self).get_context_data(**kwargs)
        queryset = AdType.objects.all()
        for query in queryset:
            
            if request in query.user.all():
                subscribed = True
            else:
                subscribed = False
        context['subscribed'] =subscribed
        return context
    
# selecting category
class selectCategory(LoginRequiredMixin,CompanyAccessPerm, View):
    def get(self,request,pk,*args,**kwargs):
        adtype = AdType.objects.get(id=pk)
        user = request.user
        adtype.user.add(user.userprofile)
      
        messages.success(request, 'category selected,Visit Ads belonging to this category to earn')
        return redirect(reverse('golt:categories'))
# unselecting category
class UnSelectCategory(LoginRequiredMixin,CompanyAccessPerm, View):
    def get(self,request,pk,*args,**kwargs):
        adtype = AdType.objects.get(id=pk)
        user = request.user
        adtype.user.remove(user.userprofile)  
        messages.info(request,'you have removed this category. You cant visit Ads related to it')      
        return redirect(reverse('golt:categories'))
    
#Ad CreateView
class AdCreateView(LoginRequiredMixin,AdCreatePerm,generic.CreateView):
    form_class = CreateAd
    template_name = 'create-ad.html'
    model = Ad
    def form_valid(self,form):
        form = form.save(commit=False)
        form.package_type = form.ad_range.package
        form.company = self.request.user.userprofile.company
        form.save()
        self.request.user.userprofile.has_company = True
        return super(AdCreateView,self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(AdCreateView,self).get_context_data(**kwargs)
        context['ranges'] = AdRange.objects.all()
        context['category'] = AdType.objects.all()
        return context
    def get_success_url(self):
        messages.success(self.request, 'Ad created successfully')
        return reverse('index')
    
    
# AD details
class AdDetailView(LoginRequiredMixin,generic.DetailView):
    model = Ad
    template_name = 'ad-details.html'
    context_object_name = 'ad'

# checking ads
class ADcheck(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        pk = kwargs['pk']
        ad_pk = kwargs['ad_pk']
        ad_model = get_object_or_404(Ad,id=ad_pk)
        url = ad_model.company.company_url
        user = request.user.userprofile
        package = user.package
        if user == ad_model.company.userprofile:
            """checks if the user own the company"""
            return redirect(reverse('index'))
        elif user in ad_model.users.all():
            """ checks if the user has already clicked this add """
            messages.warning(request,'This Ad has been visited by you')
            return redirect(reverse('index'))
        elif user not in ad_model.ad_type.user.all():
            """checks if the user belongs to this category"""
            messages.info(request,'you dont belong to this category, you can join this category in the category page')
            return redirect(reverse('golt:categories'))
        else:
            """ if user passes all test, this algorithm runs, gets the package the user belongs in"""
            counts = user.clicks_per_day
            ad_count =  package.max_ad_per_day
            ad_counter = int(ad_count)
            if counts >= ad_counter:
                counts = ad_counter
                messages.info(request,'you have exceeded your daily limit')
                return redirect(reverse('index'))
            ad_model.users.add(user)
            user.points_earned += package.package_point
            user.clicks_per_day +=1
            user.save()
            messages.success(request,f'you have earned {package.package_point} points , check details in profile')
            return redirect(reverse_lazy('index'))
            
#AdDeleteView
class AdDelete(LoginRequiredMixin,generic.DeleteView):
    model = Ad
    def get_success_url(self):
        return reverse('index')

# creating profile
class CreateProfileView(LoginRequiredMixin,generic.CreateView):
    template_name= 'create-profile.html'
    model = UserProfile
    form_class = CreateProfile
    def form_valid(self, form):
        the_user = Profile.objects.get(user__id=self.request.user.pk)
        form =form.save(commit=False)
        form.profile = self.request.user.profile
        the_user.has_profile=True
        the_user.save()
        form.user = self.request.user
        form.save()
        return super(CreateProfileView,self).form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request,'your profile was successfully created')
        return reverse('index')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['package'] = Package.objects.all()
        return context
    
# updating the user profile
class ProfileUpdateView(LoginRequiredMixin,generic.UpdateView):
    template_name = 'create-profile.html'
    context_object_name = 'profile'
    form_class = CreateProfile
    model = UserProfile
    
    def get_success_url(self):
        messages.success(self.request,'your profile have been updated')
        return reverse('index')
    def form_invalid(self, form):
        messages.info(self.request, 'all fields are required, image field is optional, type in old values to reuse them')
        return super().form_invalid(form)

# deletes user profile
def profile_delete(request,pk):
    profile=UserProfile.objects.get(id=pk)
    profile.delete()
    request.user.is_active = False
    return redirect(reverse_lazy(''))
    
    
    
#creating ads   
class CreateCompanyView(LoginRequiredMixin,CompanyAccessPerm, generic.CreateView):
    form_class = CreateCompany
    model = Company
    template_name = 'create-company.html'
    def form_valid(self,form):
        form = form.save(commit=False)
        userprofile = self.request.user.userprofile
        the_user = Profile.objects.get(user__id=self.request.user.pk)
        if form.use_profile:
            form.state = userprofile.state
            form.country = userprofile.country
            form.zip = userprofile.zip
            form.phone = userprofile.phone
            form.user = self.request.user
            form.userprofile = userprofile
            form.save()
            the_user.has_company = True
            the_user.save()
            messages.success(self.request,'your business was successfully added')
            return super(CreateCompanyView,self).form_valid(form)
        form.userprofile = userprofile
        form.save()
        the_user.has_company = True
        the_user.save()
        messages.success(self.request,'your business was successfully added')
        return super(CreateCompanyView,self).form_valid(form)
    
    def get_success_url(self):
        return reverse('index')
    
# update company info
class CompanyUpdateView(LoginRequiredMixin,CompanyAccessPerm,generic.UpdateView):
    template_name = 'create-company.html'
    context_object_name = 'company'
    form_class = CreateCompany
    model = Company
    
    def get_success_url(self):
        return reverse('golt:company',kwargs= {'pk':self.pk_url_kwarg})
    
# delete company   
class CompanyDelete(LoginRequiredMixin,CompanyAccessPerm,generic.DeleteView):
    model = Company
    def get_success_url(self):
        return reverse('index')
class UserProfileView(LoginRequiredMixin,CompanyAccessPerm,generic.DetailView):
    template_name = 'profile.html'
    context_object_name = 'pro'
    model = UserProfile

class CompanyView(LoginRequiredMixin,CompanyAccessPerm,generic.DetailView):
    template_name = 'company.html'
    context_object_name = 'comp'
    model = Company