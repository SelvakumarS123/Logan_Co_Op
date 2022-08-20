from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import is_valid_path
from . forms import ReviewForm
from category.models import Category
from carts.models import CartItem
from . models import Product, ReviewRating
from carts.views import _CartId
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from . forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct

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

    #to see if the user has purchased this particular product
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user,product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct=None
    else:
        orderproduct=None

    #get the reviews
    reviews = ReviewRating.objects.filter(product_id = single_product.id , status =  True)
    
    context={'single_product':single_product,'in_cart':in_cart,'orderproduct':orderproduct,'reviews':reviews}
    return render(request,'store/product_detail.html',context=context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    return render(request, 'store/store.html',{'products':products,'product_count':product_count})

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER') #store the previous url #/CATEGORY/JEANS/ATX-JEANS/#
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user__id = request.user.id, product__id = product_id) #'user' is a foreign key in the 'ReviewRating' model
            form = ReviewForm(request.POST, instance=reviews) #request.POST will be having all the data
            #if you don't pass the 'instance', by default it will create a new review. if there is already a review by the user, then we need to update it.
            form.save()
            messages.success(request, 'Thank You! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form =ReviewForm(request.POST) #create new review
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank You! Your review has been submitted.')
                return redirect(url)

