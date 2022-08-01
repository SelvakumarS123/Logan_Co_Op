from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from category.models import Category
from carts.models import CartItem
from . models import Product
from carts.views import _CartId
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
# Create your views here.
def Store(request, category_slug = None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category,slug = category_slug) 
        products = Product.objects.filter(category = categories,is_available =True)
        paginator = Paginator(products,1)
        page = request.GET.get('page') #CAPTURED FROM THE REQUEST
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products,3)
        page = request.GET.get('page') #CAPTURED FROM THE REQUEST
        paged_products = paginator.get_page(page) #6 products will get stored into this paged_product
        product_count = products.count()
    context = {
        'products':paged_products,'product_count' : products.count()
    }
    return render(request, 'store/store.html',context)

def ProductDetail(request, category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug) #'category'-> 'Product' model, '__'-> syntax, 'slug'-> from 'Category' model
        in_cart = CartItem.objects.filter(cart__cart_id=_CartId(request),product=single_product).exists()

    except Exception as e:
        raise e
    context={'single_product':single_product,'in_cart':in_cart}
    return render(request,'store/product_detail.html',context=context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    return render(request, 'store/store.html',{'products':products,'product_count':product_count})