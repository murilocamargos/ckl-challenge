# Generated by Django 2.0 on 2017-12-22 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_auto_20171222_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='about',
            field=models.TextField(default=''),
        ),
    ]
