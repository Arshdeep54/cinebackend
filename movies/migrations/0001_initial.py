# Generated by Django 5.0 on 2023-12-29 09:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('trailer_link', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('storyline', models.TextField()),
                ('poster_link', models.TextField()),
                ('duration', models.CharField(max_length=255)),
                ('language', models.CharField(default='Hindi', max_length=255)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('platform', models.CharField(default='Theaters', max_length=255)),
                ('platform_link', models.CharField(default='', max_length=255)),
                ('genre', models.CharField(default='comedy', max_length=255)),
                ('release_date', models.DateField()),
                ('director', models.CharField(max_length=255)),
                ('writers', models.TextField()),
                ('starcast', models.TextField()),
                ('production', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='FavouriteMovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='isfavourite', to='movies.movie')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oneliner', models.TextField()),
                ('description', models.TextField()),
                ('made_at', models.DateTimeField(auto_now_add=True)),
                ('likes', models.PositiveIntegerField(default=0)),
                ('dislikes', models.PositiveIntegerField(default=0)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='movies.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReviewFromWeb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_id', models.CharField(max_length=255)),
                ('user', models.CharField(max_length=255)),
                ('oneliner', models.TextField()),
                ('description', models.TextField()),
                ('made_at', models.DateField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='webreviews', to='movies.movie')),
            ],
        ),
    ]
