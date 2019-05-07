from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from model_utils.models import TimeStampedModel




def save_image_path(instance, filename):
    filename = instance.slug + '.jpg'
    return f'{instance.category}/{instance.brand}/{filename}'


class Category(models.Model):
    name = models.CharField(max_length = 55, unique = True)
    slug = models.SlugField(max_length = 55, unique = True)

    def get_absolute_url(self):
        return reverse('product:category-detail', kwargs = {'category_slug':self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'



class Brand(models.Model):
    name = models.CharField(max_length = 55, unique = True)
    slug = models.SlugField(max_length = 55, unique = True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'





class ProductManager(models.Manager):
    def all(self, *args, **kwargs):
        return super(ProductManager, self).get_queryset().filter(available=True)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete = models.CASCADE, related_name = 'brands')
    title = models.CharField(max_length = 255, unique = True)
    slug = models.SlugField(max_length = 255, unique = True)
    description = models.TextField()
    image = models.ImageField(upload_to = save_image_path, blank = True, default = 'default.png')
    price = models.DecimalField(decimal_places=2, max_digits=9)
    available = models.BooleanField(default = True)

    objects = ProductManager()

    def get_absolute_url(self):
        return reverse('product:product-detail', kwargs = {'category_slug':self.category.slug, 'product_slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-id']


class Like(TimeStampedModel):
    product = models.ForeignKey(Product, related_name='likes', on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='likes', on_delete = models.CASCADE)
    ip = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        unique_together = (('product', 'user'), ('product', 'ip'))
        ordering = ['-id']

    def __str__(self):
        return '{} from {}'.format(self.product, self.user or self.ip)



class Comment(TimeStampedModel):
    product = models.ForeignKey(Product, related_name='comments', on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='comments', on_delete = models.CASCADE)
    ip = models.GenericIPAddressField(blank=True, null=True)
    text = models.TextField(_('Comment'), max_length = 500)

    def __str__(self):
        return 'Comment from {}'.format(self.user or self.ip)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-id']