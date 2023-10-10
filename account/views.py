from django.shortcuts import redirect, render
from django.http import HttpResponse
from account.forms import CreateUserForm,LoginForm,UpdateUserForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress,Order,OrderItem

from django.contrib.auth.models import User
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from django.contrib import messages


# للحصول علي الموقع الحالي
from django.contrib.sites.shortcuts import get_current_site

from .token import user_tokenizer_generate

# تحميل نموذج البريد الإلكتروني من الملفات وملأه بالبيانات المطلوبة باستخدام render_to_string.
from django.template.loader import render_to_string

# تُستخدم للتأكد من أن البيانات تمثل كبايت وكسترينج
from django.utils.encoding import force_bytes, force_str

# تُستخدم عادة في معالجة رموز الاستعادة والمصادقة للمستخدمين عند إعادة تعيين كلمات المرور أو عمليات تأكيد البريد الإلكتروني.
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
# Create your views here.





def register(request):

  form = CreateUserForm()

  if request.method == 'POST':

    form = CreateUserForm(request.POST)

    if form.is_valid():
      
      user = form.save()

      user.is_active = False

      user.save()

      # email verification setup

      # جلب معلومات الموقع الحالي
      # لإنشاء روابط تحقق البريد الإلكتروني بشكل صحيح
      current_site = get_current_site(request)

      # تعيين عنوان البريد الالكتروني عند وصوله الي صندوق الوارد
      subject = 'Account verification Email'

      # لاعداد الرسالة المرسله الي المستخدم وهيا موجودة في هذا الملف
      message = render_to_string('account/registeration/email-verification.html', {
                       
          'user' : user, # اسم المستخدم

          'domain' : current_site.domain, # جلب الرابط الحالي لاستخدامه في رابط التحقق

          # لتمثيل معرف المستخدم كنص امن وتشفيره للتحقق من الهوية
          'uid' : urlsafe_base64_encode(force_bytes(user.pk)),

          # يُستخدم لإنشاء رمز التحقق الخاص بالمستخدم باستخدام مولّد الرموز المخصص
          'token' : user_tokenizer_generate.make_token(user),

      })

      # لارسال البيانات الي المستخدم
      user.email_user(subject=subject, message=message)


      return redirect('email_verification_sent')

  return render(request, 'account/registeration/register.html' , {'form': form})


# -------------------------------------

# المعلمات اللذي تم ارسالها في الرابط
def email_verification(request, uidb64, token):
  # لفك القيمة المشفرة وتحويلها الي نص وهو مفتاح المستخدم
  unique_id = force_str(urlsafe_base64_decode(uidb64))

  # يتم جلب المستخدم اللذي له نفس المفتاح اللذي قمنا بفك تشفيره
  user = User.objects.get(pk=unique_id)
  
  # sccess 

  # للتحقق من صحة المستخدم وصحة الرابط اللذي انشأناه والدخول عليه فإذا كان صحيحا 
  if user and user_tokenizer_generate.check_token(user, token):

    # قم بتفعيل الحساب
    user.is_active=True

    user.save()

    # ثم قم بتوجيه الي النجاح
    return redirect('email_verification_success')
  
  # failed

  else:

    # وجه للخطأ
    return redirect('email_verification_failed')


# -------------------------------------

def email_verification_sent(request):
  
  return render(request, 'account/registeration/email-verification-sent.html')


# -------------------------------------

def email_verification_success(request):

  return render(request, 'account/registeration/email-verification-success.html')


# -------------------------------------

def email_verification_failed(request):

  return render(request, 'account/registeration/email-verification-failed.html')


# ---------------------------------------

def my_login(request):

  form = LoginForm()

  if request.method == 'POST':

    form = LoginForm(request, data=request.POST)

    if form.is_valid():

      username = request.POST.get('username')
      password = request.POST.get('password')

      user = authenticate(request, username=username, password=password)

      if user is not None:

        auth.login(request, user)

        messages.success(request, 'Login success! ')

        return redirect('dashboard')
      
  return render(request, 'account/my-login.html', {'form':form})



# logout

def user_logout(request):

  try:

    # جلب كل مفاتيح الجلسات
    for key in list(request.session.keys()):
      
      # لو مفتاح الجلسه هو مفتاح الجلسه الحالي
      if key == 'session_key':
        
        # اكمل بدون حذف الجلسه
        continue

      # لو مفتاح الجلسه غير مفتاح الجلسه الحالي
      else:

        # احذف الجلسه
        del request.session[key]

  except KeyError:

    pass
  
  messages.error(request, 'Logged out! ')

  return redirect('store')






# dashboard

@login_required(login_url='my_login')
def dashboard(request):

  return render(request, 'account/dashboard.html',{})



# profile-management

@login_required(login_url='my_login')
def profile_management(request):

  user_form = UpdateUserForm(instance=request.user)

  if request.method == 'POST':

      user_form = UpdateUserForm(request.POST, instance=request.user)

      if user_form.is_valid():

        user_form.save()

        messages.info(request, 'Account Updated! ')

        return redirect('dashboard')
      
  


  return render(request, 'account/profile-management.html',{'user_form':user_form})



# delete-account

@login_required(login_url='my_login')
def delete_account(request):

  user = User.objects.get(id=request.user.id)

  if request.method == 'POST':

    user.delete()

    messages.error(request, 'Done! deleted account. ')

    return redirect('store')

  return render(request, 'account/delete-account.html',{})



# manage shipping
@login_required(login_url='my_login')
def manage_shipping(request):

  try:

    # account user get shipping information
    # لو فيه عناوين موجودة باسم اليوزر ده هاتها
    shipping = ShippingAddress.objects.get(user=request.user.id)

  except ShippingAddress.DoesNotExist:

    # not found shipping informations
    # لو مفيش هات الفورم فاضية
    shipping = None

  # try and except هات الفورم اللي طلعت من 
  form = ShippingForm(instance=shipping)

  if request.method == 'POST':

    form = ShippingForm(request.POST, instance=shipping)

    if form.is_valid():

      # احفظ بس استني
      shipping_user = form.save(commit=False)

      # خلي اليوزر بتاع الفورم هوا اليوز الحالي
      shipping_user.user = request.user

      # احفظ بقا
      shipping_user.save()

      return redirect('dashboard')
  
  return render(request, 'account/manage-shipping.html', {'form':form})


# Track order
@login_required(login_url='my_login')
def track_order(request):

  try:

    orders = OrderItem.objects.filter(user=request.user)

    return render(request, 'account/track-order.html', {'orders':orders})
  
  except:

    return render(request, 'account/track-order.html', {})

  