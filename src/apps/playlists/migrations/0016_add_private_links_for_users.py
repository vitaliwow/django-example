# Generated by Django 4.2.14 on 2024-08-19 15:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('playlists', '0015_add_commercial_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateLinksForUsers',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('public_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                (
                    'private_link',
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playlists.privatelink'),
                ),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'private_links_for_users',
                'unique_together': {('user', 'private_link')},
            },
        ),
    ]