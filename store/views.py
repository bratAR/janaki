from django.shortcuts import render
from .models import Product, Category

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'store/home.html', {
        'categories': categories,
        'products': products
    })

# Create your views here.
