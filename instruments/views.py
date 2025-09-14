from django.shortcuts import render
from django.http import HttpResponse
from instruments.models import Inventory

def create_rental(request):
    """
    Renders the Rental creation form with inventory items.
    The form is submitted via JavaScript POST to the REST API endpoint.
    """
    inventory_items = Inventory.objects.all().order_by('item')
    return render(request, "instruments/create_rental.html", {
        "inventory_items": inventory_items
    })

def rental_success(request):
    """
    Simple success page for Rentals (not used by JS POST, kept for fallback/consistency).
    """
    return HttpResponse("Rental created successfully!")