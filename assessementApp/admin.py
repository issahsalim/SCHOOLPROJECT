from django.contrib import admin
from django.contrib.admin.models import LogEntry
from .models import * 
from django.core.cache import cache
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin 
import csv
from django.http import HttpResponse


admin.site.register(LogEntry) 


# USERS
class CustomUserAdmin(UserAdmin):
    list_display=('username','first_name','last_name','telephone','is_superuser' ,'Class','role',) 
    search_fields=('first_name','username','telephone','Class',)

    fieldsets=(
        (None,{'fields':('username','password')}),
        ('Personal Info',{'fields':('telephone','first_name','last_name','email','Class','role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}), 
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('username', 'email', 'first_name','last_name', 'telephone','role','password1', 'password2', 'is_staff', 'is_active','Class'),
    }),
)


    ordering=('username',) 


admin.site.register(CustomUser,CustomUserAdmin)


# student results 
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display=('index_number','subject','marks',)
    search_fields=('index_number','subject',) 



# ANNOUNCEMENT
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display=('title','date',)

   
# ABSENCE FORMS 
@admin.register(absenceReport) 
class IssueReportAdmin(admin.ModelAdmin):  
    list_display=('Student_Name',"Student_Class","Parent_Name",'submitted_date',) 



@admin.register(UploadResult)
class ResultUploadAdmin(admin.ModelAdmin):
    list_display=('teacher_name','subject_name','Class',) 
    
@admin.register(UploadRecordFile    )
class ResultUploadAdmin(admin.ModelAdmin):
    list_display=('FormMaster','subject',)  









# admin.site.site_header="ITB Attendance App"
# admin.site.site_title="Royal"




