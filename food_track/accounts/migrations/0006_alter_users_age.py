# Generated by Django 4.0.4 on 2022-05-05 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_users_age_users_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='age',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
