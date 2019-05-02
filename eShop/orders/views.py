from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, View
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string


from orders.models import OrderItem,Order
from orders.forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created

import weasyprint



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




# ORDER DETAIL AND PRINT PDF ORDERS FROM DETAIL -> BUTTON
class AdminOrderDetailView(View):

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(AdminOrderDetailView, self).dispatch(*args, **kwargs)

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'admin/orders/detail.html', {'order': order})




# PRINT PDF ORDERS DIRECT FROM ADMIN PANEL
class AdminOrderPDFView(View):

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(AdminOrderPDFView, self).dispatch(*args, **kwargs)

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        html = render_to_string('orders/pdf.html', {'order': order})
        response = HttpResponse(content_type='application/pdf')

        response['Content-Disposition'] = 'filename="order_{}.pdf"'.format(order.id)
        weasyprint.HTML(string=html).write_pdf(response,
                                               stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/css/pdf.css')])
        return response