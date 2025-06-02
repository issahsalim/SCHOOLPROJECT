from django.utils import timezone
from django.db import models
from datetime import datetime
from django.db import models
from django.forms import CharField 
from django.contrib.auth.models import AbstractUser 
from django.conf import settings
from django.db.models import Max
from django.contrib.auth.models import AbstractUser
from django.db import models 
from datetime import datetime
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.hashers import make_password, check_password
 
class TeacherUser(models.Model):  
    class_choices = [
        ("None", "None"), 
        ("class1", "class1"),
        ("class2", "class2"),
        ("class3", "class3"), 
        ("class4", "class4"),
        ("class5", "class5"),
        ("class6", "class6"),
        ("form1", "form1"),
        ("form2", "form2"),
        ("form3", "form3"),
    ]

    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    Class = models.CharField(choices=class_choices, default="None", max_length=20)
    telephone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, blank=False)
    password = models.CharField(max_length=255)  
    role=models.CharField(max_length=10) 

    def save(self, *args, **kwargs):
        """Automatically generate a unique username based on first name and year"""
        self.role="teacher" 

        if not self.username:   
            current_year = datetime.now().year
            max_teacher = TeacherUser.objects.aggregate(Max('username'))['username__max']
            new_teacher_value = 1

            if max_teacher and max_teacher[:3].isalpha() and max_teacher[3:7].isdigit():
                new_teacher_value = int(max_teacher[7:]) + 1  

            extra_firstname = self.first_name[:3].upper() if self.first_name else "TCH"
            self.username = f"{extra_firstname}{current_year}{new_teacher_value:03d}T"   

        super().save(*args, **kwargs)

    def set_password(self, raw_password):
        """Manually hash passwords before saving"""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Manually check if entered password is correct"""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username


class UploadRecordFile(models.Model): 
   FormMaster=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,  related_name='record_file')  
   subject=models.CharField(max_length=20) 
   file=models.FileField(upload_to='excel_file',blank=False, null=False, default=None) 


# UPLOADING RESULTS TABLE
class UploadResult(models.Model):
   teacher_name=models.CharField(max_length=100)
   subject_name=models.CharField(max_length=100) 
   Class=models.CharField(max_length=100)  
   subject_file=models.FileField() 
   uploaded_at=models.DateTimeField(auto_now=True) 



                     # RESULT
class Result(models.Model):
    index_number = models.CharField(max_length=20)
    subject = models.CharField(max_length=100)
    marks = models.FloatField()
    grade = models.CharField(max_length=2)
    term = models.CharField(max_length=50)   
    year = models.CharField(max_length=4)    
    def __str__(self):
        return f"{self.index_number} - {self.subject} - {self.marks}"



class Announcement(models.Model):
   title=models.CharField(max_length=200)
   message=models.TextField()
   date = models.DateTimeField(default=timezone.now)
   
   def __str__(self):
    return self.title 
    

class absenceReport(models.Model):
   Student_Name=models.CharField(max_length=100)
   Student_Class=models.CharField(max_length=40)
   Parent_Name=models.CharField(max_length=100)
   reason=models.TextField() 
   proveFile=models.FileField(upload_to='upload', blank=True, null=True) 
   submitted_date=models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return self.Parent_Name 



# Form Master model
class FormMaster(models.Model):
   name=models.CharField(max_length=100)
   ClassHanlder=models.CharField(max_length=100)
   phoneNumber= models.IntegerField( )
   age=models.IntegerField() 
   picture= models.ImageField(blank=True, null=True)
   
 
#  Headmaster model
class  Headmaster(models.Model):
   name=models.CharField(max_length=50)
   phoneNumber=models.IntegerField( )
   email=models.EmailField()
   picture=models.ImageField( blank=True, null=True) 
   

class Assignment(models.Model):
   Class=models.CharField(max_length=20) 
   Date=models.DateField()
   Due_date=models.DateField()
   status=models.BooleanField()
   