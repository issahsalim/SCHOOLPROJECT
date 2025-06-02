from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 
from .views import CustomPasswordResetView

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'), 
    path('logout', views.logoutFun, name='logout'),
    path('announcement', views.announcement, name='announcement'),
    path('absence', views.absence, name='absence'),

 
    # path('general_login',views.general_login,name="general_login"), 
    # path('general_signup',views.general_signup,name="general_signup"),  

    path('teachers_signup/',views.teacher_signup,name="teachers_signup"),

    # path('teacher_login/',views.teacher_login,name='teachers_login'), 



    path('upload-results/', views.upload_results, name='upload_results'),

    path('delete_result/<int:result_id>/',views.delete_result,name='delete_result') , 


     path('password_reset/',CustomPasswordResetView.as_view(
         template_name='reset_password.html',
         email_template_name="email_reset_password.html", 
         html_email_template_name="email_reset_password.html",
     ),name='password_reset'),  
    
    
     path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(
         template_name="reset_password_done.html",
         
     ),name="password_reset_done"),

     path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
         template_name="reset_password_confirm.html"
     ),name="password_reset_confirm"),

     path('reset/done/',auth_views.PasswordResetCompleteView.as_view(
          template_name="reset_password_complete.html"  
     ),name='password_reset_complete'),

     
]
