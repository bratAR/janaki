# store/context_processors.py

from .cart import get_cart_data  # assuming you have this logic

def cart_item_count(request):
    cart = request.session.get('cart', {})
    total_items = sum(cart.values())
    return {'cart_item_count': cart_item_count}
