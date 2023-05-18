"""GoltAd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView
    
)
from GoltUser.views import LandingPage,indexView,RefSignupView
from allauth.account.views import LoginView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', indexView.as_view(), name='landing-page'),
    path('accounts/', include('allauth.urls')),
    path('accounts/<str:ref_code>/', RefSignupView.as_view(),name='ref-signup'),
    path('index/', indexView.as_view(),name='index'),
    
    # path('login/', LoginView.as_view(), name='login'),
    path('goldburry/', include('GoltUser.urls',namespace='golt')),
    path('mgt/', include('UserMgt.urls',namespace='mgt'))
    
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)