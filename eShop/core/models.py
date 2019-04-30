from django.db import models
from django.urls import reverse


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