# Generated by Django 3.2.4 on 2021-07-02 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bikes', '0007_auto_20210702_0855'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='station',
            name='capacity',
        ),
        migrations.AlterField(
            model_name='rental',
            name='bike',
            field=models.ManyToManyField(related_name='bike', to='bikes.Bike'),
        ),
    ]
