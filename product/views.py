from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Category, Review, Product
from .serializers import ProductSerializer, ReviewSerilizer, CategorySerializer,ProductReviewsSerializer, ProductValidateSerializer,CategoryValidateSerializer, ReviewValidateSerializer
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView

class ProductListApi(APIView):

    def get(self, request):
        product = Product.objects.all()
        data = ProductSerializer(product, many=True).data

        return Response(data=data)
    
    def post(self, request):
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

class ProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        
        if self.request.method == 'PUT':
            return ProductValidateSerializer
        return ProductSerializer
    
    def update(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(data=request.data)  
        serializer.is_valid(raise_exception=True)

        product.title = serializer.validated_data['title']
        product.description = serializer.validated_data['description']
        product.price = serializer.validated_data['price']
        product.category_id = serializer.validated_data['product_id']
        product.save()

        return Response(status=status.HTTP_201_CREATED, data=self.get_serializer(product).data)
    
    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CategoryListApiView(APIView):

    def get(self, request):
        category = Category.objects.all()
        data = CategorySerializer(category, many=True).data
        return Response(data=data)
    
    def post(self, request):
        serializer = CategoryValidateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        name = serializer.validated_data.get('name')

        category = Category.objects.create(
            name=name
        )

        return Response(status=status.HTTP_201_CREATED,
                        data=CategorySerializer(category).data)

class CategoryDetailListView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    lookup_field = 'id'
    def get_serializer_class(self, *args, **kwargs):
        
        if self.request.method == "PUT":
            return CategoryValidateSerializer
        return CategorySerializer
    
    def update(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer(data=request.data)  
        serializer.is_valid(raise_exception=True)

        category.name = serializer.validated_data.get('name')
        category.save()

        return Response(status=status.HTTP_201_CREATED, data=self.get_serializer(category).data)
    
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ReviewListAPiView(APIView):
    
    def get(self, request):
        review = Review.objects.all()
        data = ReviewSerilizer(review, many=True).data
        return Response(data=data)
    
    def post(self, request):
        serializer = ReviewValidateSerializer(data=request.data)

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

class ReviewDetailApi(RetrieveUpdateDestroyAPIView):

    queryset = Review.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ReviewValidateSerializer
        return ReviewSerilizer
    
    def update(self, request, *args, **kwargs):
        review = self.get_object()
        serializer = self.get_serializer(data=request.data)  
        serializer.is_valid(raise_exception=True)

        review.text = serializer.validated_data['text']
        review.stars = serializer.validated_data['stars']
        review.product_id = serializer.validated_data['product_id']
        review.save()

        return Response(status=status.HTTP_201_CREATED, data=self.get_serializer(review).data)
    
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
        

class ProductReviewApi(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductReviewsSerializer




