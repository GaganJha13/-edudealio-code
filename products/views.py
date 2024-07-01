from django.shortcuts import render
from .models import (
    ProductsModel,
)

# Create your views here.


def product_list(request):
    context = {
        'products': ProductsModel.objects.all(),
    }
    return render(request, "products/product_list.html", context)
