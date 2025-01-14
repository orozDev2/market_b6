from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework.backends import DjangoFilterBackend
from django.core.paginator import Paginator

from store.models import Tag, Category, Product, ProductImage, ProductAttribute
from .filters import ProductFilter
from .mixins import SerializerByMethodMixin, PermissionByMethodMixin, ProGenericAPIView
from .paginations import SimplePagination
from .permissions import IsOwnerOrReadOnly, IsOwner
from .serializers import CategorySerializer, TagSerializer, ListProductSerializer, DetailProductSerializer, \
    CreateProductSerializer, UpdateProductSerializer, UploadProductImageSerializer, CreateProductAttributeSerializer, \
    UpdateProductAttributeSerializer, CreateProductImageSerializer, DetailProductImageSerializer, \
    ProductAttributeSerializer, ListAttributeSerializer, CreateUpdateCategorySerializer, DetailCategorySerializer, \
    CreateUpdateTagSerializer, DetailTagSerializer, ProductImageSerializer


filtering = [
    SearchFilter, DjangoFilterBackend, OrderingFilter
]

class ListCreateProductApiView(ProGenericAPIView):
    queryset = Product.objects.all()
    permission_classes_by_method = {
        'GET': [AllowAny],
        'POST': [IsAuthenticated],
        'OPTIONS': [AllowAny],
    }
    filter_backends = filtering
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'content']
    ordering_fields = ['price', 'name', 'created_at', 'rating']
    serializer_classes = {
        'GET': ListProductSerializer,
        'POST': CreateProductSerializer,
    }
    pagination_class = SimplePagination

    def get(self, request, *args, **kwargs):
        products = self.filter_queryset(self.get_queryset())
        products = self.paginate_queryset(products)
        serializer = self.get_serializer(products, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        read_serializer = DetailProductSerializer(product, context={'request': request})
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)


      
class DetailUpdateDeleteProductApiView(ProGenericAPIView):

    queryset = Product.objects.all()
    lookup_field = 'id'
    permission_classes_by_method = {
        'GET': [AllowAny],
        'PATCH': [IsAuthenticated, IsOwner],
        'PUT': [IsAuthenticated, IsOwner],
        'DELETE': [IsAuthenticated, IsOwner],
        'OPTIONS': [AllowAny],
    }
    serializer_classes = {
        'GET': DetailProductSerializer,
        'PATCH': UpdateProductSerializer,
        'PUT': UpdateProductSerializer,
    }

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request)

    def patch(self, request, *args, **kwargs):
        return self.update(request, True)

    def update(self, request, partial=False):
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UploadProductImage(ProGenericAPIView):
    queryset = ProductImage.objects.all()
    permission_classes_by_method = {
        'GET': [AllowAny],
        'POST': [IsAuthenticated],
        'OPTIONS': [AllowAny],
    }
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
        response_serializer = DetailProductImageSerializer(prod, context={'request':request})

        return Response(response_serializer.data)


class DetailProductImage(GenericAPIView):
    queryset = ProductImage.objects.all()
    permission_classes_by_method = {
        'GET': [AllowAny],
        'PATCH': [IsAuthenticated, IsOwner],
        'PUT': [IsAuthenticated, IsOwner],
        'DELETE': [IsAuthenticated, IsOwner],
        'OPTIONS': [AllowAny],
    }
    lookup_field = 'id'
    serializer_classes = {
        'GET': DetailProductImageSerializer,
        'PUT': UploadProductImageSerializer,
        'PATCH': UploadProductImageSerializer,
    }

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, partial=False)

    def patch(self, request, *args, **kwargs):
        return self.update(request, partial=True)

    def update(self, request, partial = False):
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data, partial = partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request):
        product = self.get_object()
        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ListProductAttribute(GenericAPIView):
    queryset = ProductAttribute.objects.all()
    permission_classes_by_method = {
        'GET': [AllowAny],
        'POST': [IsAuthenticated],
        'OPTIONS': [AllowAny],
    }

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
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DetailProductAttribute(GenericAPIView):
    queryset = ProductAttribute.objects.all()
    permission_classes_by_method = {
        'GET': [AllowAny],
        'PATCH': [IsAuthenticated, IsOwner],
        'PUT': [IsAuthenticated, IsOwner],
        'DELETE': [IsAuthenticated, IsOwner],
        'OPTIONS': [AllowAny],
    }
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
        serializer = self.get_serializer(product, data = request.data, partial=partial)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ListProductCategory(GenericAPIView):
    queryset = Category.objects.all()
    permission_classes_by_method = {
        'GET': [AllowAny],
        'POST': [IsAuthenticated],
        'OPTIONS': [AllowAny],
    }

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
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data)


class DetailProductCategory(GenericAPIView):
    queryset = Category.objects.all()
    permission_classes_by_method = {
        'GET': [AllowAny],
        'PATCH': [IsAuthenticated, IsOwner],
        'PUT': [IsAuthenticated, IsOwner],
        'DELETE': [IsAuthenticated, IsOwner],
        'OPTIONS': [AllowAny],
    }
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
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


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
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data)

class DetailProductTag(GenericAPIView):
    queryset = Tag.objects.all()
    permission_classes_by_method = {
        'GET': [AllowAny],
        'PATCH': [IsAuthenticated, IsOwner],
        'PUT': [IsAuthenticated, IsOwner],
        'DELETE': [IsAuthenticated, IsOwner],
        'OPTIONS': [AllowAny],
    }
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
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)