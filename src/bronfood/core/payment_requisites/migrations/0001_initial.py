# Generated by Django 4.2.7 on 2023-12-26 12:11

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentRequisites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cardholder_name', models.CharField(max_length=255)),
                ('expiration_data', models.CharField()),
                ('cvv', models.IntegerField(validators=[django.core.validators.MinValueValidator(100), django.core.validators.MaxValueValidator(999)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client')),
            ],
        ),
    ]
