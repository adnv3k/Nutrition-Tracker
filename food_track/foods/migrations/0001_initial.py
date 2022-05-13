# Generated by Django 4.0.4 on 2022-05-13 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('nutrients', models.TextField()),
                ('dataType', models.CharField(default='SR Legacy', max_length=15)),
            ],
            options={
                'verbose_name_plural': 'foods',
            },
        ),
        migrations.CreateModel(
            name='FoodHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('food', models.CharField(max_length=255)),
                ('nutrients', models.TextField()),
                ('food_id', models.IntegerField()),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Nutrients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nutrients', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'nutrients',
            },
        ),
    ]
