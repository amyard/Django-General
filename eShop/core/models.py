from django.db import models



def save_image_path(instance, filename):
    filename = instance.slug + '.jpg'
    return f'{instance.category}/{instance.brand}/{filename}'


class Category(models.Model):
    name = models.CharField(max_length = 55, unique = True)
    slug = models.SlugField(max_length = 55, unique = True)

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



class Product(models.Model):
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete = models.CASCADE)
    title = models.CharField(max_length = 255, unique = True)
    slug = models.SlugField(max_length = 255, unique = True)
    description = models.TextField()
    image = models.ImageField(upload_to = save_image_path, blank = True, default = 'default.png')
    price = models.DecimalField(decimal_places=2, max_digits=9)
    available = models.BooleanField(default = True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'