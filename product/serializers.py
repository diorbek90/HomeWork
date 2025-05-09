from rest_framework import serializers
from .models import Category, Product, Review

class CategorySerializer(serializers.ModelSerializer):

    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = 'id name products_count'.split()

    def get_products_count(self, category):
        return category.products.all().count() 

class ReviewSerilizer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = 'title description price category'.split()

class ProductReviewsSerializer(serializers.ModelSerializer):

    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'title description price category reviews rating'.split()

    def get_reviews(self, product):
        return ReviewSerilizer(product.reviews.all(), many=True).data

    def get_rating(self, product):
        return sum([i.stars for i in product.reviews.all()]) / product.reviews.all().count()


