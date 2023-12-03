from random import randint

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

random = randint(100000, 999999)

urlpatterns = [
    path('', views.Index, name='index'),
    path('about/', views.aboutView, name='about'),
    path('contact/', views.contactView, name='contact'),
    path('user_dashboard/', views.HomePage.as_view(), name='user_dashboard'),
    path('profile/', views.Profile, name='profile'),
    path('change_task_status/<int:task_id>/', views.change_task_status, name='change_task_status'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('logout_confirmation/', views.logout_view, name='logout_confirmation'),
    path('create_task/', views.CreateTask.as_view(), name='CreateTask'),
    path('make_task/', views.make_task, name='make_task'),
    path('process_page/<int:task_id>/', views.ProcessPage.as_view(), name='process_page'),
    path(f'verify_otp/{random}/<int:task_id>/', views.verify_otp, name='verify_otp'),
    path('confirm/passcode/<str:task_id>/', views.confirm_passcode, name='confirm_passcode'),
    path('get_geo/', views.get_geo, name='get_geo'),
    path('create_pdf/<str:task_id>/', views.create_pdf, name='create_pdf'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('district/', views.State.as_view(), name='district'),
    path('blocks/', views.Blocks.as_view(), name='blocks'),
    path('select_installer/', views.Ins, name='select_installer'),
    path('beneficiary/', views.Bes, name='bes'),
    path('assign/', views.Assign, name='assign'),
    path('final_verification/', views.final_verification, name='final_verification'),
    path('superuser_dashboard/', views.superuser_dashboard, name='superuser_dashboard'),
    path('district_state/<str:id>/', views.DistrictState, name='district_state_data'),
    path('block_district_data/<str:id>/', views.BlockDistrict, name='block_district_data'),
    path('bes_block/<str:id>/', views.BesBlock, name='bes_block'),
    path('tasks_/<str:status>/', views.filtered_Bes_block, name='filtered_bes_block'),
    path('about_bes/<str:bes_id>/', views.aboutBesView, name='about_bes'),
    path('about_ins/<str:ins_id>/', views.aboutInsView, name='about_ins'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
