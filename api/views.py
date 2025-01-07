from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from django.core.paginator import Paginator

from store.models import Tag, Category, Product, ProductImage, ProductAttribute
from .serializers import CategorySerializer, TagSerializer, ListProductSerializer, DetailProductSerializer, \
    CreateProductSerializer, UpdateProductSerializer, UploadProductImageSerializer, CreateProductAttributeSerializer, \
    UpdateProductAttributeSerializer


class ListCreateProductApiView(GenericAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_classes = {
        'GET': ListProductSerializer,
        'POST': CreateProductSerializer,
    }

    def get(self, request, *args, **kwargs):
        products = self.get_queryset()

        search = request.GET.get('search')

        if search:
            products = products.filter(
                Q(name__icontains=search) | Q(description__icontains=search) | Q(content__icontains=search))

        ordering_fields = ['name', 'price', 'created_at', 'rating', 'receive_type']
        ordering = request.GET.get('ordering')  # -name ['', 'name']
        if ordering:
            ordering = ordering.split('-')[:2] if len(ordering.split('-')) > 1 else ordering.split('-')
            if ordering[0 if len(ordering) == 1 else 1] in ordering_fields:
                products = products.order_by(ordering[0] if len(ordering) == 1 else '-' + ordering[1])

        page, page_size = request.GET.get('page', 1), request.GET.get('page_size', 1)
        products_count = products.count()

        pagin = Paginator(products, page_size)
        products = pagin.get_page(page)

        serializer = self.get_serializer(products, many=True)

        return Response({
            'count': products_count,
            'page_size': page_size,
            'page': page,
            'pages_count': pagin.num_pages,
            'results': serializer.data
        })

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        read_serializer = DetailProductSerializer(product, context={'request': request})
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        assert self.serializer_classes is not None, (
                "'%s' should either include a `serializer_classes` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        serializer_class = self.serializer_classes.get(self.request.method)

        assert serializer_class is not None, f'There is no serializer for "{self.request.method}" method.'

        return serializer_class


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
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

    if request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_product_image(request):
    serializer = UploadProductImageSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status.HTTP_201_CREATED)


@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def delete_product_image(request, pk):
    product_image = get_object_or_404(ProductImage, pk=pk)
    product_image.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_product_attribute(request):
    serializer = CreateProductAttributeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status.HTTP_201_CREATED)


@permission_classes([IsAuthenticated])
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


@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = CategorySerializer(category, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    if request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def tag_list(request):
    if request.method == 'GET':
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = TagSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def tag_detail(request, pk):
    tag = get_object_or_404(Tag, pk=pk)

    if request.method == 'GET':
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = TagSerializer(tag, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    if request.method == 'DELETE':
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
