# Generated by Django 3.1.7 on 2021-04-29 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0004_auto_20210429_0622'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordersummary',
            name='quant',
            field=models.TextField(default='0'),
        ),
        migrations.AlterField(
            model_name='ordersummary',
            name='ono',
            field=models.IntegerField(default=355417, unique=True),
        ),
    ]
