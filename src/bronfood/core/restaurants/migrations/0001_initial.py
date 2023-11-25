# Generated by Django 4.2.7 on 2023-11-25 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
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
                ("is_active", models.BooleanField(default=True)),
                ("is_archived", models.BooleanField(default=False)),
                (
                    "title",
                    models.CharField(max_length=255, verbose_name="Название блюда"),
                ),
                ("price", models.PositiveIntegerField(verbose_name="Цена")),
                ("description", models.TextField(verbose_name="Описание")),
                (
                    "pic",
                    models.ImageField(
                        upload_to="pics", verbose_name="Изображение блюда"
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
                ("name", models.CharField(max_length=255)),
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
                (
                    "menu",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="restaurants.menu",
                        verbose_name="Меню",
                    ),
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