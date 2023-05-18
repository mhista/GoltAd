from django.urls import path,include
from .views import AdTypeView,selectCategory,UnSelectCategory, AdDetailView, ADcheck,CreateCompanyView,AdCreateView,ProfileUpdateView,CompanyUpdateView,CreateProfileView,UserProfileView,profile_delete,CompanyView

app_name = 'golt'

urlpatterns = [
    path('categories/', AdTypeView.as_view(), name='categories'),
    path('create-company/', CreateCompanyView.as_view(), name='create-company'),
    path('select_category/<int:pk>', selectCategory.as_view(), name='cat-select'),
    path('unselect_category/<int:pk>', UnSelectCategory.as_view(), name='cat-unselect'),
    path('profile/<int:pk>', ProfileUpdateView.as_view(), name='update-profile'),
    path('profile-delete/<int:pk>',profile_delete,name='profile-delete'),
    path('update-company/<int:pk>', CompanyUpdateView.as_view(), name='update-company'),
    path('<int:pk>/detail/', AdDetailView.as_view(), name='ad-detail'),
    path('<int:pk>/<int:ad_pk>/detail/', ADcheck.as_view(), name='adcheck'),
    path('create-ad/', AdCreateView.as_view(), name='create-ad'),
    path('profile/', CreateProfileView.as_view(), name='create-profile'),
    path('company/', CreateCompanyView.as_view(), name='create-company'),
    path('user-profile/<int:pk>', UserProfileView.as_view(), name='profile'),
    path('company/<int:pk>', CompanyView.as_view(), name='company'),
    
    
    
    
    
    
    
    ]