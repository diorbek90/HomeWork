from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Category, Review, Product

from .serializers import ProductSerializer, ReviewSerilizer, CategorySerializer,ProductReviewsSerializer, ProductValidateSerializer,CategoryValidateSerializer, ReviewValidateSerializer
from django.db import transaction

@api_view(http_method_names=['GET', 'POST'])
def product_list_api(request):

    if request.method == 'GET':
        product = Product.objects.all()
        data = ProductSerializer(product, many=True).data

        return Response(data=data)
    
    elif request.method == 'POST':
        serializer = ProductValidateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        
        with transaction.atomic():
            title = serializer.validated_data.get('title')
            description = serializer.validated_data.get('description')
            price = serializer.validated_data.get('price')
            category_id = serializer.validated_data.get('category_id')

            product = Product.objects.create(
                title=title,
                description=description,
                price=price,
                category_id=category_id
            )

        return Response(status=status.HTTP_201_CREATED,
                            data=ProductSerializer(product).data)

@api_view(http_method_names=['GET', 'PUT', "DELETE"])
def product_detail_api(request, id):

    try:
        product = Product.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        data = ProductSerializer(product).data
        return Response(data=data)

    elif request.method == "PUT":
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product.title = serializer.validated_data.get('title')
        product.description = serializer.validated_data.get('description')
        product.price = serializer.validated_data.get('price')
        product.category_id = serializer.validated_data.get('product_id')
        product.save()
        
        return Response(status=status.HTTP_201_CREATED,
                        data=ProductSerializer(product).data)
    elif request.method == "DELETE":
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

    return Response(data=data)

@api_view(http_method_names=['GET', 'POST'])
def category_list_api(request):

    if request.method == 'GET':
        category = Category.objects.all()
        data = CategorySerializer(category, many=True).data
    
        return Response(data = data)
    
    elif request.method == 'POST':
        serializer = CategoryValidateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        name = serializer.validated_data.get('name')

        category = Category.objects.create(
            name=name
        )

        return Response(status=status.HTTP_201_CREATED,
                        data=CategorySerializer(category).data)

@api_view(http_method_names=['GET', 'PUT', "DELETE"])
def category_detail_api(request, id):

    try:

        category = Category.objects.get(id=id)

    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        data = CategorySerializer(category, many=False).data
        return Response(data = data)
    
    elif request.method == "PUT":
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category.name = serializer.validated_data.get('name')
        category.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=CategorySerializer(category).data)
    
    elif request.method == "DELETE":
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(http_method_names=['GET', 'POST'])
def review_list_api(request):

    if request.method == 'GET':
        review = Review.objects.all()
        data = ReviewSerilizer(review, many=True).data
        return Response(data=data)

    elif request.method == "POST":

        serializer = ReviewSerilizer(data=request.data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        
        
        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        product_id=serializer.validated_data.get('product_id')

        review = Review.objects.create(
            text=text,
            stars=stars,
            product_id=product_id
        )


        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewSerilizer(review).data)

@api_view(http_method_names=['GET', 'PUT', "DELETE"])
def review_detail_api(request, id):

    try:

        review = Review.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

    if request.method == "GET":
        data = ReviewSerilizer(review, many=False).data
        return Response(data=data)
    
    elif request.method == "PUT":
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        review.text = serializer.validated_data.get('text')
        review.stars = serializer.validated_data.get('stars')
        review.product_id = serializer.validated_data.get("product_id")
        review.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewSerilizer(review).data)
    elif request.method == "DELETE":
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    


@api_view(http_method_names=['GET'])
def product_reviews_api(request):
    product = Product.objects.all()
    data = ProductReviewsSerializer(product, many=True).data
    return Response(data=data)


