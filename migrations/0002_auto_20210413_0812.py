# Generated by Django 3.1.5 on 2021-04-13 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='usuario',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='fornecedor',
            name='usuario',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='produto',
            name='tipo',
            field=models.CharField(choices=[('CASA', 'Casa/Lar'), ('ELET', 'Eletrônicos'), ('INFA', 'Produtos Infantis'), ('ROUP', 'Roupas')], default=None, max_length=4),
        ),
    ]