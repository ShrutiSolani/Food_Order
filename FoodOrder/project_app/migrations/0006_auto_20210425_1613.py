# Generated by Django 3.1.7 on 2021-04-25 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0005_auto_20210425_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordersummary',
            name='ono',
            field=models.IntegerField(default=560693, unique=True),
        ),
    ]