# Generated by Django 2.2.24 on 2021-06-14 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_submission_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='grade',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
    ]
