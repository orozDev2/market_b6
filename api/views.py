from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from store.models import Tag, Category, Product, ProductImage, ProductAttribute
from .filters import ProductFilter
from .mixins import ProModelViewSet, PermissionByActionMixin, SerializerByActionMixin
from .paginations import SimplePagination
from .permissions import IsOwnerOrReadOnly, IsOwner, IsOwnerProduct, IsSuperuser
from .serializers import CategorySerializer, TagSerializer, CreateProductAttributeSerializer, \
    UpdateProductAttributeSerializer, CreateProductImageSerializer, ListProductSerializer, \
    CreateProductSerializer, DetailProductSerializer, UpdateProductSerializer

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


class ImageViewSet(
    PermissionByActionMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = ProductImage.objects.all()
    serializer_class = CreateProductImageSerializer
    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'destroy': [IsAuthenticated, IsOwnerProduct],
    }


class AttributeViewSet(
    SerializerByActionMixin,
    PermissionByActionMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = ProductAttribute.objects.all()
    lookup_field = 'id'
    serializer_classes = {
        'create': CreateProductAttributeSerializer,
        'update': UpdateProductAttributeSerializer,
    }
    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'update': [IsAuthenticated, IsOwnerProduct],
        'destroy': [IsAuthenticated, IsOwnerProduct],
    }


class CategoryViewSet(ProModelViewSet):
    queryset = Category.objects.all()
    lookup_field = 'id'
    filter_backends = filtering
    ordering_fields = ['name', 'created_at']
    search_fields = ['name']
    pagination_class = SimplePagination
    serializer_class = CategorySerializer,
    permission_classes_by_action = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'create': [IsAuthenticated, IsSuperuser],
        'update': [IsAuthenticated, IsSuperuser],
        'destroy': [IsAuthenticated, IsSuperuser],
    }


class TagViewSet(ProModelViewSet):
    queryset = Tag.objects.all()
    lookup_field = 'id'
    filter_backends = filtering
    ordering_fields = ['name', 'created_at']
    search_fields = ['name']
    pagination_class = SimplePagination
    serializer_class = TagSerializer
    permission_classes_by_action = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'create': [IsAuthenticated, IsSuperuser],
        'update': [IsAuthenticated, IsSuperuser],
        'destroy': [IsAuthenticated, IsSuperuser],
    }
