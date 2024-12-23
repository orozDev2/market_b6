from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from store.models import Tag, Category, Product, ProductImage, ProductAttribute
from .serializers import CategorySerializer, TagSerializer, ListProductSerializer, DetailProductSerializer, \
    CreateProductSerializer, UpdateProductSerializer, UploadProductImageSerializer, CreateProductAttributeSerializer, \
    UpdateProductAttributeSerializer


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ListProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = CreateProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        read_serializer = DetailProductSerializer(product, context={'request': request})
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'PATCH'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'GET':
        serializer = DetailProductSerializer(product, context={'request': request})
        return Response(serializer.data)

    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = UpdateProductSerializer(product, data=request.data, context={'request': request}, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def upload_product_image(request):
    serializer = UploadProductImageSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status.HTTP_201_CREATED)


@api_view(['DELETE'])
def delete_product_image(request, pk):
    product_image = get_object_or_404(ProductImage, pk=pk)
    product_image.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def create_product_attribute(request):
    serializer = CreateProductAttributeSerializer()
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status.HTTP_201_CREATED)


@api_view(['DELETE', 'PUT', 'PATCH'])
def delete_update_product_attribute(request, pk):
    product_attribute = get_object_or_404(ProductAttribute, pk=pk)

    if request.method == 'DELETE':
        product_attribute.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = UpdateProductAttributeSerializer(product_attribute, data=request.data,
                                                      context={'request': request},
                                                      partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)


@api_view(['GET'])
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)


@api_view(['GET', ])
def tag_list(request):
    if request.method == 'GET':
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True, context={'request': request})
        return Response(serializer.data)


@api_view(['GET'])
def tag_detail(request, pk):
    tag = get_object_or_404(Tag, pk=pk)

    if request.method == 'GET':
        serializer = TagSerializer(tag)
        return Response(serializer.data)
