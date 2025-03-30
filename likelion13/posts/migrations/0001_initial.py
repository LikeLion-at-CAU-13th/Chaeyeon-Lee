# Generated by Django 5.1.7 on 2025-03-30 10:02

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
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=30)),
                ('content', models.TextField()),
                ('status', models.CharField(choices=[('STORED', '보관'), ('PUBLISHED', '발행')], default='STORED', max_length=15)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('user', models.CharField(default='anonymous', max_length=30)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='posts.post')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.category')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
            ],
        ),
    ]
