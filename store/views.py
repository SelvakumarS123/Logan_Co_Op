from tkinter import E
from django.shortcuts import get_object_or_404, render
from category.models import Category
from . models import Product

# Create your views here.
def Store(request, category_slug = None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category,slug = category_slug) 
        products = Product.objects.filter(category = categories,is_available =True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()
    context = {
        'products':products,'product_count' : products.count()
    }
    return render(request, 'store/store.html',context)

def ProductDetail(request, category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug) #'category'-> 'Product' model, '__'-> syntax, 'slug'-> from 'Category' model
    except Exception as e:
        raise e
    context={'single_product':single_product}
    return render(request,'store/product_detail.html',context=context)