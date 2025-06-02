from xml.dom import ValidationErr
from django import forms
from django.forms import ModelForm, ValidationError
from .models import  *
# from django.contrib.auth.models import User 
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .models import TeacherUser 


                           # TEACHERS LOGIN 
class TeacherSignupForm(forms.ModelForm):

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}))

    class Meta:
        model = TeacherUser
        fields = ['first_name', 'last_name', 'email', 'telephone', 'Class']
        
        widgets={
            'fist_name':forms.TextInput(attrs={'class':'form-control','placeholder':'first name',}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'last name',}),
            'email':forms.TextInput(attrs={'class':'form-control' ,'placeholder':'email',}), 
            'telephone':forms.TextInput(attrs={'class':'form-control mt-4','placeholder':'telephone'}),   
            'Class':forms.Select(attrs={'class':'form-control'}) ,  
        }


    def clean_email(self):
        """Ensure email is unique"""
        email = self.cleaned_data.get("email")
        if TeacherUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already taken. Try another one.")
        return email

    def clean_telephone(self):
        """Ensure telephone is unique"""
        telephone = self.cleaned_data.get("telephone")
        if TeacherUser.objects.filter(telephone=telephone).exists():
            raise forms.ValidationError("Telephone number already registered.")
        return telephone

    def clean(self):
        """Ensure both passwords match"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class TeacherLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    
    
       
# ISSUE REPORT 
class AbsenceReport(ModelForm):
    class Meta: 
        model=absenceReport
        fields=("Student_Name","Student_Class","Parent_Name","reason","proveFile",)

        labels={
            'Student_Name':'',
            'reason':'', 
            'proveFile':'Child Pic', 
             
            # 'name':'' 
        }

        widgets={
            'Student_Name':forms.TextInput(attrs={'class':'form-control','placeholder':'Student Name',}),
            'Student_Class':forms.TextInput(attrs={'class':'form-control','placeholder':'Student CLass',}),
            'Parent_Name':forms.TextInput(attrs={'class':'form-control' ,'placeholder':'Parent Name',}), 
            'reason':forms.Textarea(attrs={'class':'form-control mt-4','placeholder':'Reason','style':'height:100px'}),  
            'proveFile':forms.FileInput(attrs={'placeholder':'Prove File'}) ,
            # 'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Name'})  
        }



# UPLOADING RESULT 
class UploadResultForm(ModelForm): 
    class Meta: 
          model= UploadResult 
          fields=("teacher_name","subject_name","Class","subject_file") 
          
          widgets={
                'teacher_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Teachers name'}),
                'Class':forms.TextInput(attrs={'class':'form-control','placeholder':'Your class'}), 
                'subject_name':forms.TextInput(attrs={'class':'form-control','placeholder':'subject'}),
                'subject_file':forms.FileInput(attrs={'class':'form-control'}), 
            }

           
    def clean(self):
               cleaned_data= super().clean() 
               subject_name=cleaned_data.get('subject_name')
               teacher_name=cleaned_data.get('teacher_name')
               # Check if a teacher has already submit a subject file 
            #    try: 
            #         get_teacherName=UploadResult.objects.get(teacher_name=teacher_name)
            #    except UploadResult.DoesNotExist:
            #          raise ValidationError("Your can't be recognize in the system please contact the admin")
                 
                 
               if UploadResult.objects.filter(teacher_name=teacher_name,subject_name=subject_name).exists(): 
                    self.add_error('subject_name',f'Please you have already submit {subject_name}')

               return cleaned_data 
                    
                        
                    

# form teachers
class FormMasterForms(forms.ModelForm):

    class Meta:
        model=FormMaster
        fields="__all__"

        widgets={
            'name':forms.TextInput(attrs={'class':'form-control',}),
            'phoneNumber':forms.TextInput(attrs={'class':'form-control','max-length':'10'}),
            'age':forms.TextInput(attrs={'class':'form-control'}),
            'picture':forms.TextInput(attrs={'class':'form-control'})
            
        }