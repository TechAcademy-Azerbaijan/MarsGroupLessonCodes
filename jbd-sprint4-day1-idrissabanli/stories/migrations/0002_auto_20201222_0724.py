# Generated by Django 2.2.8 on 2020-12-22 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(editable=False, max_length=110, unique=True, verbose_name='Slug'),
        ),
    ]
