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
    path('form_teacher',views.addTeach,name="form_teachers"),

    path('upload-results/', views.upload_results, name='upload_results'),
    path('delete_result/<int:result_id>/',views.delete_result,name='delete_result') , 

    path('student_signup/',views.signup_view,name='student_signup'),
    
    path('login/',views.login_view,name='login'), 
    path('teacher_signup/',views.teachers_view,name="teacher_signup"),

    path('general_login',views.general_login,name="general_login"), 
    path('general_signup',views.general_signup,name="general_signup"),  


    # path('teacher_login/',views.teachers_login_view,name='teachers_login'),

    path('teacher_dashboard/',views.teachers_dashboard,name='teacher_dashboard'),

    path('my-results/', views.student_results, name='student_results'),

    path('download_result/',views.downloadResult,name='download_result') ,
    

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
