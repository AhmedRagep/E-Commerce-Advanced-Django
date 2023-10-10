from django.shortcuts import render
from .cart import Cart
from store.models import Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
# Create your views here.

def cart_summary(request):

  cart = Cart(request)

  return render(request, 'cart/cart_summary.html', {'cart':cart})


def cart_add(request):
  cart = Cart(request)

  # اذا كانت قيمة الطلب من كود اجاكس بوست
  if request.POST.get('action') == 'post':
    # جلب رقم المنتج من اجاكس
    product_id = int(request.POST.get('product_id'))
    # جلب كمية المنتج من اجاكس
    product_quantity = int(request.POST.get('product_quantity'))

    # جلب المنتج صاحب الرقم
    product = get_object_or_404(Product, id=product_id)

    # اضافة المعلومات في دالة   وهيا المنتج وكميته
    cart.add(product=product, product_qty=product_quantity)

    # __len__  هذا لجلب كمية المنتجات من الكارت من الدالة 
    cart_quantity = cart.__len__()

    # ثم نقوم بإرجاعها في اجاكس
    response = JsonResponse({'qty': cart_quantity})

    return response


def cart_delete(request):
  cart = Cart(request)

  # اذا كانت قيمة الطلب من كود اجاكس بوست
  if request.POST.get('action') == 'post':

    # جلب رقم المنتج من اجاكس
    product_id = int(request.POST.get('product_id'))

    # ارسال رقم المنتج الي دالة الحذف في الكارت
    cart.delete(product=product_id)

    # __len__  هذا لجلب كمية المنتجات من الكارت من الدالة 
    cart_quantity = cart.__len__()

    # جلب الاجمالي بعد الحذف
    cart_total = cart.get_total()

    # يتم ارسال هذا لاجاكس
    response = JsonResponse({'qty': cart_quantity, 'total': cart_total})

    return response


def cart_update(request):
  cart = Cart(request)

  # اذا كانت قيمة الطلب من كود اجاكس بوست
  if request.POST.get('action') == 'post':

    # جلب رقم المنتج من اجاكس
    product_id = int(request.POST.get('product_id'))

    # جلب كمية المنتج من اجاكس
    product_quantity = int(request.POST.get('product_quantity'))

    # ارسال المنتج والكمية لدالة الاتحديث في الكارت
    cart.update(product=product_id, qty=product_quantity)

    # __len__  هذا لجلب كمية المنتجات من الكارت من الدالة 
    cart_quantity = cart.__len__()

    # جلب الاجمالي بعد الحذف
    cart_total = cart.get_total()

    # يتم ارسال هذا لاجاكس
    response = JsonResponse({'qty': cart_quantity, 'total': cart_total})

    return response