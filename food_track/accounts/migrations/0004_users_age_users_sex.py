# Generated by Django 4.0.4 on 2022-05-04 00:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0003_remove_users_age_remove_users_sex'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='age',
            field=models.PositiveSmallIntegerField(default=2, null=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='users',
            name='sex',
            field=models.CharField(default='M', max_length=1),
            preserve_default=False,
        ),
    ]
