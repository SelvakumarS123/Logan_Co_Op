from distutils.command.upload import upload
from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500,blank=True)
    price = models.IntegerField()
    product_image = models.ImageField(upload_to = 'photos/products',)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # when category is deleted, the product associated with that category will also get deleted
    created_date = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now = True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug]) #this product->category->slug(in Category model)

    def __str__(self):
        return self.product_name