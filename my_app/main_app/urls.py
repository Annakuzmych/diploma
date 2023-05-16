from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user='profile'), name='profile'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    path('user_login/', views.user_login, name='user_login'),
    path('donors/', views.donor_list, name='donor_list'),
    path('donors/add/', views.add_donor, name='add_donor'),
    path('blood-request/create/<int:donor_id>/', views.create_blood_request, name='create_blood_request'),
    path('donors/<int:donor_id>/', views.donor_detail, name='donor_detail'),
    path('donor/<int:donor_id>/donations/', views.donor_donations, name='donor_donations'),
    path('donation/<int:donation_id>/', views.donation_details, name='donation_details'),
    path('donation/<int:donation_id>/create_rejection/', views.create_rejection, name='create_rejection'),
    path('donation/show_rejections/', views.show_rejections, name='show_rejections'),

]