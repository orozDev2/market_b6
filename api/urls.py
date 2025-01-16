from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('products', views.ProductViewSet)

urlpatterns = [
    path('products/images/', views.UploadProductImage.as_view()),
    path('products/images/<int:id>/', views.DetailProductImage.as_view()),
    path('products/attributes/', views.ListProductAttribute.as_view()),
    path('products/attributes/<int:id>/', views.DetailProductAttribute.as_view()),
    path('products/categories/', views.ListProductCategory.as_view()),
    path('products/categories/<int:id>/', views.DetailProductCategory.as_view()),
    path('products/tags/', views.ListProductTag.as_view()),
    path('products/tags/<int:id>/', views.DetailProductTag.as_view()),
    path('auth/', include('api.auth.urls')),
    path('', include(router.urls))
]
