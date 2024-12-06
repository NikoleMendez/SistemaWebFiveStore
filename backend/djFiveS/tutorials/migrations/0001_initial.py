# Generated by Django 5.0.4 on 2024-10-25 01:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=25, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=25, null=True)),
                ('telefono', models.IntegerField(blank=True, null=True)),
                ('direccion', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=25, null=True)),
                ('telefono', models.IntegerField(blank=True, null=True)),
                ('direccion', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=25, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod', models.CharField(blank=True, max_length=25, null=True)),
                ('nombre', models.CharField(blank=True, max_length=25, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=200, null=True)),
                ('categoria', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tutorials.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Cotizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(blank=True, null=True)),
                ('cotizacion', models.CharField(blank=True, max_length=25, null=True)),
                ('cantidad', models.IntegerField(blank=True, null=True)),
                ('preciov', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total', models.IntegerField(blank=True, null=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorials.cliente')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorials.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Almacen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(blank=True, null=True)),
                ('cantidad', models.IntegerField(blank=True, default=1, null=True)),
                ('precioc', models.IntegerField(blank=True, null=True)),
                ('preciov', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('estado', models.BooleanField(default=True)),
                ('categoria', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tutorials.categoria')),
                ('producto', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tutorials.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(blank=True, null=True)),
                ('cantidad', models.IntegerField(blank=True, null=True)),
                ('precioc', models.IntegerField(blank=True, null=True)),
                ('preciov', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total', models.IntegerField(blank=True, null=True)),
                ('producto', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tutorials.producto')),
                ('proveedor', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tutorials.proveedor')),
            ],
        ),
        migrations.CreateModel(
            name='Permiso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=25, null=True)),
                ('modulo_administracion', models.BooleanField(default=False)),
                ('modulo_compra', models.BooleanField(default=False)),
                ('modulo_venta', models.BooleanField(default=False)),
                ('modulo_stock', models.BooleanField(default=False)),
                ('modulo_informe', models.BooleanField(default=False)),
                ('rol', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tutorials.rol')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='default_name', max_length=25, null=True)),
                ('ubicacion', models.CharField(blank=True, max_length=200, null=True)),
                ('producto', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tutorials.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=150, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('rol', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tutorials.rol')),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(blank=True, null=True)),
                ('glosa', models.CharField(blank=True, max_length=25, null=True)),
                ('cantidad', models.IntegerField(blank=True, null=True)),
                ('preciov', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total', models.IntegerField(blank=True, null=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorials.cliente')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorials.producto')),
            ],
        ),
    ]
