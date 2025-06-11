from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from .models import Category, Review, Product
from .serializers import (
    ProductSerializer, ReviewSerilizer, CategorySerializer,
    ProductReviewsSerializer, ProductValidateSerializer,
    CategoryValidateSerializer, ReviewValidateSerializer
)
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from common.permission import IsAuthenticatedOrReadOnly, IsSuperUser, IsStaff
from rest_framework.permissions import AllowAny


class ProductListApi(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        products = Product.objects.all()
        data = ProductSerializer(products, many=True).data
        return Response(data=data)

    @swagger_auto_schema(request_body=ProductValidateSerializer)
    def post(self, request):
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        with transaction.atomic():
            product = Product.objects.create(
                title=serializer.validated_data['title'],
                description=serializer.validated_data['description'],
                price=serializer.validated_data['price'],
                category_id=serializer.validated_data['category_id'],
                owner=request.user
            )

        return Response(status=status.HTTP_201_CREATED, data=ProductSerializer(product).data)


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
        product.category_id = serializer.validated_data['category_id']
        product.save()

        return Response(status=status.HTTP_201_CREATED, data=ProductSerializer(product).data)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class CategoryListApiView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly | IsSuperUser]

    def get(self, request):
        categories = Category.objects.all()
        data = CategorySerializer(categories, many=True).data
        return Response(data=data)

    @swagger_auto_schema(request_body=CategoryValidateSerializer)
    def post(self, request):
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        category = Category.objects.create(name=serializer.validated_data['name'])
        return Response(status=status.HTTP_201_CREATED, data=CategorySerializer(category).data)


class CategoryDetailListView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    lookup_field = 'id'
    permission_classes = [IsSuperUser]

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return CategoryValidateSerializer
        return CategorySerializer

    def update(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category.name = serializer.validated_data['name']
        category.save()

        return Response(status=status.HTTP_201_CREATED, data=CategorySerializer(category).data)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ReviewListAPiView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        reviews = Review.objects.all()
        data = ReviewSerilizer(reviews, many=True).data
        return Response(data=data)

    @swagger_auto_schema(request_body=ReviewValidateSerializer)
    def post(self, request):
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        review = Review.objects.create(
            text=serializer.validated_data['text'],
            stars=serializer.validated_data['stars'],
            product_id=serializer.validated_data['product_id'],
            owner=request.user
        )

        return Response(status=status.HTTP_201_CREATED, data=ReviewSerilizer(review).data)


class ReviewDetailApi(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    lookup_field = 'id'
    permission_classes = [IsStaff]

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

        return Response(status=status.HTTP_201_CREATED, data=ReviewSerilizer(review).data)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ProductReviewApi(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductReviewsSerializer
    permission_classes = [AllowAny]
