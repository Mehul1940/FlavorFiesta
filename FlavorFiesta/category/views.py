from django.shortcuts import render, get_object_or_404
from .models import Category
from food.models import Item  # Adjust if your products are in a different app

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category/category_list.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Item.objects.filter(category=category)  # Assuming your Product model has a `category` FK
    return render(request, 'category/category_detail.html', {
        'category': category,
        'products': products
    })
