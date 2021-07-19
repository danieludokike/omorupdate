# Generated by Django 3.0 on 2021-07-18 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('omorapp', '0004_auto_20210717_2342'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='views',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='author',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='head_line',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='time',
            field=models.TimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='write_up',
            field=models.TextField(max_length=5000, null=True),
        ),
        migrations.DeleteModel(
            name='View',
        ),
    ]