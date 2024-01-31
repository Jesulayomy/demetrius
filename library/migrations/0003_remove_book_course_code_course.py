# Generated by Django 5.0.1 on 2024-01-31 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_folder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='course',
        ),
        migrations.AddField(
            model_name='code',
            name='course',
            field=models.CharField(blank=True, help_text='The course this book is required for (i.e. Power Systems)', max_length=128, null=True),
        ),
    ]