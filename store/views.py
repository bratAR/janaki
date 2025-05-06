from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render
from .models import Order


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
        product = get_object_or_404(Product, id=int(product_id))  # Cast to int here
        subtotal = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
        total += subtotal

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })

# ✅ Stage 2: Add to cart via URL (e.g., /add-to-cart/1/)
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('home')  # or wherever you want to go after adding

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
    data = json.loads(request.body)
    product_id = str(data['product_id'])
    quantity = int(data['quantity'])

    cart = request.session.get('cart', {})
    cart[product_id] = quantity
    request.session['cart'] = cart

    # Build a cart response like the JS expects
    from .models import Product
    items = []
    total = 0

    for pid, qty in cart.items():
        try:
            product = Product.objects.get(id=pid)
            subtotal = product.price * qty
            items.append({
                'product_id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': qty,
                'subtotal': subtotal,
            })
            total += subtotal
        except Product.DoesNotExist:
            continue

    return JsonResponse({'success': True, 'cart': {'items': items, 'total': total}})

# AJAX - Remove item
def ajax_remove_from_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart = request.session.get('cart', {})
        cart.pop(product_id, None)
        request.session['cart'] = cart
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def place_order(request):
    if request.method == 'POST':
        customer_email = request.POST.get('janakiverity5151@gmail.com')

        send_mail(
            'Order Confirmation - Janaki Verity',
            'Thank you for your order! We have received it and are processing it.',
            settings.EMAIL_HOST_USER,
            [customer_email],
            fail_silently=False,
        )

        request.session['cart'] = {}  # Clear cart

        return redirect('thankyou')

# Checkout view
from django.core.mail import send_mail
from django.conf import settings

def checkout_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment_method')
        email = request.POST.get('email')  # You need to add this field in your HTML form!

        # Send email
        send_mail(
            subject='Order Confirmation - Janaki Verity',
            message=f'Thank you {name} for your order!\n\n'
                    f'Order Details:\n'
                    f'Name: {name}\n'
                    f'email: {email}\n'
                    f'Address: {address}\n'
                    f'Phone: {phone}\n'
                    f'Payment Method: {payment_method}\n'
                    f'We will contact you soon.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        # Clear cart and redirect
        request.session['cart'] = {}
        return redirect('thankyou')

    return render(request, 'checkout.html')


# Thank you page
def thank_you_view(request):
    return render(request, 'thankyou.html')

def about_view(request):
    return render(request, 'store/about.html')

def contact_view(request):
    return render(request, 'store/contact.html')

