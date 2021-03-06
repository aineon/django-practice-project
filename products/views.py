from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category, Subcategory
import random


def all_products(request):
    """ A view to show all products, including sorting and searching """

    products = Product.objects.all()
    query = None
    categories = None
    subcategories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if sortkey == 'subcategory':
                sortkey = 'subcategory__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)
            subcategories = Subcategory.objects.filter(category__in=categories)

        if 'subcategory' in request.GET:
            subcategories = request.GET['subcategory'].split(',')
            products = products.filter(subcategory__name__in=subcategories)
            subcategories = Subcategory.objects.filter(name__in=subcategories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,
                               ("You didn't enter any search criteria!"))
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(
                        description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    # if category_slug is not None:
    # cat = Category.objects.get(slug=category_slug)
    # if subcategory_slug is not None:
    # subcat = Subcategory.objects.get(slug=subcategory_slug)

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_subcategories': subcategories,
        'current_sorting': current_sorting,
        # 'cat': cat,
        # 'subcat': subcat,
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
