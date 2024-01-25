# Generated by Django 4.2.7 on 2024-01-23 20:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0003_alter_tempuseraccountdata_new_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccountTempData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp_data_code', models.CharField(max_length=6)),
                ('new_password', models.CharField(max_length=128, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='temp_data', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='TempUserAccountData',
        ),
    ]