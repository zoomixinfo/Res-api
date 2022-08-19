from django.shortcuts import render
from .models import Drink
from .serializer import DrinkSerilaizer
from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def index(request):
    if request.method == 'GET':
        drinks = Drink.objects.all()
        serilaizer = DrinkSerilaizer (drinks, many=True)
        return JsonResponse({'drinks':serilaizer.data}, safe=False)
    if request.method == 'POST':
        serilaizer = DrinkSerilaizer(data=request.data)
        if serilaizer.is_valid():
            serilaizer.save()
            return JsonResponse(serilaizer.data, status=201)

@api_view(['GET', 'PUT', 'DELETE'])
def detail(request, id):
    try:
        drink = Drink.objects.get(pk=id)
    except Drink.DoesNotExist:
        return JsonResponse({'error':'Drink not found'}, status=404)
    if request.method == 'GET':
        serilaizer = DrinkSerilaizer(drink)
        return JsonResponse(serilaizer.data)
    elif request.method == 'PUT':
        serilaizer = DrinkSerilaizer(data=request.data)
        if serilaizer.is_valid():
            serilaizer.save()
            return JsonResponse(serilaizer.data)
        return JsonResponse(serilaizer.errors, status=400)
    elif request.method == 'DELETE':
        drink.delete()
        return JsonResponse({}, status=204)