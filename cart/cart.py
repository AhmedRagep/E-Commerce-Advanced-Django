from decimal import Decimal

from store.models import Product


class Cart():
  
  def __init__(self, request):

    self.session = request.session
    
    cart = self.session.get('session_key')

    if 'session_key' not in request.session:

      cart = self.session['session_key'] = {}

    self.cart = cart


  # هذه للتحقق مما اذا تم التعديل علي الاد ام لا 
  # اذا كان اامنتج موجود في السلة يقوم بتحديث الكمية
  # واذا كان غير موجود يتم انشاء سلة جديدة بالمنتج وسعره وكميته
  # ثم يتحقق من انه تم التعديل

# -------------------------------

  def add(self, product, product_qty):
    
    # تحويل رقم المنتج اللي قيمة نصية
    product_id = str(product.id)

    # يتم التحقق هنا مما إذا كان product_id موجودًا بالفعل في سلة التسوق (self.cart) أم لا.
    # وسلة التسوق اتت بالمنتج من الفيو
    if product_id in self.cart:
      
      # سيتم تحديث الكمية الموجودة بالكمية المجلوبة من الفيو
      # qty هوا بمثابة متغير للكمية
      # واذا اضاف كمية اخري سيتم تحديث الكمية بدون عمل سلة جديدة
      self.cart[product_id]['qty'] = product_qty

    else:
      
      # سيتم انشاء مدخل جديد في سلة التسوق واضافة المنتج بسعره وكميته
      self.cart[product_id] = {'price': str(product.price), 'qty': product_qty}

    # اذا تم التعديل علي الكود 
    self.session.modified = True



  # -------------------------------

  def delete(self,product):
    
    # جلب المنتج الذي سيحذف من الفيو
    product_id = str(product)

    # لو هوا موجود في الكارت
    if product_id in self.cart:

      # قم بحذفه
      del self.cart[product_id]

    # اذا تم التعديل علي الكود 
    self.session.modified = True
  

# --------------------------------------


  def update(self, product, qty):

    # جلب المنتج الذي سيحذف من الفيو
    product_id = str(product)

    # جلب الكمية التي اخترتها في هذا المنتج
    product_quantity = qty

    # لو هوا موجود في الكارت
    if product_id in self.cart:

      # قم بتحديث الكمية الي الكمية المحدثة
      self.cart[product_id]['qty'] = product_quantity

    # اذا تم التعديل علي الكود 
    self.session.modified = True


# -------------------------------------
  # هذه دالة لارجاع مجموع الكميات الموجودة في سلة التسوق
  def __len__(self):
    #باستخدام سم وياتي بهم جميعا من الكارت qty هذا يقوم بجمع القيم من 
    return sum(item['qty'] for item in self.cart.values())
  

# ----------------------------------------

  def __iter__(self):

    # لجلب جميع مفاتيح المنتجات الموجودة في سلة التسوق
    all_product_ids = self.cart.keys()

    # استرداد جميع المنتجات اللتي تحمل المفاتيح السابقة 
    products = Product.objects.filter(id__in=all_product_ids)
    
    # يتم نسخ محتوي سلة التسوق الي مصفوفة
    cart = self.cart.copy()

    # لعمل تكرار بالمنتجات المفلترة اللتي اتينا بها
    for product in products:
      
      # لعمل مفتاح بالاسم لاستخدامه لاحقا في العرض وهو به المنتجات
      cart[str(product.id)]['product'] = product

    # لكل عنصر في مجموعة كرات فعل الامور التالية
    for item in cart.values():

      # لتحويل كل عنصر اتينا به الي رقم حسابي وهذا للتعامل معه جيدا في العمليات الرياضية
      item['price'] = Decimal(item['price'])

      # total ضرب قيمة السعر الاجمالي في كل عنصر في الكمية وهذا ياتي بالسعر الكلي داخل المتغير 
      item['total'] = item['price'] * item['qty']

      # لاعادة العنصر الحالي من سلة التسوق بشكل تدريجي وهذا لتوفير الذاكرة والاداء
      yield item


  # -----------------------------------

  def get_total(self):
    
    # لجلب الاسعار وضربها في الكمية للحصول علي السعر الكلي لجميع المنتجات بكمياتهم
    return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())