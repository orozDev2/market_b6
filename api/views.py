from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from store.models import Tag, Category, Product, ProductImage, ProductAttribute
from .filters import ProductFilter
from .mixins import ProModelViewSet
from .paginations import SimplePagination
from .permissions import IsOwnerOrReadOnly, IsOwner
from .serializers import CategorySerializer, TagSerializer, UploadProductImageSerializer, \
    CreateProductAttributeSerializer, \
    UpdateProductAttributeSerializer, CreateProductImageSerializer, DetailProductImageSerializer, \
    ProductAttributeSerializer, ListAttributeSerializer, CreateUpdateCategorySerializer, DetailCategorySerializer, \
    CreateUpdateTagSerializer, DetailTagSerializer, ProductImageSerializer, ListProductSerializer, \
    CreateProductSerializer, DetailProductSerializer, UpdateProductSerializer, DetailProductAttributeSerializer
from rest_framework import serializers


filtering = [
    SearchFilter,
    DjangoFilterBackend,
    OrderingFilter,
]


class ProductViewSet(ProModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    lookup_field = 'id'
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'content']
    ordering_fields = ['price', 'name', 'created_at', 'rating']
    serializer_classes = {
        'list': ListProductSerializer,
        'create': CreateProductSerializer,
        'retrieve': DetailProductSerializer,
        'update': UpdateProductSerializer,
    }
    permission_classes_by_action = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'create': [IsAuthenticated],
        'update': [IsAuthenticated, IsOwner],
        'destroy': [IsAuthenticated, IsOwner],

    }
    pagination_class = SimplePagination


class ImageViewSet(ProModelViewSet):
    queryset = ProductImage.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly,  IsOwnerOrReadOnly]
    lookup_field = 'id'

    filter_backends = filtering
    search_fields = ['product']
    filterset_fields = ['product']
    ordering_fields = ['product']
    pagination_class = SimplePagination

    serializer_classes = {
        'list': ProductImageSerializer,
        'create': CreateProductImageSerializer,
        'update': UploadProductImageSerializer,
        'retrieve': DetailProductImageSerializer,
    }

    permission_classes_by_action = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'create': [IsAuthenticated],
        'update': [IsAuthenticated, IsOwner],
        'destroy': [IsAuthenticated, IsOwner],
    }


class AttributeViewSet(ProModelViewSet):
    queryset = ProductAttribute.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    lookup_field = 'id'
    filter_backends = filtering
    search_fields = ['name']
    filterset_fields = ['name']
    ordering_fields = ['name']
    pagination_class = SimplePagination
    serializer_classes = {
        'list': ProductAttributeSerializer,
        'create': CreateProductAttributeSerializer,
        'update': UpdateProductAttributeSerializer,
        'retrieve': DetailProductAttributeSerializer,
    }

    permission_classes_by_action = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'create': [IsAuthenticated],
        'update': [IsAuthenticated, IsOwner],
        'destroy': [IsAuthenticated, IsOwner],
    }

class CategoryViewSet(ProModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'
    filter_backends = filtering
    pagination_class = SimplePagination

    serializer_classes = {
        'list': CategorySerializer,
        'create': CreateUpdateCategorySerializer,
        'update': CreateUpdateCategorySerializer,
        'retrieve': DetailCategorySerializer,
    }

    permission_classes_by_action = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'create': [IsAuthenticated],
        'update': [IsAuthenticated, IsOwner],
        'destroy': [IsAuthenticated, IsOwner],
    }

class TagViewSet(ProModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    lookup_field = 'id'
    filter_backends = filtering
    pagination_class = SimplePagination

    serializer_classes = {
        'list': TagSerializer,
        'create': CreateUpdateTagSerializer,
        'update': CreateUpdateTagSerializer,
        'retrieve': DetailTagSerializer,
    }

    permission_classes_by_action = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'create': [IsAuthenticated],
        'update': [IsAuthenticated, IsOwner],
        'destroy': [IsAuthenticated, IsOwner],
    }


