from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    TYPE = [
        ('FF', 'Фаст Фуд'),
        ('CF', 'Кафе'),
        ('CFN', 'Кофейня'),
    ]

    title = models.CharField('Название ресторана', max_length=255)
    adress = models.CharField('Адресс', max_length=255)
    description = models.TextField('Описание')
    pic = models.ImageField('Изображение ресторана', upload_to='pics')
    from_work = models.CharField('Начало работы', max_length=255)
    to_work = models.CharField('Конец работы', max_length=255)
    type_of_restaurant = models.CharField('Тип ресторана', choices=TYPE, max_length=10)
    tags = models.ForeignKey(
        Tag, on_delete=models.SET_NULL, null=True, verbose_name='Теги'
    )
    is_canceled = models.BooleanField(
        default=False, verbose_name='Можно ли отменить заказ'
    )
    time_to_cancel = models.TimeField('Время для отмены заказа', null=True)
    menu = models.ForeignKey(
        'Menu', on_delete=models.SET_NULL, null=True, verbose_name='Меню'
    )

    def __str__(self):
        return self.title


class Menu(models.Model):
    is_active = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)
    title = models.CharField('Название блюда', max_length=255)
    price = models.PositiveIntegerField('Цена', null=False)  # models.FloatField('Цена')
    description = models.TextField('Описание')
    pic = models.ImageField('Изображение блюда', upload_to='pics')

    def __str__(self):
        return self.title
