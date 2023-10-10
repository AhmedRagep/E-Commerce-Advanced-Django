from django.db import models
from django.contrib.auth.models import User
from store.models import Product

# Create your models here.


class ShippingAddress(models.Model):

  full_name = models.CharField(max_length=300)

  email = models.EmailField(max_length=254)

  address1 = models.CharField(max_length=300)

  address2 = models.CharField(max_length=300)

  city = models.CharField(max_length=300)

  # optional

  state = models.CharField(max_length=300, null=True, blank=True)

  zipcode = models.CharField(max_length=300, null=True, blank=True)


  # fk

  # authenticated / not authenticated
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


  class Meta:

    verbose_name_plural = "Shippng Address"


  def __str__(self):
      return 'Shippng Address - ' + str(self.id)



class Order(models.Model):
   
  full_name = models.CharField(max_length=300)

  email = models.EmailField(max_length=300)

  shipping_address = models.TextField(max_length=10000)

  amount_paid = models.DecimalField(max_digits=8, decimal_places=2)

  date_orderd = models.DateTimeField(auto_now_add=True)

  #  fk
  # authenticated / not authenticated
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


  def __str__(self):
      return 'Order - # ' + str(self.id)
  

class OrderItem(models.Model):

  order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
  product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
   
  # حقل عدد صحيح ايجابي
  quantity = models.PositiveIntegerField(default=1)
  price = models.DecimalField(max_digits=8, decimal_places=2)

  #  fk
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


  def __str__(self):
      return 'Order - # ' + str(self.id) 