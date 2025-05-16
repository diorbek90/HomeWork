from rest_framework import serializers
from .models import Category, Product, Review
from rest_framework.exceptions import ValidationError

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

# Валидация

class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField()


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField()
    stars = serializers.IntegerField()
    product_id = serializers.IntegerField(min_value=1, max_value=6)

    def validate_product_id(self, product_id):

        try:
            Product.objects.get(id=product_id)
        except:
            raise ValidationError("Review is not exist! ")
        return product_id
    

class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField(required=False)
    price = serializers.IntegerField(min_value=1)
    category_id = serializers.IntegerField()

    def validate_category_id(self, catogory_id):

        try:
            Category.objects.get(id=catogory_id)
        except:
            raise ValidationError("Category_id does not exist!")
        return catogory_id
    


