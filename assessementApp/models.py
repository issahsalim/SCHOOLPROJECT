from django.utils import timezone
from django.db import models
from datetime import datetime
from django.db import models
from django.forms import CharField, ValidationError 
from django.contrib.auth.models import AbstractUser,Group,Permission 
from django.conf import settings
from django.db.models import Max
from datetime import datetime
from django.db.models.functions import Substr,Cast 
from django.db.models import Max

class staticIndexNumbers(models.Model):
  Student_IndexNumber=models.CharField(max_length=10)
  def __str__(self):
     return self.Student_IndexNumber



class CustomUser(AbstractUser):
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
    
    roles = [
       ("student", "Student"),   
       ("teacher", "Teacher"), 
    ]
    
    Class = models.CharField(choices=class_choices, default="None", max_length=20)
    telephone = models.CharField(max_length=15) 
    role = models.CharField(choices=roles, max_length=20,blank=True)  
    
    def __str__(self):
        return self.username


    def save(self, *args, **kwargs):
        if not self.pk and self.role == "student":
            current_year = datetime.now().year
            max_username = CustomUser.objects.filter(
                username__startswith=f"STU{current_year}"
            ).aggregate(Max('username'))['username__max']
            
            if max_username:
                num_part = max_username[7:]  
                self.username = f"STU{current_year}{int(num_part)+1:03d}"
            else:
                num_part=0
                self.username = f"STU{current_year}{int(num_part)+1:03d}"


        elif not self.pk and self.role == "teacher":
            current_year = datetime.now().year
            max_username = CustomUser.objects.filter(
                username__startswith=f"SIR{current_year}"
            ).aggregate(Max('username'))['username__max']
            
            if max_username:
                num_part = max_username[7:]  
                self.username = f"SIR{current_year}{int(num_part)+1:03d}"
            else:
                 num_part=0   
                 self.username = f"SIR{current_year}{int(num_part)+1:03d}"


        super().save(*args, **kwargs)

# STUDENT PROFILE 
# class StudentProfile(models.Model):
#     user=models.OneToOneField(CustomUser, on_delete=models.CASCADE) 
#     class_choices = [
#         ("class1", "class1"),
#         ("class2", "class2"),
#         ("class3", "class3"),
#         ("class4", "class4"),
#         ("class5", "class5"),
#         ("class6", "class6"),
#         ("form1", "form1"),
#         ("form2", "form2"),
#         ("form3", "form3"),
#     ]

#     classes = models.CharField(choices=class_choices, default="None", max_length=20)
#     Student_name = models.CharField(max_length=100, blank=False, null=False , default="unknown")
#     parent_name = models.CharField(max_length=100,blank=False, null=False  , default="unknown" ) 
#     telephone = models.CharField(max_length=15, blank=False, null=False)
#     role=models.CharField(max_length=10) 
    
    
#     def __str__(self):
#         return self.username if self.username else "Unnamed User"
    
   

# UPLOADING RESULTS TABLE
class UploadResult(models.Model):
   teacher_name=models.CharField(max_length=100)
   subject_name=models.CharField(max_length=100) 
   Class=models.CharField(max_length=100)  
   subject_file=models.FileField() 
   uploaded_at=models.DateTimeField(auto_now=True) 




                     # RESULT


# Student results 
class Result(models.Model):
    index_number = models.CharField(max_length=10)
    subject = models.CharField(max_length=100)
    marks = models.FloatField()
    grade = models.CharField(max_length=2)
    term = models.CharField(max_length=50)   
    year = models.CharField(max_length=4)    
    def __str__(self):
        return f"{self.index_number} - {self.subject} - {self.marks}"


# Announcement
class Announcement(models.Model):
   title=models.CharField(max_length=200)
   message=models.TextField()
   date = models.DateTimeField(default=timezone.now)
   
   def __str__(self):
    return self.title 
    

# Absence Form
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
   

# Assignment
class Assignment(models.Model):
   Class=models.CharField(max_length=20) 
   Date=models.DateField()
   Due_date=models.DateField()
   status=models.BooleanField()
   

# Uploading result files 
class UploadRecordFile(models.Model): 
   FormMaster=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,limit_choices_to={'role':'teacher'} ,related_name='record_file')  
   subject=models.CharField(max_length=20) 
   file=models.FileField(upload_to='excel_file',blank=False, null=False, default=None) 
   def clean(self):
        super().clean()
        if self.FormMaster and self.FormMaster.role != 'teacher':
            raise ValidationError({'FormMaster': 'Only users with teacher role can be assigned as Form Master'})





 


