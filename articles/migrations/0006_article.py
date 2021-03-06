# Generated by Django 2.0 on 2017-12-22 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('date', models.DateTimeField()),
                ('url', models.CharField(max_length=255, unique=True)),
                ('thumb', models.CharField(default='', max_length=255)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.Author')),
                ('categories', models.ManyToManyField(to='articles.Category')),
                ('outlet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.Outlet')),
            ],
        ),
    ]
