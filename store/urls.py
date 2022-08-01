from django.urls import path
from . import views

urlpatterns = [
    path('',views.Store, name='store'),
    path('category/<slug:category_slug>/',views.Store, name = 'products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/',views.ProductDetail, name = 'product_detail'),
    path('search/',views.search, name='search')
]