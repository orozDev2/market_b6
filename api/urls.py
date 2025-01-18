from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('images', views.ImageViewSet)
router.register('attributes', views.AttributeViewSet)
router.register('categories', views.CategoryViewSet)
router.register('tags', views.TagViewSet)

urlpatterns = [
    path('auth/', include('api.auth.urls')),
    path('', include(router.urls))
]
