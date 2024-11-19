import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.http import HttpResponse


def hello_world(request):
    return HttpResponse('Hello, World!')


@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        products = list(Product.objects.values('id', 'name', 'price', 'available'))
        return JsonResponse(products, safe=False)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            price = data.get('price')
            available = data.get('available')
            if not name or price is None or available is None:
                return HttpResponseBadRequest("Missing part of the request body.")
            if price < 0:
                return HttpResponseBadRequest("Price must be a positive value.")
            product = Product(name=name, price=Decimal(str(price)), available=available)
            product.full_clean()
            product.save()
            return JsonResponse({
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'available': product.available
            }, status=201)
        except (ValidationError, ValueError) as e:
            return HttpResponseBadRequest(f"Invalid data: {e}")
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON format.")
    else:
        return HttpResponseBadRequest("Unsupported method.")


@csrf_exempt
def product_detail(request, product_id):
    if request.method == 'GET':
        try:
            product = Product.objects.get(id=product_id)
            return JsonResponse({
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'available': product.available
            })
        except Product.DoesNotExist:
            return HttpResponseNotFound("Product with this ID does not exist.")

    elif request.method == 'POST':
        if Product.objects.filter(id=product_id).exists():
            return HttpResponseBadRequest("Product with that ID already exists.")
        else:
            try:
                data = json.loads(request.body)
                name = data.get('name')
                price = data.get('price')
                available = data.get('available')
                if not name or price is None or available is None:
                    return HttpResponseBadRequest("Missing part of the request body.")
                if price < 0:
                    return HttpResponseBadRequest("Price must be a positive value.")
                product = Product(id=product_id, name=name, price=Decimal(str(price)), available=available)
                product.full_clean()
                product.save()
                return JsonResponse({
                    'id': product.id,
                    'name': product.name,
                    'price': float(product.price),
                    'available': product.available
                }, status=201)
            except (ValidationError, ValueError) as e:
                return HttpResponseBadRequest(f"Invalid data: {e}")
            except json.JSONDecodeError:
                return HttpResponseBadRequest("Invalid JSON format.")
    else:
        return HttpResponseBadRequest("Unsupported method.")
