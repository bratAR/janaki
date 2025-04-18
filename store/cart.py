def get_cart_data(request):
    cart = request.session.get('cart', {})
    items = []

    for product_id, item in cart.items():
        items.append({
            'product_id': product_id,
            'quantity': item.get('quantity', 0),
        })

    return {
        'items': items
    }
