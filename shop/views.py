import stripe
from django.conf import settings
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from .models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY

def item_detail(request, id):
    item = get_object_or_404(Item, pk=id)
    return render(request, "shop/item_detail.html", {
        "item": item,
        "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
    })

def buy_item(request, id):
    item = get_object_or_404(Item, pk=id)
    # Для теста валюты используйте USD
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": item.currency,
                    "product_data": {
                        "name": item.name,
                        "description": item.description,
                    },
                    "unit_amount": item.price,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=request.build_absolute_uri(f"/item/{id}?success=1"),
            cancel_url=request.build_absolute_uri(f"/item/{id}?canceled=1"),
        )
        return JsonResponse({"session_id": session.id})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
def item_list(request):
    items = Item.objects.all()
    return render(request, "shop/item_list.html", {"items": items})


