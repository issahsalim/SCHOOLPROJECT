from django.contrib import admin
from django.contrib.admin.models import LogEntry

from .models import * 
from django.core.cache import cache
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin 
import csv
from django.http import HttpResponse



# USERS
# class CustomUserAdmin(UserAdmin):
#     list_display=('username','telephone','is_superuser','Class') 
#     search_fields=('username','telephone',)

#     fieldsets=(
#         (None,{'fields':('username','password')}),
#         ('Personal Info',{'fields':('telephone','email', 'Class')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
#         ('Important Dates', {'fields': ('last_login', 'date_joined')}),

#     )


#     add_fieldsets = (
#     (None, {
#         'Class': ('wide',),
#         'fields': ('username', 'email', 'telephone', 'password1', 'password2', 'is_staff', 'is_active', 'Class'), 
#     }),
# )

#     ordering=('username',) 

admin.site.register(TeacherUser) 


# SUBMITTED RESULT 
@admin.register(UploadResult)
class ResultUploadAdmin(admin.ModelAdmin):
    list_display=('teacher_name','subject_name','Class','uploaded_at',)



#   TEACHERS SUBJECTS FILES 
@admin.register(UploadRecordFile)
class UploadFile(admin.ModelAdmin):
    list_display=('FormMaster','subject',)   


# ASSIGNMENT
@admin.register(Assignment)
class Assignment(admin.ModelAdmin):
    list_display=('form','Date','Due_date','status',)


# ANNOUNCEMENT
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display=('title','date',)

   
# ABSENCE FORMS 
@admin.register(absenceReport) 
class IssueReportAdmin(admin.ModelAdmin):  
    list_display=('Student_Name',"Student_Class","Parent_Name",'submitted_date',) 


# TEACHERS
@admin.register(FormMaster)
class Add_Form_Master(admin.ModelAdmin):
    list_display=('name','phoneNumber','ClassHanlder',) 
    search_fields=("name","phoneNumber","age","ClassHanlder",)


# HEADMASTERS
@admin.register(Headmaster)
class Headmaster(admin.ModelAdmin):
    list_display=("name","phoneNumber",) 


 




