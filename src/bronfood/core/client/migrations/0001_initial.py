# Generated by Django 4.2.7 on 2023-12-17 08:02

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('useraccount', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('useraccount.useraccount',),
        ),
    ]
