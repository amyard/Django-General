import os, django, random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eShop.settings')
django.setup()

from core.models import Product, Brand, Category
from django.utils.text import slugify
from transliterate import translit
from django.core.files.images import ImageFile
from faker import Faker



def gen_slug(s):
    try:
        new_slug = slugify(translit(s, reversed=True, allow_unicode = True))
    except:
        new_slug = slugify(s, allow_unicode = True)
    return new_slug


def create_category_brand(data, model):
    for i in data:
        model.objects.create(
            name = i,
            slug = gen_slug(i)
        )


def create_product(N, categories, brands):
    fake = Faker()
    for i in range(N):
        numb_for_cat = random.randint(0, 3)
        numb_for_brand = random.randint(0, 5)
        pic = random.randint(1, 5)
        product = Product.objects.create(
            category = Category.objects.get(name = categories[numb_for_cat]),
            brand = Brand.objects.get(name = brands[numb_for_brand]),
            title=f'Product № {i}',
            slug=gen_slug(f'Product № {i}'),
            price=random.randint(100, 9999999),
            description = fake.text()
        )
        product.image = ImageFile(open(f'{os.getcwd()}/populate_data/{categories[numb_for_cat]}/{pic}.jpg', 'rb'))
        product.save()


def main():
    categories = ['Смартфоны', 'Ноутбуки', 'Комплектующие', 'Планшеты']
    brands = ['Apple', 'Dell', 'Samsung', 'Xiaomi', 'LG', 'Asus']
    create_category_brand(categories, Category)
    create_category_brand(brands, Brand)
    create_product(30, categories, brands)

if __name__ == '__main__':
    main()

    print('Finish All.')