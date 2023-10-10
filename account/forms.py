from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput

# انشاء مستخدم جديد
class CreateUserForm(UserCreationForm):

  class Meta:

    model = User

    fields = ['username', 'email', 'password1', 'password2']

  # للسماح بالحفظ والتعديل
  def __init__(self, *args, **kwargs):
    super(CreateUserForm, self).__init__(*args, **kwargs)

    # لجعل حقل الايميل مطلوب
    self.fields['email'].required = True

  # للتاكد من صحة الايميل
  def clean_email(self):

    # جلب الايميل
    email = self.cleaned_data.get('email')

    # لو الايميل مسجل في الامستخدمين
    if User.objects.filter(email=email).exists():

      # اظهار ريالة الخطأ
      raise forms.ValidationError('This email is Invalid!')
    
    # لو الايميل طوله اكبر من 200
    if len(email) >= 200:

      # اظهر هذه الرسالة
      raise forms.ValidationError('This email is too Long!')
    
    return email
  


# login form 

class LoginForm(AuthenticationForm):

  username=forms.CharField(widget=TextInput())
  password=forms.CharField(widget=PasswordInput())



# update user

class UpdateUserForm(forms.ModelForm):

  password = None

  class Meta:

    model = User
    fields = ['username','email']
    exclude = ['password1','password2']

  # للسماح بالحفظ والتعديل
  def __init__(self, *args, **kwargs):
    super(UpdateUserForm, self).__init__(*args, **kwargs)

    # لجعل حقل الايميل مطلوب
    self.fields['email'].required = True


  # للتاكد من صحة الايميل
  def clean_email(self):

    # جلب الايميل
    email = self.cleaned_data.get('email')

    # لو الايميل مسجل في الامستخدمين مع تجاهل الايميل الحالي لانه يعمل
    if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():

      # اظهار ريالة الخطأ
      raise forms.ValidationError('This email is Invalid try anothor email')
    
    # لو الايميل طوله اكبر من 200
    if len(email) >= 200:

      # اظهر هذه الرسالة
      raise forms.ValidationError('This email is too Long!')
    
    return email
  