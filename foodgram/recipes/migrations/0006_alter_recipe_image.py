# Generated by Django 3.2.3 on 2021-06-18 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_alter_recipeingredient_ingredient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(help_text='Загрузите изображение', upload_to='recipes/', verbose_name='Изображение'),
        ),
    ]
