from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from django.views.decorators.http import require_POST
from django.http import JsonResponse

def home(request):
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'store/home.html', {
        'categories': categories,
        'products': products,
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
    cart[product_id] = cart.get(product_id, 0) + 1  # Increment quantity
    request.session['cart'] = cart
    return redirect('cart')

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
        total += subtotal
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

    
    products = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        products.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
        total += subtotal
    return render(request, 'cart.html', {'cart_items': products, 'total': total})

def ajax_add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart = request.session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + 1
        request.session['cart'] = cart
        return JsonResponse({'success': True, 'cartCount': sum(cart.values())})
    return JsonResponse({'success': False})

def ajax_update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        if quantity > 0:
            cart[product_id] = quantity
        else:
            cart.pop(product_id, None)
        request.session['cart'] = cart
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def ajax_remove_from_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart = request.session.get('cart', {})
        cart.pop(product_id, None)
        request.session['cart'] = cart
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

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
