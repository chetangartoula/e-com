# Generated by Django 4.1.1 on 2022-10-25 13:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0004_alter_product_pro_desc_alter_product_main_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='sub_category',
            name='slug',
            field=models.SlugField(blank=True, default=uuid.uuid1, null=True),
        ),
    ]
