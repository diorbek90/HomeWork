

from django.urls import path
from product.views import *


urlpatterns = [
    path('categories/', CategoryListApiView.as_view()),
    path('categories/<int:id>/', CategoryDetailListView.as_view()),
    path('products/', ProductListApi.as_view()),
    path('products/<int:id>/', ProductDetailView.as_view()),
    path('reviews/', ReviewListAPiView.as_view()),
    path('reviews/<int:id>/', ReviewDetailApi.as_view()),
    path('products/reviews/', ProductReviewApi.as_view()),
]