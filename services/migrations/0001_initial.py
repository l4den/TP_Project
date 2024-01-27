# Generated by Django 4.2.9 on 2024-01-26 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shops', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(default='', max_length=100)),
                ('price', models.PositiveIntegerField(default=0)),
                ('time_to_complete', models.TimeField()),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.shop')),
            ],
            options={
                'unique_together': {('shop', 'service')},
            },
        ),
    ]