from django.contrib import admin
from .models import Product,Category
# Register your models here.

@admin.register(Category)
class CatergoryAdmin(admin.ModelAdmin):
  # لمساواة الاسم بالسلج
  prepopulated_fields = {'slug' : ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug' : ('title',)}

