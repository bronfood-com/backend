import bronfood.core.restaurants.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('name', models.CharField(max_length=200, verbose_name='Название варианта')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('default', models.BooleanField(default=False, verbose_name='По умолчанию')),
                ('chosen', models.BooleanField(default=False, verbose_name='Выбран пользователем')),
            ],
            options={
                'verbose_name': 'Вариант выбора',
                'verbose_name_plural': 'Варианты выбора',
            },
        ),
        migrations.CreateModel(
            name='Coordinates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=8, verbose_name='Широта')),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='Долгота')),
            ],
            options={
                'verbose_name': 'Координаты',
                'verbose_name_plural': 'Координаты',
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('name', models.CharField(max_length=200, verbose_name='Название дополнения')),
                ('choices', models.ManyToManyField(to='restaurants.choice', verbose_name='Варианты выбора')),
            ],
            options={
                'verbose_name': 'Дополнение',
                'verbose_name_plural': 'Дополнения',
            },
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('name', models.CharField(max_length=255, verbose_name='Название блюда')),
                ('description', models.TextField(verbose_name='Описание блюда')),
                ('photo', models.URLField(verbose_name='URL фотографии')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('type', models.CharField(choices=[('food', 'Еда'), ('drink', 'Напиток'), ('dessert', 'Десерт')], max_length=7, verbose_name='Тип блюда')),
                ('waitingTime', models.PositiveIntegerField(verbose_name='Время ожидания')),
                ('features', models.ManyToManyField(blank=True, to='restaurants.feature', verbose_name='Дополнения')),
            ],
            options={
                'verbose_name': 'Блюдо',
                'verbose_name_plural': 'Блюда',
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('photo', models.URLField(verbose_name='URL фотографии')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('isLiked', models.BooleanField(default=False, verbose_name='Понравился ли ресторан')),
                ('rating', models.DecimalField(decimal_places=1, max_digits=4, verbose_name='Рейтинг')),
                ('workingTime', models.CharField(max_length=255, verbose_name='Время работы')),
                ('type', models.CharField(choices=[('fastFood', 'Фастфуд'), ('cafe', 'Кафе'), ('cafeBar', 'Кафе-бар')], max_length=8, verbose_name='Тип ресторана')),
                ('coordinates', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='restaurants.coordinates', verbose_name='Координаты')),
                ('meals', models.ManyToManyField(to='restaurants.meal', verbose_name='Блюда')),
            ],
            options={
                'verbose_name': 'Ресторан',
                'verbose_name_plural': 'Рестораны',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='OrderedMeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество блюд')),
                ('orderedMeal', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='restaurants.meal', verbose_name='Заказанное блюдо')),
            ],
            options={
                'verbose_name': 'Блюдо в заказе',
                'verbose_name_plural': 'Блюда в заказе',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('userId', models.CharField(max_length=255, verbose_name='Идентификатор клиента')),
                ('id', models.CharField(default=bronfood.core.restaurants.utils.create_order, max_length=255, primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('totalAmount', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Общая сумма заказа')),
                ('preparationStatus', models.CharField(choices=[('waiting', 'Ожидание'), ('confirmed', 'Подтверждено'), ('notConfirmed', 'Не подтверждено')], default='waiting', max_length=13, verbose_name='Статус подготовки заказа')),
                ('preparationTime', models.IntegerField(verbose_name='Время приготовления заказа')),
                ('paymentStatus', models.CharField(choices=[('paid', 'Оплачено'), ('notPaid', 'Не оплачено')], default='notPaid', max_length=7, verbose_name='Статус оплаты')),
                ('cancellationTime', models.DateTimeField(blank=True, null=True, verbose_name='Время отмены заказа')),
                ('cancellationStatus', models.CharField(choices=[('none', 'Нет'), ('requested', 'Запрошено'), ('confirmed', 'Подтверждено')], default='none', max_length=9, verbose_name='Статус отмены заказа')),
                ('isCancellationRequested', models.BooleanField(default=False, verbose_name='Запрос на отмену заказа')),
                ('admin_confirmed', models.BooleanField(default=False, verbose_name='Подтверждение админом')),
                ('orderedMeal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='restaurants.orderedmeal')),
                ('restaurantId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.restaurant', verbose_name='Ресторан')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=255, verbose_name='Категория меню')),
                ('meals', models.ManyToManyField(to='restaurants.meal', verbose_name='Блюда')),
            ],
            options={
                'verbose_name': 'Меню',
                'verbose_name_plural': 'Меню',
            },
        ),
        migrations.CreateModel(
            name='MealInBasket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.BigIntegerField(default=0, verbose_name='Количество блюд')),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.meal')),
            ],
            options={
                'verbose_name': 'Блюдо в корзине',
                'verbose_name_plural': 'Блюда в корзине',
            },
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='restaurants.restaurant', verbose_name='Ресторан')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='client.client', verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Избранное заведение',
                'verbose_name_plural': 'Избранные заведения',
            },
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meals', models.ManyToManyField(related_name='baskets', to='restaurants.mealinbasket', verbose_name='Блюда в корзине')),
                ('restaurant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurants.restaurant', verbose_name='Ресторан')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
            },
        ),
        migrations.CreateModel(
            name='UserLikedRestaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_liked', models.BooleanField(default=False, verbose_name='Понравился ли ресторан')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.restaurant', verbose_name='Ресторан')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client', verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Пользовательский ресторан',
                'verbose_name_plural': 'Пользовательские рестораны',
                'unique_together': {('user', 'restaurant')},
            },
        ),
        migrations.AddConstraint(
            model_name='favorites',
            constraint=models.UniqueConstraint(fields=('user', 'restaurant'), name='unique_restaurant'),
        ),
    ]
