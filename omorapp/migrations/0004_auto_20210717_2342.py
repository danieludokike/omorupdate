# Generated by Django 3.0 on 2021-07-17 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('omorapp', '0003_postview'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PostView',
            new_name='View',
        ),
    ]