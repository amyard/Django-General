from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, View


from orders.models import OrderItem,Order
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

            # set the order in the session
            request.session['order_id'] = order.id

            # redirect for payment
            return redirect(reverse('payment:process'))




# PRINT PDF ORDERS
class AdminOrderDetailView(View):

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(AdminOrderDetailView, self).dispatch(*args, **kwargs)

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'admin/orders/detail.html', {'order': order})
