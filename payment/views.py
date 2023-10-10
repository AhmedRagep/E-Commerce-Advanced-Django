from django.shortcuts import render
from .models import ShippingAddress,Order,OrderItem
from cart.cart import Cart

from django.http import JsonResponse

from django.core.mail import send_mail
from django.conf import settings

# Create your views here.


def checkout(request):

  # لو اليوزر مسجل دخول
  if request.user.is_authenticated:

    try:

      # هات العنوان اللي باسم المستخدم الحالي لو موجود
      shipping = ShippingAddress.objects.get(user=request.user.id)

      return render(request, 'payment/checkout.html', {'shipping':shipping}) 
    
    except:

      # لو مش موجود روح للصفحه عادي
      return render(request, 'payment/checkout.html', {}) 
    
  else:

    # لو اليوزر مش مسجل روح للصفحة فاضية
    return render(request, 'payment/checkout.html', {}) 



def complete_order(request):

  # submit لو المستخدم ضغط علي 
  if request.POST.get('action') == 'post':

    # معلومات من الصفحة
    name = request.POST.get('name')
    email = request.POST.get('email')
    address1 = request.POST.get('address1')
    address2 = request.POST.get('address2')
    city = request.POST.get('city')
    state = request.POST.get('state')
    zipcode = request.POST.get('zipcode')

    # all-in-one shipping address
    # العنوان بالكامل تحت بعض
    shipping_address = (address1 + "\n" + address2 + "\n" + city + "\n" +
                        
    state + "\n" + zipcode)


    # shopping cart information

    # جلب الكارت
    cart = Cart(request)

    # جلب السعر الكلي للمنجات
    total_cost = cart.get_total()

    '''
      Order variations

      1) انشاء اوردر باستخدام الايميل المسجل سواء لديه عنوان ام لا

      2) انشاء الاوردر حتي لو الشخص مش عامل حساب

    '''

    # لو الشحص عنده حساب
    if request.user.is_authenticated:

      # انشئ اوردر بالمعلومات واليوزر الحالي والعنوان بالكامل والسعر الكلي
      order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address,

      amount_paid = total_cost, user=request.user)

      # جلب رقم الاوردر اللذ انشئناه حالا
      order_id = order.pk

      # عمل تكرار علي المنتجات اللتي في سلة التسوق
      product_list = []
      for item in cart:

        # انشاء اوردر للمنتج به المعلومات من الكارت واختياره عن طريق رقم الاوردر السابق وايضا اليوزر الحالي
        OrderItem.objects.create(order_id=order_id, product=item['product'], quantity=item['qty'],
                                 
        price=item['price'], user=request.user)

        product_list.append(item['product'])

      all_products = product_list


      # send mail
      email_subject = 'Order received'
      email_message = (
          'Hi!\n\n'
          'Thank you for placing your order.\n\n'
          'Please see your order details below:\n\n'
          # قم بإضافة تفاصيل الطلب هنا، مثل all_products والمبلغ المدفوع
          'Order Details:\n\n'
          'Products: {}\n\n'.format(all_products) +
          'Total paid: ${}\n\n'.format(cart.get_total())
          # قد تضيف المزيد من التفاصيل حول الطلب هنا
      )
      send_mail(email_subject, email_message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
      



    # لو اليوزر مش مسجل وبيعمل اوردر
    else:
      
      # انشئ اوردر بالمعلومات والعنوان بالكامل والسعر الكلي
      order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address,
      
      amount_paid = total_cost)

      # جلب رقم الاوردر اللذ انشئناه حالا
      order_id = order.pk


      product_list = []
      # عمل تكرار علي المنتجات اللتي في سلة التسوق
      for item in cart:
        
        # انشاء اوردر للمنتج به المعلومات من الكارت واختياره عن طريق رقم الاوردر السابق وايضا بدون يوزر
        OrderItem.objects.create(order_id=order_id, product=item['product'], quantity=item['qty'],
                                 
        price=item['price'])

        product_list.append(item['product'])

      all_products = product_list



      # send mail
      email_subject = 'Order received'
      email_message = (
          'Hi!\n\n'
          'Thank you for placing your order.\n\n'
          'Please see your order details below:\n\n'
          # قم بإضافة تفاصيل الطلب هنا، مثل all_products والمبلغ المدفوع
          'Order Details:\n\n'
          'Products: {}\n\n'.format(all_products) +
          'Total paid: ${}\n\n'.format(cart.get_total())
          # قد تضيف المزيد من التفاصيل حول الطلب هنا
      )
      send_mail(email_subject, email_message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
      
 




    # ارسال نجاح لاجاكس
    order_success = True

    # ارسال نجاح لاجاكس
    response = JsonResponse({'success':order_success})

    return response



def payment_success(request):

  # clear shopping cart

  for key in list(request.session.keys()):

    if key == 'session_key':

      del request.session[key]

  return render(request, 'payment/payment-success.html',{})




def payment_failed(request):

  return render(request, 'payment/payment-failed.html',{})