from pprint import pprint

from django.contrib.auth.models import User
from rest_framework import serializers
import uuid

from store.models import Tag, Category, Product, ProductImage, ProductAttribute
from utils.main import base64_to_image_file


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        )


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ("created_at", "updated_at", "product")


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        exclude = ("created_at", "updated_at", "product")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields = '__all__'
        exclude = ("created_at", "updated_at")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        # fields = '__all__'
        exclude = ("created_at", "updated_at")


class ListProductSerializer(serializers.ModelSerializer):
    # category = serializers.CharField(source='category.name')
    # tags = serializers.ListSerializer(child=serializers.CharField(source='tags.name'))

    category = CategorySerializer()
    # tags = serializers.ListSerializer(child=TagSerializer())
    tags = TagSerializer(many=True)
    user = UserSerializer()
    image = serializers.ImageField()
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        exclude = (
            "created_at",
            "updated_at",
            "content",
        )


class DetailProductSerializer(serializers.ModelSerializer):
    # category = serializers.CharField(source='category.name')
    # tags = serializers.ListSerializer(child=serializers.CharField(source='tags.name'))

    category = CategorySerializer()
    # tags = serializers.ListSerializer(child=TagSerializer())
    tags = TagSerializer(many=True)
    user = UserSerializer()
    image = serializers.ImageField()
    images = ProductImageSerializer(many=True)
    attributes = ProductAttributeSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"


class UpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "name",
            "description",
            "content",
            "category",
            "tags",
            "price",
            "receive_type",
            "rating",
            "is_published",
        )

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Цена не может быть отрицательной")
        return value


class CreateProductSerializer(serializers.ModelSerializer):

    attributes = ProductAttributeSerializer(many=True)
    images = serializers.ListSerializer(child=serializers.CharField())

    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        images = validated_data.pop("images")
        attributes = validated_data.pop("attributes")
        tags = validated_data.pop("tags")

        file_images = []

        for image in images:
            try:
                file = base64_to_image_file(image, uuid.uuid4())
                file_images.append(file)
            except Exception as e:
                print(e)
                raise serializers.ValidationError(
                    {"images": ["Загрузите корректное изображение"]}
                )

        product = super().create(validated_data)
        product.tags.add(*tags)

        for attribute in attributes:
            ProductAttribute.objects.create(**attribute, product=product)

        for file_image in file_images:
            product_image = ProductImage.objects.create(product=product)
            product_image.image.save(file_image.name, file_image)
            product_image.save()

        return product


class UploadProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = "__all__"


class CreateProductAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductAttribute
        fields = "__all__"


class UpdateProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ("name", "value")
