# Generated by Django 4.2.7 on 2024-02-19 19:59

import bronfood.core.useraccount.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('role', models.CharField(choices=[('ADMIN', 'admin'), ('CLIENT', 'client'), ('OWNER', 'owner'), ('RESTAURANT_ADMIN', 'restaurant_admin')], default='CLIENT', max_length=16)),
                ('username', models.CharField(max_length=40)),
                ('fullname', models.CharField(max_length=40, validators=[bronfood.core.useraccount.validators.FullnameValidator])),
                ('phone', models.CharField(max_length=18, unique=True, validators=[bronfood.core.useraccount.validators.KazakhstanPhoneNumberValidator])),
                ('status', models.SmallIntegerField(choices=[(0, 'Unconfirmed'), (1, 'Confirmed'), (2, 'Blocked')], default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserAccountTempData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp_data_code', models.CharField(max_length=6)),
                ('password', models.CharField(max_length=128, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('fullname', models.CharField(max_length=40, null=True, validators=[bronfood.core.useraccount.validators.FullnameValidator])),
                ('phone', models.CharField(max_length=18, null=True, validators=[bronfood.core.useraccount.validators.KazakhstanPhoneNumberValidator])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_account_temp_data', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
