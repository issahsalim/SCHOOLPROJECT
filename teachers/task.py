
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_email_fun():
    message="Email sent successfully"
    subject="Testing"
    recipient_mail= ["issahsalim233@gmail.com"] 

    send_mail(
        subject=subject,
        message=message,
        recipient_list=recipient_mail,
        from_email=settings.EMAIL_HOST_USER,   
        fail_silently=False
    )
    return "Email sent"


#  student Email ID sending function 
@shared_task 
def send_username_mail(username,child_name,parent_name,recipient_mail): 
    message=f"Hi {parent_name} here is your child {child_name} index number {username}" 
    subject="Your student ID"  

    send_mail(
        subject=subject,
        message=message, 
        recipient_list=recipient_mail,
        from_email=settings.EMAIL_HOST_USER,   
        fail_silently=False
    ) 
    return "Username sent"


# Teachers ID email send 
@shared_task
def teacher_id_mail(username,teacher_name,teacher_mail): 
    message=f"Hi  teacher {teacher_name} here is your ID Number  {username}"  
    subject="Your ID"   
    
    send_mail(
        subject=subject,
        message=message, 
        recipient_list=teacher_mail, 
        from_email=settings.EMAIL_HOST_USER,   
        fail_silently=False
    )  
    
    return "Username sent"

# SEND MAIL WHEN ANN IS GIVEN 
@shared_task
def teacher_id_mail(username,teacher_name,teacher_mail): 
    message=f"Hi  teacher {teacher_name} here is your ID Number  {username}"  
    subject="Your ID"   
    
    send_mail(
        subject=subject,
        message=message, 
        recipient_list=teacher_mail, 
        from_email=settings.EMAIL_HOST_USER,   
        fail_silently=False
    )  
    
    return "Username sent"

