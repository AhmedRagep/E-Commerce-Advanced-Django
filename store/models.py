from django.db import models
from django.urls import reverse
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True) # لتسريع البحث في قاعدة البيانات

    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'التصنيفات'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_list", args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name="product", on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=250)
    brand = models.CharField(max_length=100, default='not-brand')
    description = models.TextField(blank=True) #لجعل الفارغ صحيح ومقبول
    slug = models.SlugField(max_length=200)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'المنتجات'

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.slug])
    