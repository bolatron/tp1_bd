# Generated by Django 3.1.5 on 2021-04-13 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0002_auto_20210413_0812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='imagem',
            field=models.ImageField(upload_to='web_app/static/media/'),
        ),
    ]
