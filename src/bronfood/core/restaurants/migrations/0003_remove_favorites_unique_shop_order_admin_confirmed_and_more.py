from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0002_rename_favorite_favorites_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='favorites',
            name='unique_shop',
        ),
        migrations.AddField(
            model_name='order',
            name='admin_confirmed',
            field=models.BooleanField(default=False, verbose_name='Подтверждение админом'),
        ),
        migrations.AddConstraint(
            model_name='favorites',
            constraint=models.UniqueConstraint(fields=('user', 'restaurant'), name='unique_restaurant'),
        ),
    ]
