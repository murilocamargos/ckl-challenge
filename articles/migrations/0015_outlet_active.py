# Generated by Django 2.0 on 2017-12-28 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0014_auto_20171226_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='outlet',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
