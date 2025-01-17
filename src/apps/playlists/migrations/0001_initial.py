# Generated by Django 4.2.9 on 2024-01-23 14:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('videos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                    'name',
                    models.CharField(
                        choices=[
                            ('movies', 'Кино'),
                            ('music', 'Музыка'),
                            ('sports', 'Спорт'),
                            ('hobbies', 'Хобби'),
                            ('flowers', 'Цветы'),
                            ('children', 'Дети'),
                            ('home', 'Дом'),
                            ('humor', 'Юмор'),
                            ('useful', 'Полезное'),
                            ('psychology', 'Психология'),
                            ('education', 'Образование'),
                            ('languages', 'Языки'),
                            ('work', 'Работа'),
                            ('travel', 'Путешествия'),
                        ],
                        default='education',
                    ),
                ),
                ('image', models.ImageField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('public_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True)),
                ('background_image', models.ImageField(upload_to='playlists/')),
                (
                    'privacy_type',
                    models.CharField(
                        choices=[('private', 'Private'), ('public', 'Public'), ('link', 'Link')], default='public'
                    ),
                ),
                ('status', models.CharField(choices=[('active', 'Active'), ('banned', 'Banned')], default='active')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='playlists.category')),
                (
                    'owner',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='owned_playlists',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'ordering': ['created'],
                'default_related_name': 'playlists',
            },
        ),
        migrations.CreateModel(
            name='PlaylistsUsersRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_liked', models.BooleanField(default=False)),
                ('is_viewed', models.BooleanField(default=False)),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playlists.playlist')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'playlist')},
            },
        ),
        migrations.AddField(
            model_name='playlist',
            name='users',
            field=models.ManyToManyField(through='playlists.PlaylistsUsersRelation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='playlist',
            name='videos',
            field=models.ManyToManyField(to='videos.video'),
        ),
    ]