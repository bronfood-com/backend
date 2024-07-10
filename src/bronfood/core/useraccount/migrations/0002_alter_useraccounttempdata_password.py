from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccounttempdata',
            name='password',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
