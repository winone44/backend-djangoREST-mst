# Generated by Django 4.0.4 on 2022-05-23 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='name',
            new_name='title',
        ),
    ]
