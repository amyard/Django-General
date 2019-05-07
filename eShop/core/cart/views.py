from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from django.views.generic import View

from core.product.models import Product
from core.cart.cart import Cart
from core.cart.forms import CartAddProductForm




class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            cart.add(product=product, quantity=data['quantity'], update_quantity=data['update'])
        return redirect('cart:cart_detail')

# @require_POST
# def cart_add(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     form = CartAddProductForm(request.POST)
#     if form.is_valid():
#         data = form.cleaned_data
#         cart.add(product=product, quantity=data['quantity'], update_quantity=data['update'])
#     return redirect('cart:cart_detail')



class CartDeleteView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('cart:cart_detail')


# def cart_remove(request, product_id):
    # cart = Cart(request)
    # product = get_object_or_404(Product, id=product_id)
    # cart.remove(product)
    # return redirect('cart:cart_detail')


class CartListView(View):
    def get(self, request):
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],'update': True})
        return render(request, 'cart/detail.html', {'cart': cart})


# def cart_detail(request):
#     cart = Cart(request)
#     for item in cart:
#         item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],'update': True})
#     return render(request, 'cart/detail.html', {'cart': cart})