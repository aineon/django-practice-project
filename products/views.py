from django.shortcuts import render, get_object_or_404
from .models import Product
import random


def all_products(request):
    """ A view to show all products, including sorting and searching """

    products = Product.objects.all()
    
    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """A view to shoe individual product details"""

    product = get_object_or_404(Product, pk=product_id)
    all_products = list(Product.objects.all())
    rand_products = random.sample(all_products, 7)

    context = {
        'product': product,
        'rand_products': rand_products,
    }

    return render(request, 'products/product_detail.html', context)
