from email import message
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
from django.template.loader import render_to_string 
from xhtml2pdf import pisa 
import csv



# Email invalid when resetting password
class CustomPasswordResetView(PasswordResetView):
    template_name = 'reset_password.html'
    email_template_name = "email_reset_password.html"
    success_url = reverse_lazy('password_reset_done')  

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        
        
        if CustomUser.objects.filter(email=email).exists():     
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


# general login
def general_login(request):
    return render(request,'generallogin.html')


# general signup 
def general_signup(request):
    return render(request,'generalsignup.html')


# ANNOUNCEMENT VIEW 
@login_required
def announcement(request):  
     announcement=Announcement.objects.all()
     return render(request,'announcement.html',{'announcement':announcement})    


# ABSENCE REPORT VIEWS
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
                email=request.user.email
                send_email_fun.delay(StudentName,email) 

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
                'Student_Name': request.user.get_full_name ,
                'Student_Class':request.user.Class
            }
        )

        return render(request, 'absence.html', {'absence_form': absenceForm})


# LIST TEACHERS VIEWS
@login_required 
def addTeach(request):
    # if request.method=="GET":
        searched=request.GET.get('search','') 
        teachers=FormMaster.objects.all() 
        headmaster=Headmaster.objects.all() 
        onpage={'teachers':teachers,'headmaster':headmaster} 
        if searched:  
            
            result=FormMaster.objects.filter(Q(name__icontains=searched) | Q(ClassHanlder__icontains=searched)) 
            if not result:  
                return render(request,'notFound.html',{'errorsearch':searched})  
            return render(request,'formteacher.html',{'search':result})      
            
        return render(request,'formteacher.html',onpage)


# STUDENT REGISTRATION 
def signup_view(request):
    errormessage=None 
    if request.method == 'POST': 
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():   
            user = form.save(commit=False)
            user.role="student"  
            if user.telephone:   
                student_name=request.user.get_full_name() 
                mail=user.email 
                username=user.username

                try:    
                    send_username_mail.delay(username,student_name,mail) 

                except BadHeaderError:
                    errormessage = "Invalid header found."
                
                except Exception as e:
                    errormessage = f"Something went wrong: {e}" 

                except smtplib.SMTPException as e:
                    errormessage = f"SMTP error occurred: {e}"

                if errormessage:
                    messages.error(request, f"{errormessage} Error occurred.")
                    return redirect('student_signup') 
                
            user.save() 
            login(request, user) 
            return redirect('home') 
    else:                               
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


# Teachers registration
def teachers_view(request):
    errormessage=None 
    if request.method == 'POST': 
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():   
            user = form.save(commit=False)
            user.role="teacher"  
            if user.telephone: 

                username=request.user.username
                teacher_name=request.user.get_full_name() 
                mail=user.email             
                try:    
                    
                    teacher_id_mail.delay(username,teacher_name,mail) 
                    
                except BadHeaderError:
                    errormessage = "Invalid header found."
                
                except Exception as e:
                    errormessage = f"Something went wrong: {e}" 

                except smtplib.SMTPException as e:
                    errormessage = f"SMTP error occurred: {e}"

                if errormessage:
                    messages.error(request, f"{errormessage} Error occurred.")
                    return redirect('teacher_signup') 
             
            user.save() 
            login(request, user) 
            return redirect('teacher_dashboard') 
    else:                               
        form = CustomUserCreationForm()
    return render(request, 'teachers_register.html', {'form': form})


# LOGIN     
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid(): 
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            

            try: 
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                messages.error(request, 'User does not exist.')
                return render(request, 'login.html', {'form': form})
            
            
            # Authenticate the user
            user = authenticate(username=username, password=password)
            if user is not None:
                # Redirect based on role
                login(request, user) 

                if user.role == 'student': 
                    return redirect('home') 
                
                elif user.role=='teacher':
                    return redirect('teacher_dashboard')
                
                elif request.user.is_superuser:
                    return redirect('general_login')
                 
                else:    
                    messages.error(request, 'Invalid role.')
                    return redirect('login/') 
            else: 
                messages.error(request, 'Invalid credentials.') 
                return redirect('login/') 
        else:   
            messages.error(request, 'Invalid username or password')  
            return render(request,'login.html')
    else:   
        return render(request, 'login.html' )


# LOGOUT
def logoutFun(request):  
    logout(request) 
    messages.error(request,'Logout Successfully') 
    return redirect('home')  


def custom_404(request, exception):
    return render(request, '404.html', status=404) 



# STUDENT VIEW RESULTS
@login_required
def student_results(request):
    if request.user.role != 'student':                                   
        messages.info(request,'You are not allow authorized to go there') 
        return redirect('home')  
    recorded=Result.objects.filter(index_number=request.user).exists()
    if not recorded:  
        messages.info(request,f"{request.user.get_full_name()} please your result has not been uploaded yet.")
        return render(request,'home.html')  
    results = Result.objects.filter(index_number=request.user).distinct() 
    return render(request, 'student_results.html', {'results': results})


# DOWNLOADING RESULT 
@login_required
def downloadResult(request):
    # Fetch results for the logged-in user
    results = Result.objects.filter(index_number=request.user)  
    student_name = request.user 
    
    # Path to the HTML template and context for rendering
    html_template = 'download_result.html'
    context = {'results': results, 'student': student_name}
 
    # Render HTML as a string
    html = render_to_string(html_template, context) 

    # Prepare the HTTP response for PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={student_name.username}_result.pdf' 
    
    # Generate the PDF
    pisa_status = pisa.CreatePDF(html, dest=response) 

    # Check for errors during PDF generation
    if pisa_status.err: 
        return HttpResponse("An error occurred while downloading the results. Please try again.", content_type="text/plain")
    
    return response       


# UPLOADING RESULT  
@login_required 
def upload_results(request): 
    if request.method == "POST": 
        form = UploadResultForm(request.POST, request.FILES)
        
        if form.is_valid():
            save_result=form.save(commit=False)
            csv_file = form.cleaned_data.get('subject_file') 
            teachers_name=form.cleaned_data.get('teacher_name')
            Class =form.cleaned_data['Class']
            subject_name=form.cleaned_data['subject_name'] 

            # Validate teacher before uploading result
            if teachers_name != request.user.username:
                messages.error(request,"Please ensure you are submitting the your own file")
                return redirect('upload_results')
            
            # Check if teachers submit their own class file
            valid_class= request.user.Class
            if Class != valid_class: 
                messages.info(request,'Please you can only submit your class file.')
                return redirect('upload_results') 
            
            # CHECK IF TEACHER HAS ALREADY SUBMIT A CERTAIN SUBJECT 
                
            if UploadResult.objects.filter(teacher_name=request.user,subject_name=subject_name).exists(): 
                    messages.info(request,f'You have already submit {subject_name}') 
                    return redirect('upload_results') 

            # Check if the uploaded file is a valid CSV file
            if not csv_file.content_type=="text/csv": 
                messages.error(request, "Please upload a valid CSV file.")
                return redirect('upload_results')

            try:
                # Read and decode the file content
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.reader(decoded_file)
                
                # chek headers
                headers = next(reader)
                expected_headers = ['index_number', 'subject', 'marks', 'grade', 'term', 'year']
                if headers != expected_headers:
                    messages.error(request, 'Please check the headers of your file.')
                    return redirect('upload_results')

                # Process the data to save to databas
                for row in reader:
                    Result.objects.create(
                        index_number=row[0],
                        subject=row[1],
                        marks=float(row[2]),
                        grade=row[3],
                        term=row[4],
                        year=row[5]
                    ) 

                save_result.save() 
                messages.success(request, "Results uploaded successfully!")
                return redirect('upload_results')

            except Exception as e:  
                messages.error(request, f"An error occurred while processing the file: {str(e)}")
                return redirect('upload_results')
        
        else:
            # Form validation errors  
            messages.error(request, "Please correct the errors in the form.")
            return render(request, 'uploadResult.html', {'form': form})
    
    else:
        # Handle GET request
        form = UploadResultForm(
            initial={
                'teacher_name':request.user.username,
                'Class':request.user.Class 
            }  
        )   

        submitted_subject=UploadResult.objects.filter(teacher_name=request.user) 
        # allTeachers=TeacherUser.objects.filter(role="teacher").values_list('email') 
    return render(request, 'uploadResult.html', {'form': form,'submitted_subject':submitted_subject,}) 


# DELETE SUBMITTED RESULT
def delete_result(request,result_id):
    getResultFromadmin=get_object_or_404(UploadResult, id=result_id) 
    getResultFromadmin.delete()
    messages.info(request,'Result deleted')
    return redirect('upload_results')


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
   
