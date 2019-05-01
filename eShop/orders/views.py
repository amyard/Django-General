from django.shortcuts import render
from django.views.generic import CreateView
from orders.models import OrderItem
from orders.forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created


class OrderCreateView(CreateView):

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        form = OrderCreateForm()
        return render(request, 'orders/create.html', {'cart': cart, 'form': form})

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                         quantity=item['quantity'])

            # cleat the cart
            cart.clear()

            # launch asynchronous task
            order_created.delay(order.id)

            return render(request, 'orders/created.html', {'order': order})