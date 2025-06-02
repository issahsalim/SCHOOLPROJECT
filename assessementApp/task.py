from celery import shared_task
from django.core.mail import send_mail,send_mass_mail
from django.conf import settings


@shared_task
def send_email_fun(student_name,email):
    message=f"Thank you {student_name} reporting the head master will take the necessary action"
    subject="THANK YOU"

    send_mail(
        subject=subject,
        message=message, 
        recipient_list=[email], 
        from_email=settings.EMAIL_HOST_USER,   
        fail_silently=False
    )
    return "Email sent"


#  student Email ID sending function 
@shared_task
def send_username_mail(username,student_name,recipient_mail): 
    message=f"Hi {student_name} here is index number <strong> {username} </strong>"  
    subject="Your student ID"  

    send_mail(
        subject=subject,
        message=message, 
        recipient_list=[recipient_mail],
        from_email=settings.EMAIL_HOST_USER,   
        fail_silently=False
    )  

    return "Username sent"

@shared_task
def teacher_id_mail(username,teacher_name,recipient_mail): 
    message=f"Hi {teacher_name} here is your STAFF <strong> {username} </strong>"  
    subject="Your STAFF ID"   

    send_mail(
        subject=subject,
        message=message, 
        recipient_list=[recipient_mail],
        from_email=settings.EMAIL_HOST_USER,   
        fail_silently=False
    )  
    return "Username sent"


# Teachers ID email send 
@shared_task 
def send_ann_mail(subject,message,from_mail,mails): 
    
    send_mass_mail(
        (subject, message,from_mail,[email])
        for email in mails
    ) 
     
    return "Announcement sent"
