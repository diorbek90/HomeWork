from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category, Review, Product

from .serializers import ProductSerializer, ReviewSerilizer, CategorySerializer, ProductReviewsSerializer


@api_view(http_method_names=['GET'])
def product_list_api(request):
    product = Product.objects.all()
    data = ProductSerializer(product, many=True).data

    return Response(data=data)

@api_view(http_method_names=['GET'])
def product_detail_api(request, id):
    product = Product.objects.get(id=id)
    data = ProductSerializer(product, many=False).data

    return Response(data=data)

@api_view(http_method_names=['GET'])
def category_list_api(request):
    category = Category.objects.all()
    data = CategorySerializer(category, many=True).data
    
    return Response(data = data)

@api_view(http_method_names=['GET'])
def category_detail_api(request, id):
    category = Category.objects.get(id=id)
    data = CategorySerializer(category, many=False).data
    
    return Response(data = data)

@api_view(http_method_names=['GET'])
def review_list_api(request):
    review = Review.objects.all()
    data = ReviewSerilizer(review, many=True).data
    return Response(data=data)

@api_view(http_method_names=['GET'])
def review_detail_api(request, id):
    review = Review.objects.get(id=id)
    data = ReviewSerilizer(review, many=False).data
    return Response(data=data)


@api_view(http_method_names=['GET'])
def product_reviews_api(request):
    product = Product.objects.all()
    data = ProductReviewsSerializer(product, many=True).data
    return Response(data=data)


