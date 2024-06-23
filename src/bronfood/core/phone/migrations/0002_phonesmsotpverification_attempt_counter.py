from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phone', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='phonesmsotpverification',
            name='attempt_counter',
            field=models.IntegerField(default=0, verbose_name='Attempt counter'),
        ),
    ]
