# Generated by Django 3.2.5 on 2022-07-04 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oj', '0004_auto_20220703_0006'),
    ]

    operations = [
        migrations.AddField(
            model_name='solutions',
            name='submitted_code',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='problems',
            name='statement',
            field=models.CharField(max_length=255),
        ),
    ]
