# Generated by Django 4.2.4 on 2023-09-28 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_category_options_product_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name_plural': 'المنتجات'},
        ),
    ]
