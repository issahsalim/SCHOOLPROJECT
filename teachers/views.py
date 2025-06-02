from django.shortcuts import render
from . models import *
from django.shortcuts import render,redirect,get_object_or_404
from .forms import * 
from .models import * 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login ,logout 
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse 
from django.contrib.auth.views import PasswordResetView 
from django.urls import reverse_lazy 
from django.core.mail import send_mail,BadHeaderError
from django.conf import settings
import smtplib   
from .task import send_email_fun,send_username_mail,teacher_id_mail
import csv 
# Create your views here. 

class CustomPasswordResetView(PasswordResetView):
    template_name = 'reset_password.html'
    email_template_name = "email_reset_password.html"
    success_url = reverse_lazy('password_reset_done')  

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        
        
        if TeacherUser.objects.filter(email=email).exists():     
            return super().form_valid(form)
        else:
            messages.error(self.request, "Email does not match any account")
            return self.form_invalid(form)


def base(request): 
    return render(request,'base.html')  


def home(request):  
    return render(request,'home.html')   


def index(request):
    return render(request,'index.html')


def teacher_signup(request):
    if request.method == "POST":
        form = TeacherSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role="teacher" 
            user.set_password(form.cleaned_data['password1'])   
            user.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect("login")  


    else:
        form = TeacherSignupForm()
    return render(request, "teachers/signup.html", {"form": form})
    
    
def teacher_login(request):
    if request.method == "POST":
        form = TeacherLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try: 
                user = TeacherUser.objects.get(email=email)
                if user.check_password(password):
                    request.session['teacher_id'] = user.id   
                    messages.success(request, "Login successful!")
                    return redirect("dashboard")
                else: 
                    messages.error(request, "Incorrect password.")
            except TeacherUser.DoesNotExist:
                messages.error(request, "No account found with this email.")
    else:
        form = TeacherLoginForm()
    return render(request, "teachers/login.html", {"form": form})


def teacher_logout(request):
    request.session.flush()   
    messages.success(request, "Logged out successfully.")
    return redirect("login")


# teachers home page  
@login_required
def teachers_dashboard(request):
        query=request.GET.get('query','')
        if query:  
            filesearch=UploadRecordFile.objects.filter(subject__icontains=query) 
            if not filesearch:   
                return render(request,'notFound.html',{'error_file':query})  
            return render(request,'teachers/teacher_dashboard.html',{'search_file':filesearch,'query':query}) 
        
        teacher_class=request.user  
                                                       
        class_data=UploadRecordFile.objects.filter(FormMaster=teacher_class)    
       

        return render(request,'teachers/teacher_dashboard.html',{'class_data':class_data})
      


# Logout 
def logoutFun(request):  
    logout(request) 
    messages.error(request,'Logout Successfully') 
    return redirect('home')  


# DELETE SUBMITTED RESULT
def delete_result(request,result_id):
    getResultFromadmin=get_object_or_404(UploadResult, id=result_id) 
    # getResult_from_student= get_object_or_404(Result,id=result_id)
    # getResult_from_student.delete()  
    getResultFromadmin.delete()
    messages.info(request,'Result deleted')
    return redirect('upload_results')


# Issue Reporter Form 
@login_required
def absence(request):
    errormessage = None
    if request.method == "POST":
        forms = AbsenceReport(request.POST, request.FILES)
        if forms.is_valid():
            forms.save()
            ParentName = forms.cleaned_data['Parent_Name']
            StudentName = forms.cleaned_data['Student_Name']

            try:
            
                send_email_fun.delay()

            except BadHeaderError:
                errormessage = "Invalid header found."

            except Exception as e:
                errormessage = f"Something went wrong: {e}"

            except smtplib.SMTPException as e:
                errormessage = f"SMTP error occurred: {e}"

            if errormessage:
                messages.error(request, f"{errormessage} Error occurred.")
                return redirect('absence')

            messages.success(request, f"Thank you for reporting, {ParentName}.")
            return redirect('absence')

    else:
        absenceForm = AbsenceReport(
            initial={
                'Student_Name': request.user.Student_name,
                'Parent_Name': request.user.parent_name
            }
        )

        return render(request, 'absence.html', {'absence_form': absenceForm})


# ANNOUNCEMENT VIEW
@login_required
def announcement(request):  
     announcement=Announcement.objects.all()
     return render(request,'announcement.html',{'announcement':announcement})    



