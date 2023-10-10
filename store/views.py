from django.shortcuts import render
from .models import Category,Product
from django.shortcuts import get_object_or_404
# Create your views here.

def store(request):
  all_product = Product.objects.all()
  context = {
    'all_product' : all_product,
  }
  return render(request, 'store/store.html',context)



def categories(request):
  all_categories = Category.objects.all()
  return {'all_categories':all_categories}


def category_list(request, category_slug=None):
  category = get_object_or_404(Category, slug=category_slug)
  product = Product.objects.filter(category=category)

  context = {
    'category' : category,
    'product' : product
  }
  return render(request, 'store/category_list.html', context)

def product_detail(request, product_slug):
  detail = get_object_or_404(Product, slug=product_slug)

  context = {
    'detail':detail
  }

  return render(request, 'store/product_detail.html', context)