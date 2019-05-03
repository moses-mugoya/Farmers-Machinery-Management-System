from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from machine.models import Machine
from .cart import Cart
from .forms import CartAddProductForm
from django.contrib import messages


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Machine, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        if cd['quantity'] > product.stock:
            messages.error(request, 'Please check the available number of this machine. The available number is {}'.format(product.stock))
            return redirect('machine:product_list')
        else:
            cart.add(product=product,
                     quantity=cd['quantity'],
                     update_quantity=cd['update'])
    return redirect('machine:product_list')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Machine, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})


