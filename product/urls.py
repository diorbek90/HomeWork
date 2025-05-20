

from django.urls import path
from product.views import *


urlpatterns = [
    path('categories/', category_list_api),
    path('categories/<int:id>/', category_detail_api),
    path('products/', product_list_api),
    path('products/<int:id>/', product_detail_api),
    path('reviews/', review_list_api),
    path('reviews/<int:id>/', review_detail_api),
    path('products/reviews/', product_reviews_api),
]