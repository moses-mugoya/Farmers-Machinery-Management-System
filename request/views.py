from django.shortcuts import render, get_object_or_404
from .models import Request
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.auth.decorators import login_required


@login_required
def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                Request.objects.create(order=order,
                                       user=request.user,
                                       product=item['product'],
                                       price=item['price'],
                                       quantity=item['quantity'])
                item.product.stock = item.product.stock - item['quantity']
                item.product.save()
                item.save()
            cart.clear()
            return render(request, 'request/order_created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'request/order_create.html', {'cart': cart, 'form': form})
