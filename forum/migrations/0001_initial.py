# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-21 17:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mainapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('created_on', models.DateTimeField()),
                ('dp', models.ImageField(null=True, upload_to='forum_dps')),
                ('description', models.CharField(max_length=200, null=True)),
                ('detail', models.TextField(null=True)),
                ('last_thread_on', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('created_on', models.DateTimeField()),
                ('dp', models.ImageField(null=True, upload_to='forum_dps')),
                ('description', models.CharField(max_length=200, null=True)),
                ('detail', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('url', models.CharField(max_length=40, unique=True)),
                ('punchline', models.CharField(default='', max_length=100)),
                ('created_on', models.DateTimeField()),
                ('thumb', models.ImageField(upload_to='')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forums', to='mainapp.RootProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('post_time', models.DateTimeField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('content', models.FileField(upload_to='forum_post_files')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Post')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_on', models.DateTimeField()),
                ('screen_name', models.CharField(blank=True, max_length=30, null=True)),
                ('dp', models.ImageField(upload_to='user_dp')),
                ('quote', models.CharField(blank=True, max_length=300, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('karma', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_point', models.SmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Post')),
                ('rater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_on', models.DateTimeField()),
                ('title', models.CharField(max_length=170)),
                ('thread_type', models.CharField(choices=[('NM', 'Normal'), ('PN', 'Pinned'), ('AM', 'Announcement')], default='NM', max_length=2)),
                ('views', models.IntegerField(default=0)),
                ('last_post_on', models.DateTimeField()),
                ('post_count', models.IntegerField(default=1)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Board')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_threads', to=settings.AUTH_USER_MODEL)),
                ('last_post_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Thread'),
        ),
        migrations.AddField(
            model_name='category',
            name='forum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Forum'),
        ),
        migrations.AddField(
            model_name='board',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Category'),
        ),
    ]
