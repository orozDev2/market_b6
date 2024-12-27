from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_resized import ResizedImageField
User = get_user_model()


class TimeStampAbstractModel(models.Model):
    created_at = models.DateTimeField('дата добавление', auto_now_add=True)
    updated_at = models.DateTimeField('дата изменения', auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    name = models.CharField('название', max_length=250, unique=True)

    def __str__(self):
        return f'{self.name}'


class Tag(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    name = models.CharField('название', max_length=255)

    def __str__(self):
        return f'{self.name}'


def example_validation(value):
    if float(value) == 3.3:
        raise ValidationError('Example error')

    return value


class Product(TimeStampAbstractModel):
    ORDER = 'order'
    IN_STOCK = 'in_stock'
    PICK_UP = 'pick_up'

    RECEIVE_TYPE = (
        (ORDER, 'На заказ'),
        (IN_STOCK, 'В наличии'),
        (PICK_UP, 'Самовывоз')
    )

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ('-created_at',)

    name = models.CharField('название', max_length=100)
    description = models.CharField('описание', max_length=255, help_text='Просто описание')
    content = models.TextField('контент')
    category = models.ForeignKey('store.Category', models.PROTECT, verbose_name='категория',
                                 help_text='Выберите категорию')
    tags = models.ManyToManyField('store.Tag', verbose_name='теги')
    price = models.DecimalField('цена', max_digits=10, decimal_places=2, default=0.0)
    user = models.ForeignKey(User, models.CASCADE, verbose_name='пользователь')
    receive_type = models.CharField('условия получение', choices=RECEIVE_TYPE, default=ORDER, max_length=15)
    rating = models.DecimalField('рейтинг', max_digits=2, decimal_places=1,
                                         validators=[MinValueValidator(1), MaxValueValidator(5), example_validation])
    is_published = models.BooleanField('публичность', default=True)

    @property
    def image(self):
        if self.images.first():
            return self.images.first().image
        return None

    def __str__(self):
        return f'{self.name}'


class ProductImage(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'изображение товара'
        verbose_name_plural = 'изображении товаров'
        ordering = ('-created_at',)

    product = models.ForeignKey('store.Product', models.CASCADE, related_name='images', verbose_name='товар')
    image = ResizedImageField('изображение', upload_to='product_images/', quality=90, force_format='WEBP')

    def __str__(self):
        return f'{self.product.name}'


class ProductAttribute(TimeStampAbstractModel):
    class Meta:
        verbose_name = 'атрибут товара'
        verbose_name_plural = 'атрибуты товаров'
        ordering = ('-created_at',)

    name = models.CharField('название', max_length=50)
    value = models.CharField('значение', max_length=50)
    product = models.ForeignKey('store.Product', models.CASCADE, related_name='attributes', verbose_name='товар')

    def __str__(self):
        return f'{self.name} - {self.value}'
