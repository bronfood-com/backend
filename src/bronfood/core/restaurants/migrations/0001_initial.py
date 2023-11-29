# Generated by Django 4.2.7 on 2023-11-29 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Dishes",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Название блюда"),
                ),
                (
                    "description",
                    models.CharField(
                        max_length=255, null=True, verbose_name="Описание"
                    ),
                ),
                ("price", models.PositiveIntegerField(verbose_name="Цена")),
                (
                    "pic",
                    models.ImageField(
                        upload_to="pics", verbose_name="Изображение блюда"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Menu",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Активно ли"),
                ),
                (
                    "pic",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="pics",
                        verbose_name="Изображение меню",
                    ),
                ),
                (
                    "dishes",
                    models.ManyToManyField(
                        to="restaurants.dishes", verbose_name="Блюда"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="Название"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Restaurant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=255, verbose_name="Название ресторана"),
                ),
                ("adress", models.CharField(max_length=255, verbose_name="Адресс")),
                ("description", models.TextField(verbose_name="Описание")),
                (
                    "pic",
                    models.ImageField(
                        upload_to="pics", verbose_name="Изображение ресторана"
                    ),
                ),
                (
                    "from_work",
                    models.CharField(max_length=255, verbose_name="Начало работы"),
                ),
                (
                    "to_work",
                    models.CharField(max_length=255, verbose_name="Конец работы"),
                ),
                (
                    "type_of_restaurant",
                    models.CharField(
                        choices=[
                            ("FF", "Фаст Фуд"),
                            ("CF", "Кафе"),
                            ("CFN", "Кофейня"),
                        ],
                        max_length=10,
                        verbose_name="Тип ресторана",
                    ),
                ),
                (
                    "is_canceled",
                    models.BooleanField(
                        default=False, verbose_name="Можно ли отменить заказ"
                    ),
                ),
                (
                    "time_to_cancel",
                    models.TimeField(null=True, verbose_name="Время для отмены заказа"),
                ),
                ("rating", models.PositiveIntegerField(verbose_name="Рейтинг")),
                (
                    "menu",
                    models.ManyToManyField(to="restaurants.menu", verbose_name="Меню"),
                ),
                (
                    "tags",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="restaurants.tag",
                        verbose_name="Теги",
                    ),
                ),
            ],
        ),
    ]
