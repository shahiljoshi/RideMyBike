# Generated by Django 3.2.4 on 2021-06-22 16:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bikes', '0002_bike'),
    ]

    operations = [
        migrations.CreateModel(
            name='rental',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(default=None, null=True)),
                ('cost', models.IntegerField(null=True)),
                ('bike', models.ManyToManyField(to='bikes.bike')),
                ('end_station', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='end_station', to='bikes.station')),
                ('start_station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='start_station', to='bikes.station')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
