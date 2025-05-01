from django.shortcuts import render, get_object_or_404, redirect
from food.models import Item
from .models import CartItem , Order, OrderItem
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from decimal import Decimal

def product_list(request):
    products = Item.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Item, pk=pk)
    ingredients = product.ingredients.split(',') if product.ingredients else []

    context = {
        'product': product,
        'ingredients': ingredients,
    }
    return render(request, 'shop/product_detail.html', context)


def add_to_cart(request, pk):
    product = get_object_or_404(Item, pk=pk)
    session_key = request.session.session_key or request.session.save()

    cart_item, created = CartItem.objects.get_or_create(
        session_key=request.session.session_key,
        item=product
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} added to cart.")
    return redirect('shop:cart')

@login_required
def cart(request):
    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(session_key=session_key)
    total = sum(item.get_total() for item in cart_items)
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total': total})

@require_http_methods(["DELETE"])
def remove_from_cart(request, item_id):
    session_key = request.session.session_key
    if not session_key:
        return JsonResponse({'success': False, 'error': 'Session not found'}, status=400)
    
    try:
        cart_item = CartItem.objects.get(item_id=item_id, session_key=session_key)
        cart_item.delete()
        cart_total = calculate_cart_total(session_key)
        return JsonResponse({
            'success': True,
            'cart_total': cart_total,
            'message': 'Item removed from cart.'
        })
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item not in cart'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def update_cart_quantity(request, item_id):
    try:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        
        cart_item = CartItem.objects.get(item_id=item_id, session_key=session_key)
        
        change = int(request.GET.get('change', 0))
        
        new_quantity = cart_item.quantity + change
        
        if new_quantity <= 0:
            cart_item.delete()
            cart_total = calculate_cart_total(session_key)
            return JsonResponse({
                'success': True, 
                'removed': True,
                'cart_total': cart_total
            })
        else:
            cart_item.quantity = new_quantity
            cart_item.save()
            
            new_total = cart_item.get_total()
            cart_total = calculate_cart_total(session_key)
            
            return JsonResponse({
                'success': True,
                'new_quantity': new_quantity,
                'new_total': new_total,
                'cart_total': cart_total
            })
    except Exception as e:
        print(f"Error in update_cart_quantity: {e}")
        return JsonResponse({'success': False, 'error': str(e)})

def calculate_cart_total(session_key):
    cart_items = CartItem.objects.filter(session_key=session_key)
    total = sum(item.get_total() for item in cart_items)
    return total

@login_required
def checkout(request):
    # Ensure that the cart is not empty
    cart_items = CartItem.objects.filter(session_key=request.session.session_key)
    
    if not cart_items:
        return HttpResponse("Your cart is empty. Please add items before checking out.")
    
    # Calculate total amount
    total_amount = sum(cart_item.get_total() for cart_item in cart_items)

    if request.method == 'POST':
        # Ensure that the shipping address is provided
        shipping_address = request.POST.get('shipping_address')
        if not shipping_address:
            return HttpResponse("Shipping address is required.")

        # Create an order
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            shipping_address=shipping_address,
            status="Pending"
        )
        
        # Create order items from the cart items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.item,
                quantity=cart_item.quantity,
                total=cart_item.get_total()
            )
        
        # Clear the cart (you can either delete or mark them as purchased)
        cart_items.delete()
        
        # Redirect the user to an order confirmation page
        return redirect('shop:order_confirmation', order_id=order.id)
    
    # Handle GET request: display the checkout form
    return render(request, 'shop/checkout.html', {'cart_items': cart_items, 'total_amount': total_amount})


@login_required
def order_confirmation(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return HttpResponse("Order not found.")
    
    return render(request, 'shop/order_confirmation.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/order_history.html', {'orders': orders})


def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = Decimal('0.00')

    for item_id, item_data in cart.items():
        # Assuming you have a Product model with fields: id, name, price, image
        product = Product.objects.get(pk=item_id)
        quantity = item_data['quantity']
        item_total = product.price * quantity
        total += item_total

        cart_items.append({
            'item': product,
            'quantity': quantity,
            'get_total': item_total,
        })

    shipping = Decimal('0.00')
    if total <= Decimal('500.00'):
        shipping = Decimal('70.00')
        total += shipping

    context = {
        'cart_items': cart_items,
        'total': total.quantize(Decimal('0.01')),  # round to 2 decimal places
    }

    return render(request, 'food/cart.html', context)
