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
    CreateProductSerializer, DetailProductSerializer, UpdateProductSerializer
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
    permission_classes_by_method = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'create': [IsAuthenticated],
        'update': [IsAuthenticated, IsOwner],
        'destroy': [IsAuthenticated, IsOwner],

    }
    pagination_class = SimplePagination


class UploadProductImage(GenericAPIView):
    queryset = ProductImage.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = filtering
    search_fields = ['product']
    filterset_fields = ['product']
    ordering_fields = ['product']
    pagination_class = SimplePagination

    serializer_classes = {
        'GET': ProductImageSerializer,
        'POST': CreateProductImageSerializer,
    }

    def get(self, request, *args, **kwargs):
        image = self.filter_queryset(self.get_queryset())
        image = self.paginate_queryset(image)
        serializer = self.get_serializer(image, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        prod = serializer.save()
        response_serializer = DetailProductImageSerializer(prod, context={'request': request})

        return Response(response_serializer.data)

    def get_serializer_class(self):
        assert self.serializer_classes is not None, (
                "'%s' should either include a `serializer_classes` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        serializer_class = self.serializer_classes.get(self.request.method)

        assert serializer_class is not None, f'There is no serializer for "{self.request.method}" method.'

        return serializer_class


class DetailProductImage(GenericAPIView):
    queryset = ProductImage.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'
    serializer_classes = {
        'GET': DetailProductImageSerializer,
        'PUT': UploadProductImageSerializer,
        'PATCH': UploadProductImageSerializer,
        'DELETE': ...,
    }

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, partial=False)

    def patch(self, request, *args, **kwargs):
        return self.update(request, partial=True)

    def update(self, request, partial=False):
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request):
        product = self.get_object()
        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        assert self.serializer_classes is not None, (
                "'%s' should either include a `serializer_classes` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        serializer_class = self.serializer_classes.get(self.request.method)

        assert serializer_class is not None, f'There is no serializer for "{self.request.method}" method.'

        return serializer_class


class ListProductAttribute(GenericAPIView):
    queryset = ProductAttribute.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = filtering

    search_fields = ['name']
    filterset_fields = ['name']
    ordering_fields = ['name']

    pagination_class = SimplePagination

    serializer_classes = {
        'GET': ProductAttributeSerializer,
        'POST': CreateProductAttributeSerializer,
    }

    def get(self, request, *args, **kwargs):
        product = self.filter_queryset(self.get_queryset())
        product = self.paginate_queryset(product)
        serializer = self.get_serializer(product, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        assert self.serializer_classes is not None, (
                "'%s' should either include a `serializer_classes` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        serializer_class = self.serializer_classes.get(self.request.method)

        assert serializer_class is not None, f'There is no serializer for "{self.request.method}" method.'

        return serializer_class


class DetailProductAttribute(GenericAPIView):
    queryset = ProductAttribute.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'
    serializer_classes = {
        'GET': ListAttributeSerializer,
        'PUT': UpdateProductAttributeSerializer,
        'PATCH': UpdateProductAttributeSerializer,
    }

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request)

    def patch(self, request, *args, **kwargs):
        return self.update(request, partial=True)

    def update(self, request, partial=False):
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        assert self.serializer_classes is not None, (
                "'%s' should either include a `serializer_classes` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        serializer_class = self.serializer_classes.get(self.request.method)

        assert serializer_class is not None, f'There is no serializer for "{self.request.method}" method.'

        return serializer_class


class ListProductCategory(GenericAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = filtering
    pagination_class = SimplePagination

    serializer_classes = {
        'GET': CategorySerializer,
        'POST': CreateUpdateCategorySerializer,
    }

    def get(self, request, *args, **kwargs):
        product = self.filter_queryset(self.get_queryset())
        product = self.paginate_queryset(product)
        serializer = self.get_serializer(product, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def get_serializer_class(self):
        assert self.serializer_classes is not None, (
                "'%s' should either include a `serializer_classes` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        serializer_class = self.serializer_classes.get(self.request.method)

        assert serializer_class is not None, f'There is no serializer for "{self.request.method}" method.'

        return serializer_class


class DetailProductCategory(GenericAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'

    serializer_classes = {
        'GET': DetailCategorySerializer,
        'PUT': CreateUpdateCategorySerializer,
        'PATCH': CreateUpdateCategorySerializer,
    }

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request)

    def patch(self, request, *args, **kwargs):
        return self.update(request, partial=True)

    def update(self, request, partial=False):
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        assert self.serializer_classes is not None, (
                "'%s' should either include a `serializer_classes` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        serializer_class = self.serializer_classes.get(self.request.method)

        assert serializer_class is not None, f'There is no serializer for "{self.request.method}" method.'

        return serializer_class


class ListProductTag(GenericAPIView):
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = filtering
    pagination_class = SimplePagination

    serializer_classes = {
        'GET': TagSerializer,
        'POST': CreateUpdateTagSerializer,
    }

    def get(self, request, *args, **kwargs):
        product = self.filter_queryset(self.get_queryset())
        product = self.paginate_queryset(product)
        serializer = self.get_serializer(product, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def get_serializer_class(self):
        assert self.serializer_classes is not None, (
                "'%s' should either include a `serializer_classes` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        serializer_class = self.serializer_classes.get(self.request.method)

        assert serializer_class is not None, f'There is no serializer for "{self.request.method}" method.'

        return serializer_class


class DetailProductTag(GenericAPIView):
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'

    serializer_classes = {
        'GET': DetailTagSerializer,
        'PUT': CreateUpdateTagSerializer,
        'PATCH': CreateUpdateTagSerializer,
    }

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request)

    def patch(self, request, *args, **kwargs):
        return self.update(request, partial=True)

    def update(self, request, partial=False):
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        assert self.serializer_classes is not None, (
                "'%s' should either include a `serializer_classes` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        serializer_class = self.serializer_classes.get(self.request.method)

        assert serializer_class is not None, f'There is no serializer for "{self.request.method}" method.'

        return serializer_class
