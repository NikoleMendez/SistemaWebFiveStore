# Generated by Django 5.0.4 on 2024-12-05 02:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutorials', '0004_venta_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venta',
            name='cantidad',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='preciov',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='producto',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='total',
        ),
    ]
