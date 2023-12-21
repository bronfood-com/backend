from django.db import models


class Complement(models.Model):
    '''Дополнение к основному блюду.'''
    name = models.CharField(
        'Дополнение',
        max_length=200
    )
    price = models.PositiveIntegerField('Цена')

    class Meta:
        verbose_name = 'Дополнение'
        verbose_name_plural = 'Дополнения'

    def __str__(self):
        return self.name


class Dish(models.Model):
    """Блюдо."""
    name = models.CharField('Название блюда', max_length=255)
    description = models.CharField('Описание', max_length=255, null=True)
    price = models.PositiveIntegerField('Цена')
    image = models.ImageField('Изображение блюда', upload_to='pics')
    size = models.CharField('Размер блюда', max_length=255)
    wait = models.PositiveIntegerField('Время ожидания')
    tags = models.CharField('Теги', max_length=50)
    complement = models.ForeignKey(
        Complement,
        verbose_name='Дополнения',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Menu(models.Model):
    """Модель меню."""
    image = models.ImageField(
        'Изображение меню',
        upload_to='pics',
        null=True,
        blank=True
    )
    dishes = models.ManyToManyField(Dish, verbose_name='Блюда')


class Restaurant(models.Model):
    """Модель ресторана."""
    class TypeOfShop(models.TextChoices):
        FASTFOOD = "FF",
        CAFE = "CA"
        COFFESHOP = "CS"
    name = models.CharField('Название', max_length=255)
    address = models.CharField('Адрес', max_length=255)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение ресторана', upload_to='pics')
    begin_time = models.CharField('Начало работы', max_length=255)
    end_time = models.CharField('Конец работы', max_length=255)
    menu = models.ForeignKey(
        Menu,
        verbose_name='Меню',
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey('RestaurantOwner')
    admin = models.ForeignKey('RestaurantAdmin')
    type_of_shop = models.CharField(
        max_length=2,
        choices=TypeOfShop.choices,
        default=TypeOfShop.FF,
    )

    def __str__(self):
        return self.name
