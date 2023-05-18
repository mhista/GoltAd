from django.shortcuts import render
from .forms import PaymentForm
from django.conf import settings
from .models import PayModel
from django.contrib import messages 
from django.shortcuts import get_object_or_404,redirect,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.request import HttpRequest
from django.views import generic,View
from django.http.response import HttpResponse


class InitiatePayment(LoginRequiredMixin,generic.CreateView):
    form_class = PaymentForm
    model = PayModel
    context_object_name = 'payment'
    template_name = 'initiate_payment.html'
    
    def form_valid(self, form):
        self.payment = form.save()
        return render(self.request, 'make_payment.html', {'payment':self.payment, 'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY})
   
    
class VerifyPayment(View):
    def get(self,*args,**kwargs):
        payment = get_object_or_404(PayModel,ref=kwargs['ref'])
        verified = payment.verify_payment()
        if verified:
            messages.success(self.request,"verification successful")
        else:
            messages.error(self.request, "verification failed")
        return redirect('initiate-payment')
    
# class CollectAccountNumber(LoginRequiredMixin,generic.CreateView):
#     form_class = PaymentForm
#     model = PayModel
#     context_object_name = 'payment'
#     template_name = 'resolve_payment.html'
    
#     def form_valid(self,form):
        
        
class VerifyAccount(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        account = get_object_or_404(PayModel,user__id=kwargs['pk'])
        print(account)
        verified = account.validate_account()
        if verified:
             messages.success(self.request,"verification successful")
             return redirect('index')
        else:
            messages.error(self.request, "verification failed")
            return redirect('mgt:initiate-payment')