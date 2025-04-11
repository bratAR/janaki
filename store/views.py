from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from django.views.decorators.http import require_POST

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'store/home.html', {
        'categories': categories,
        'products': products
    })

@require_POST
def update_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart[product_id_str] = quantity
        else:
            cart.pop(product_id_str, None)
    except ValueError:
        pass  # Ignore invalid input

    request.session['cart'] = cart
    return redirect('cart')

from django.shortcuts import render, redirect

def checkout_view(request):
    if request.method == 'POST':
        # Clear the cart as part of the checkout process (mock action)
        request.session['cart'] = {}
        # Redirect to the 'thankyou' page after checkout
        return redirect('thankyou')

    return render(request, 'checkout.html')

def thank_you_view(request):
    # Simply render the thank-you page
    return render(request, 'thankyou.html')


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

def cart_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        return render(request, 'cart.html', {'message': 'Your cart is empty!'})
    
    products = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        products.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
        total += subtotal
    return render(request, 'cart.html', {'cart_items': products, 'total': total})


# store/views.py
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart

    return redirect('cart')


def checkout_view(request):
    # Clear cart for now as a simple "checkout"
    request.session['cart'] = {}
    return render(request, 'checkout.html')
# Create your views here.
