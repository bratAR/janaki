from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json

# Home page - with category filtering
def home(request):
    category_id = request.GET.get('category')
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'store/home.html', {
        'categories': categories,
        'products': products,
    })

# Cart view - show all items in cart with subtotal and total
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })
        total += subtotal

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

# ✅ Stage 2: Add to cart via URL (e.g., /add-to-cart/1/)
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    cart[product_id_str] = cart.get(product_id_str, 0) + 1
    request.session['cart'] = cart

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'cartCount': sum(cart.values())})

    return redirect('home')

# Remove item from cart
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('cart')

# Update cart item quantity (non-AJAX)
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
        pass

    request.session['cart'] = cart
    return redirect('cart')

# AJAX - Add to cart (manual endpoint if needed)
def ajax_add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = str(data.get('product_id'))

        cart = request.session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + 1
        request.session['cart'] = cart

        return JsonResponse({'success': True, 'cart_count': sum(cart.values())})
    return JsonResponse({'success': False})

# AJAX - Update item quantity
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

# AJAX - Remove item
def ajax_remove_from_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart = request.session.get('cart', {})
        cart.pop(product_id, None)
        request.session['cart'] = cart
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# Checkout view
def checkout_view(request):
    if request.method == 'POST':
        request.session['cart'] = {}  # Clear cart
        return redirect('thankyou')
    return render(request, 'checkout.html')

# Thank you page
def thank_you_view(request):
    return render(request, 'thankyou.html')
