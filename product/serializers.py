from rest_framework import serializers
from .models import Category, Product, Review

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = 'id name'.split()


    


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ReviewSerilizer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'
