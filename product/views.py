from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Category, Review, Product

from .serializers import ProductSerializer, ReviewSerilizer, CategorySerializer, ProductReviewsSerializer


@api_view(http_method_names=['GET', 'POST'])
def product_list_api(request):

    if request.method == 'GET':
        product = Product.objects.all()
        data = ProductSerializer(product, many=True).data

        return Response(data=data)
    
    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category_id = request.data.get('category_id')

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
        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.category_id = request.data.get('product_id')
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

        name = request.data.get('name')

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
        category.name = request.data.get('name')
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

        text = request.data.get('text')
        stars = request.data.get('stars')
        product_id=request.data.get('product_id')

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
        review.text = request.data.get('text')
        review.stars = request.data.get('stars')
        review.product_id = request.data.get("product_id")
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


