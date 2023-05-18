from .views import InitiatePayment,VerifyPayment,VerifyAccount
from django.urls import path
app_name = 'mgt'

urlpatterns = [
    path('',InitiatePayment.as_view(), name="initiate-payment"),
    path('<str:ref>/', VerifyPayment.as_view(), name="verify-payment"),
    path('<int:pk>/verify_account/', VerifyAccount.as_view(), name="verify-account"),
    
    
]