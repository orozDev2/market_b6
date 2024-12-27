from django.urls import path, include

from . import views

urlpatterns = [
    path('products/', views.product_list, name='product-list'),
    path('products/images/', views.upload_product_image),
    path('products/images/<int:pk>/', views.delete_product_image),
    path('products/attributes/', views.create_product_attribute),
    path('products/attributes/<int:pk>/', views.delete_update_product_attribute),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('categories/', views.category_list, name='category-list'),
    path('categories/<int:pk>/', views.category_detail, name='category-detail'),
    path('tags/', views.tag_list, name='tag-list'),
    path('tags/<int:pk>/', views.tag_detail, name='tag-detail'),

    path('auth/', include('api.auth.urls'))
]
