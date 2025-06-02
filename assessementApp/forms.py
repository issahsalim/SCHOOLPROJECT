from xml.dom import ValidationErr
from django import forms
from django.forms import ModelForm, ValidationError
from .models import  *
# from django.contrib.auth.models import User 
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .models import CustomUser 


# STUDENT SIGNUP FORM 
class CustomUserCreationForm(UserCreationForm):
    telephone = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'e.g 0503499999'}))
    
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '******','id':'id_password1'}))
    
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': '*******','id':'id_password2'}))
    
    Classes = [
        ("",""),
        ("class1", 'class1'), 
        ("class2", 'class2'),
        ("class3", 'class3'),
        ("class4", 'class4'),
        ("class5", 'class5'),
        ("class6", 'class6'),
        ("form1", 'form1'),
        ("form2", 'form2'),
        ("form3", 'form3'),
    ]
    
    Class = forms.CharField(
         widget=forms.Select(choices=Classes, attrs={'class':'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'telephone', 'Class', 'email', 'password1', 'password2']
        
        widgets = { 
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Email'}),  
            'first_name': forms.EmailInput(attrs={'class': 'form-control','placeholder':'First Name','required':'ture'}),  
            'last_name': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Last Name','require':'true'}),  
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'role' in self.fields: 
            del self.fields['role']

    def clean(self):
         cleaned_data= super().clean()
         first_name=cleaned_data.get('first_name')
         last_name=cleaned_data.get('last_name')
         email=cleaned_data.get('email')
         if first_name=='':
              self.add_error('first_name','first name is required')
         if last_name=='':
              self.add_error('last_name','last name is required')
         if email=='':
              self.add_error('email','email is required')  
         return cleaned_data 

    def clean_telephone(self):
        telephone = self.cleaned_data['telephone']
        if len(telephone) != 10: 
            raise ValidationError('Phone number must be 10 digits') 
        if not telephone.isdigit():
             raise ValidationError('Phone number must contain only digits')
        if CustomUser.objects.filter(telephone=telephone).exists(): 
            raise ValidationError('An account with this phone number already exists')
        return telephone


# STUDENT AUTHENTICATION FORMS
class CustomAuthenticationForm(AuthenticationForm):
        username=forms.CharField(
            widget=forms.TextInput(attrs={'class':'form-control','placeholder':'ID Number'})
        ) 
        password=forms.CharField(
            widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password','id':'password'}) 
        )

        # def clean(self):
        #         clean_data= super().clean() 
        #         student_username=clean_data.get('username') 
        #         student_password=clean_data.get('password') 
        #         if student_password and student_username:
        #              student_role=CustomUser.objects.get(username=student_username) 
        #              if student_role.role !='student':
        #                   raise ValidationError('You are not authorized to log in here.')
        #         return  clean_data 
        




        #                                     # TEACHERS LOGIN 


 
 
    

       
       
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