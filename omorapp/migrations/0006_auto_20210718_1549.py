# Generated by Django 3.0 on 2021-07-18 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('omorapp', '0005_auto_20210718_1130'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-id']},
        ),
    ]