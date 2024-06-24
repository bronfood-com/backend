from django.db import models
from django.db.models import UniqueConstraint

from bronfood.core.client.models import Client
from bronfood.core.restaurants.utils import create_order


class Coordinates(models.Model):
    '''Координаты заведения для Yandex Maps.'''
    latitude = models.DecimalField(
        'Широта',
        max_digits=8,
        decimal_places=6
    )
    longitude = models.DecimalField(
        'Долгота',
        max_digits=9,
        decimal_places=6
    )

    class Meta:
        verbose_name = 'Координаты'
        verbose_name_plural = 'Координаты'

    def __str__(self):
        return f"{self.latitude}, {self.longitude}"


class Tag(models.Model):
    '''Класс тегов к заведениям.'''
    name = models.CharField(
        'Название',
        max_length=255,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Choice(models.Model):
    '''Вариант выбора для дополнения.'''
    id = models.AutoField(
        'Идентификатор',
        primary_key=True
    )
    name = models.CharField(
        'Название варианта',
        max_length=200
    )
    price = models.DecimalField(
        'Цена',
        max_digits=10,
        decimal_places=2
    )
    default = models.BooleanField(
        'По умолчанию',
        default=False
    )
    chosen = models.BooleanField(
        'Выбран пользователем',
        default=False
    )

    class Meta:
        verbose_name = 'Вариант выбора'
        verbose_name_plural = 'Варианты выбора'

    def __str__(self):
        return self.name


class Feature(models.Model):
    '''Дополнение к блюду.'''
    id = models.AutoField(
        'Идентификатор',
        primary_key=True
    )
    name = models.CharField(
        'Название дополнения',
        max_length=200
    )
    choices = models.ManyToManyField(
        'Choice',
        verbose_name='Варианты выбора'
    )

    class Meta:
        verbose_name = 'Дополнение'
        verbose_name_plural = 'Дополнения'

    def __str__(self):
        return self.name


class Meal(models.Model):
    '''Блюдо.'''
    MEAL_TYPES = [
        ('food', 'Еда'),
        ('drink', 'Напиток'),
        ('dessert', 'Десерт'),
    ]
    id = models.AutoField(
        'Идентификатор',
        primary_key=True
    )
    name = models.CharField(
        'Название блюда',
        max_length=255
    )
    description = models.TextField(
        'Описание блюда',
    )
    photo = models.URLField(
        'URL фотографии'
    )
    price = models.DecimalField(
        'Цена',
        max_digits=10,
        decimal_places=2
    )
    type = models.CharField(
        'Тип блюда',
        max_length=7,
        choices=MEAL_TYPES
    )
    waitingTime = models.PositiveIntegerField(
        'Время ожидания'
    )
    features = models.ManyToManyField(
        Feature,
        verbose_name='Дополнения',
        blank=True
    )

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return self.name


class Menu(models.Model):
    '''Модель меню.'''
    meals = models.ManyToManyField(
        Meal,
        verbose_name='Блюда'
    )
    category = models.CharField(
        'Категория меню',
        max_length=255
    )

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'


class Restaurant(models.Model):
    '''Модель ресторана.'''
    RESTAURANT_TYPES = [
        ('fastFood', 'Фастфуд'),
        ('cafe', 'Кафе'),
        ('cafeBar', 'Кафе-бар'),
    ]
    id = models.AutoField(
        'Идентификатор',
        primary_key=True
    )
    name = models.CharField(
        'Название',
        max_length=255
    )
    photo = models.URLField(
        'URL фотографии'
    )
    address = models.CharField(
        max_length=255,
        verbose_name='Адрес'
    )
    coordinates = models.OneToOneField(
        Coordinates,
        on_delete=models.CASCADE,
        verbose_name='Координаты'
    )
    rating = models.DecimalField(
        'Рейтинг',
        max_digits=4,
        decimal_places=1
    )
    workingTime = models.CharField(
        'Время работы',
        max_length=255
    )
    meals = models.ManyToManyField(
        Meal,
        verbose_name='Блюда'
    )
    type = models.CharField(
        'Тип ресторана',
        max_length=8,
        choices=RESTAURANT_TYPES
    )

    class Meta:
        verbose_name = 'Ресторан'
        verbose_name_plural = 'Рестораны'

    def __str__(self):
        return self.name


class UserLikedRestaurant(models.Model):
    '''
    Модель для отслеживания отношения между пользователем и рестораном.
    Содержит поле `is_liked`, которое указывает, понравился ли ресторан пользователю.
    '''
    user = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name='Клиент'
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        verbose_name='Ресторан'
    )
    is_liked = models.BooleanField(
        'Понравился ли ресторан',
        default=False
    )

    class Meta:
        unique_together = ('user', 'restaurant')
        verbose_name = 'Пользовательский ресторан'
        verbose_name_plural = 'Пользовательские рестораны'


class Favorites(models.Model):
    '''Избранные рестораны'''
    user = models.ForeignKey(
        Client,
        related_name='favorites',
        on_delete=models.CASCADE,
        verbose_name='Клиент'
    )
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='favorites',
        on_delete=models.CASCADE,
        verbose_name='Ресторан'
    )

    class Meta:
        verbose_name = 'Избранное заведение'
        verbose_name_plural = 'Избранные заведения'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'restaurant'],
                name="unique_restaurant"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.restaurant}"


class MealInBasket(models.Model):
    '''Блюдо в корзине.'''
    meal = models.ForeignKey(
        Meal,
        on_delete=models.CASCADE
    )
    count = models.BigIntegerField(
        'Количество блюд',
        default=0
    )

    class Meta:
        verbose_name = 'Блюдо в корзине'
        verbose_name_plural = 'Блюда в корзине'

    def __str__(self):
        return f"{self.meal} - {self.count}"


class Basket(models.Model):
    '''Корзина.'''
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Ресторан'
    )
    meals = models.ManyToManyField(
        MealInBasket,
        related_name='baskets',
        verbose_name='Блюда в корзине'
    )

    def add_meal(self, meal_in_basket):
        self.meals.add(meal_in_basket)

    def remove_meal(self, meal_in_basket):
        self.meals.remove(meal_in_basket)

    def clear(self):
        self.meals.clear()

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f"Корзина {self.id} ресторана {self.restaurant}"


class OrderedMeal(models.Model):
    '''Блюда в заказе.'''
    orderedMeal = models.ForeignKey(
        Meal,
        on_delete=models.CASCADE,
        default=None,
        verbose_name='Заказанное блюдо'
    )
    quantity = models.PositiveIntegerField(
        'Количество блюд'
    )

    class Meta:
        verbose_name = 'Блюдо в заказе'
        verbose_name_plural = 'Блюда в заказе'

    def __str__(self):
        return self.orderedMeal.name


class Order(models.Model):
    '''Заказ'''
    CANCELLATION_STATUS_CHOICES = [
        ('none', 'Нет'),
        ('requested', 'Запрошено'),
        ('confirmed', 'Подтверждено'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('paid', 'Оплачено'),
        ('notPaid', 'Не оплачено'),
    ]
    PREPARATION_STATUS_CHOICES = [
        ('waiting', 'Ожидание'),
        ('confirmed', 'Подтверждено'),
        ('notConfirmed', 'Не подтверждено'),
    ]
    userId = models.CharField(
        'Идентификатор клиента',
        max_length=255
    )
    id = models.CharField(
        'Идентификатор',
        primary_key=True,
        max_length=255,
        default=create_order
    )
    totalAmount = models.DecimalField(
        'Общая сумма заказа',
        max_digits=5,
        decimal_places=2
    )
    preparationStatus = models.CharField(
        'Статус подготовки заказа',
        max_length=13,
        choices=PREPARATION_STATUS_CHOICES,
        default='waiting'
    )
    preparationTime = models.IntegerField(
        'Время приготовления заказа'
    )
    paymentStatus = models.CharField(
        'Статус оплаты',
        max_length=7,
        choices=PAYMENT_STATUS_CHOICES,
        default='notPaid'
    )
    cancellationTime = models.DateTimeField(
        'Время отмены заказа',
        null=True,
        blank=True
    )
    cancellationStatus = models.CharField(
        'Статус отмены заказа',
        max_length=9,
        choices=CANCELLATION_STATUS_CHOICES,
        default='none'
    )
    isCancellationRequested = models.BooleanField(
        'Запрос на отмену заказа',
        default=False
    )
    orderedMeal = models.ForeignKey(
        OrderedMeal,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    restaurantId = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        verbose_name='Ресторан'
    )
    admin_confirmed = models.BooleanField(
        'Подтверждение админом',
        default=False
    )

    def confirm_order(self):
        self.admin_confirmed = True
        self.save()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Заказ {self.id} клиента {self.userId}"
