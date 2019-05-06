import os, django, random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eShop.settings')
django.setup()

from product.models import Product, Brand, Category, Comment, Like
from django.utils.text import slugify
from transliterate import translit
from django.core.files.images import ImageFile
from django.contrib.auth import get_user_model
from faker import Faker



User = get_user_model()


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
            title=f'{brands[numb_for_brand]} - {categories[numb_for_cat]} Product № {i}',
            slug=gen_slug(f'Product № {i}'),
            price=random.randint(100, 9999999),
            description = fake.text()
        )
        product.image = ImageFile(open(f'{os.getcwd()}/populate_data/{categories[numb_for_cat]}/{pic}.jpg', 'rb'))
        product.save()


def create_users(data):
    for i in data:
        User.objects.create(
            username = i,
            email = f'{i.lower()}@gmail.com',
            password = f'{i.lower()}'
        )


def create_comments(N):
    fake = Faker()
    for _ in range(N):
        Comment.objects.create(
            product = Product.objects.order_by("?").first(),
            ip = f'192.198.12.1{_}',
            text = fake.text()
        )

def create_likes(N):
    for _ in range(N):
        product = Product.objects.order_by("?").first()
        user = User.objects.order_by("?").first()
        ip = f'192.198.12.1{_}'
        likes = Like.objects.filter(product=product).values_list('user__id', flat=True)

        like_obj = Like.objects.create(product = product)

        if user.id not in likes:
            like_obj.user = user
        else:
            like_obj.ip = ip
        like_obj.save()





def main():
    categories = ['Смартфоны', 'Ноутбуки', 'Комплектующие', 'Планшеты']
    brands = ['Apple', 'Dell', 'Samsung', 'Xiaomi', 'LG', 'Asus']
    users = ['TestUser', 'NewUser', 'delme', 'ItsMe', 'Awesome']

    create_category_brand(categories, Category)
    create_category_brand(brands, Brand)
    create_product(30, categories, brands)

    create_users(users)
    create_comments(15)
    create_likes(50)





if __name__ == '__main__':
    main()

    print('Finish All.')