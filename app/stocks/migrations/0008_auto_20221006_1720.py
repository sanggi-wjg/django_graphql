# Generated by Django 3.1.5 on 2022-10-06 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0007_auto_20221006_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(choices=[('COSMETIC', 'Cosmetic'), ('FOOD', 'Food'), ('BOOK', 'Book')], max_length=250, null=True),
        ),
    ]
