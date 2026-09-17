from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from avito_app.models import Category, SubCategory, Product, ProductImage, Reviews

User = get_user_model()


class Command(BaseCommand):
    help = 'Заполняет базу тестовыми данными'

    def handle(self, *args, **options):

        # --- Пользователи ---
        users_data = [
            ('john_doe', 25, '+996700100001', 'gold'),
            ('aida_k', 30, '+996700100002', 'silver'),
            ('bekzat_m', 28, '+996700100003', 'bronze'),
            ('elena_v', 34, '+996700100004', 'simple'),
            ('nurlan_t', 22, '+996700100005', 'gold'),
            ('dmitry_s', 41, '+996700100006', 'simple'),
            ('anara_b', 27, '+996700100007', 'silver'),
            ('maksat_o', 33, '+996700100008', 'bronze'),
            ('kate_p', 24, '+996700100009', 'gold'),
            ('ruslan_z', 29, '+996700100010', 'simple'),
            ('zhanna_a', 31, '+996700100011', 'silver'),
            ('ivan_k', 26, '+996700100012', 'bronze'),
        ]
        users = []
        for username, age, phone, status in users_data:
            user, _ = User.objects.get_or_create(
                username=username,
                defaults=dict(
                    age=age,
                    phone_number=phone,
                    avatar='profile_images/default.jpg',
                    status=status,
                ),
            )
            users.append(user)

        # --- Категории ---
        categories_data = [
            'Electronics', 'Home Appliances', 'Furniture', 'Clothing',
            'Footwear', 'Sports', 'Books', 'Toys',
            'Beauty', 'Automotive', 'Garden', 'Pets',
        ]
        categories = []
        for name in categories_data:
            slug = name.lower().replace(' ', '_')
            category, _ = Category.objects.get_or_create(
                category_name=name,
                defaults=dict(category_image=f'category_images/{slug}.jpg'),
            )
            categories.append(category)

        # --- Подкатегории ---
        subcategories_data = [
            'Smartphones', 'Laptops', 'Refrigerators', 'Sofas',
            'T-Shirts', 'Sneakers', 'Fitness Gear', 'Fiction',
            'Board Games', 'Skincare', 'Car Accessories', 'Dog Supplies',
        ]
        subcategories = []
        for i, name in enumerate(subcategories_data):
            slug = name.lower().replace(' ', '_')
            subcategory, _ = SubCategory.objects.get_or_create(
                category=categories[i % len(categories)],
                sub_category_name=name,
                defaults=dict(sub_category_image=f'sub_category_image/{slug}.jpg'),
            )
            subcategories.append(subcategory)

        # --- Товары ---
        products_data = [
            ('iPhone 15 Pro', 899.99, 'Latest Apple smartphone with A17 chip.'),
            ('Samsung Galaxy S24', 749.99, 'Flagship Samsung smartphone with AI features.'),
            ('MacBook Air M3', 1199.00, 'Lightweight laptop with the M3 chip.'),
            ('Dell XPS 13', 999.00, 'Compact ultrabook with a bright display.'),
            ('Samsung Fridge RB37', 650.00, 'No-frost refrigerator with large capacity.'),
            ('IKEA Kivik Sofa', 540.00, 'Comfortable three-seat sofa.'),
            ('Basic Cotton T-Shirt', 15.00, 'Soft cotton t-shirt, various colors.'),
            ('Nike Air Max', 129.99, 'Classic running sneakers.'),
            ('Yoga Mat Pro', 25.00, 'Non-slip yoga mat, 6mm thick.'),
            ('The Great Novel', 12.50, 'Bestselling fiction novel.'),
            ('Strategy Board Game', 34.90, 'Board game for 2-4 players.'),
            ('Face Moisturizer', 18.75, 'Daily face moisturizer for all skin types.'),
        ]
        products = []
        for i, (name, price, description) in enumerate(products_data):
            product, _ = Product.objects.get_or_create(
                article_number=1000001 + i,
                defaults=dict(
                    SubCategory=subcategories[i % len(subcategories)],
                    product_name=name,
                    price=price,
                    description=description,
                    product_type=True,
                ),
            )
            products.append(product)

        # --- Изображения товаров ---
        for i, product in enumerate(products, start=1):
            ProductImage.objects.get_or_create(
                product=product,
                product_image=f'product_images/product_{i}.jpg',
            )

        # --- Отзывы ---
        comments = [
            ('Отличный товар, всё понравилось!', 5),
            ('Хороший, но могло быть лучше.', 4),
            ('Соответствует описанию.', 4),
            ('Не совсем то, что ожидал.', 3),
            ('Быстрая доставка, качество на высоте.', 5),
            ('Пользуюсь уже месяц, всё отлично.', 5),
            ('Средне, есть аналоги подешевле.', 3),
            ('Рекомендую всем!', 5),
            ('Неплохо за свою цену.', 4),
            ('Разочарован качеством сборки.', 2),
            ('Прекрасное соотношение цена/качество.', 5),
            ('Буду брать ещё.', 5),
        ]
        for i, product in enumerate(products):
            comment, stars = comments[i % len(comments)]
            Reviews.objects.get_or_create(
                user=users[i % len(users)],
                product=product,
                defaults=dict(start=stars, comment=comment),
            )

        self.stdout.write(self.style.SUCCESS('Данные успешно добавлены.'))