import pytz
from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404, redirect
from .models import Machine, Category
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages
from cart.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required
from django.db.models import Max


def product_list(request, category_slug=None):
    category = None
    harvest = Category.objects.get(name='Harvesting')
    sowing = Category.objects.get(name='Sowing and Tillage Equipments')
    forage = Category.objects.get(name='Forage Equipments')
    sprayers = Category.objects.get(name='Sprayers')
    categories = Category.objects.all()
    products = Machine.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    paginator = Paginator(products, 12)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    cart_product_form = CartAddProductForm()
    return render(request, 'machine/list.html', {'category': category,
                                                 'categories': categories,
                                                 'page': page,
                                                 'products': products,
                                                 'sowing': sowing,
                                                 'harvest': harvest,
                                                 'forage': forage,
                                                 'sprayers': sprayers,
                                                 'cart_product_form': cart_product_form
                                                 })


def product_detail(request, id, slug):
    product = get_object_or_404(Machine, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'machine/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})









