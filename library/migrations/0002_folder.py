# Generated by Django 5.0.1 on 2024-01-31 02:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('name', models.CharField(help_text='The name of the folder', max_length=64, primary_key=True, serialize=False)),
                ('id', models.CharField(help_text='The drive id of the folder', max_length=64)),
                ('parent', models.ForeignKey(blank=True, help_text='The parent folder of this folder', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='library.folder')),
            ],
        ),
    ]