from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('<slug:category_slug>/', views.all_products,
         name='product_categories'),
    path('<slug:category_slug>/<slug:subcategory_slug>/',
         views.all_products, name='product_subcategories'),
    path('<slug:category_slug>/<slug:subcategory_slug>/<slug:product_slug>/',
         views.product_detail, name='product_detail')
]
