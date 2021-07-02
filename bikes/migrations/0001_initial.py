# Generated by Django 3.2.4 on 2021-06-22 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('capacity', models.IntegerField()),
                ('working', models.BooleanField(default=True)),
            ],
        ),
    ]