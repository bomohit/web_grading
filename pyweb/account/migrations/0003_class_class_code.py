# Generated by Django 2.2.24 on 2021-06-09 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='class_code',
            field=models.CharField(default=0, max_length=6),
            preserve_default=False,
        ),
    ]
