from django.shortcuts import render

from django_ts_gems.inventories.models import Inventory

def product_view(request):
    
    # products = Bracelet.objects.all()
    products = Inventory.objects.filter(content_type__model="ring").prefetch_related()
    print(products)

    # products = Inventory.objects.filter(content_type=ContentType.objects.get_for_model(Ring))

    
    context = {
        'products': products
    }
    
    return render(request, 'products.html', context)
