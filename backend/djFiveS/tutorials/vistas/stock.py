from tutorials.models import Producto, Categoria, Almacen, Compra
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.db.models import F, Sum

# Margen
def margen_create (request):
    return render(request, 'margenprecios_fm.html')

# Principal
#@permiso_requerido('Permiso Venta')
def modulo_stock (request):
    return render(request, 'stock.html')


# Listar Producto
def producto(request):
    # Ordenar los productos por id en orden descendente
    productos = Producto.objects.all().order_by('-id')
    context = {
        'title': 'Lista de Productos',
        'producto': productos
    }
    return render(request, 'Productos_lista.html', context)



#Crear Producto
def producto_create(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        categoria_id = request.POST.get('categoria')
        descripcion = request.POST.get('descripcion')

        # Crear el producto en la base de datos
        producto = Producto.objects.create(
            cod=codigo,
            nombre=nombre,
            categoria_id=categoria_id,
            descripcion=descripcion
        )

        # Redirigir a la lista de productos
        return redirect('producto')  # redirigir al nombre de la URL definida en urls.py

    # Si no es una solicitud POST, mostrar el formulario para crear un nuevo producto
    categorias = Categoria.objects.all()  # Obtener todas las categorías
    return render(request, 'Productos_fm.html', {
        'categorias': categorias  # Pasar las categorías al contexto
    })

# Detalles Producto
def producto_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'Productos_detail.html', {'producto': producto})



# Actualiza Producto
def producto_update(request, pk):
    # Obtén la instancia del Producto que deseas actualizar
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':  # Maneja solicitudes POST para actualizar el producto
        data = request.POST  # Obtiene los datos de la solicitud POST
        
        # Actualiza los campos del Producto con los datos proporcionados
        producto.cod = data.get('codigo', producto.cod)  # Asegúrate de usar el nombre correcto del campo
        producto.nombre = data.get('nombre', producto.nombre)
        producto.descripcion = data.get('descripcion', producto.descripcion)
        
        # Maneja la actualización de la categoría
        categoria_id = data.get('categoria')
        if categoria_id:
            try:
                categoria = Categoria.objects.get(id=categoria_id)
                producto.categoria = categoria
            except Categoria.DoesNotExist:
                producto.categoria = None
        
        producto.save()  # Guarda los cambios en la base de datos

        # Redirige a la página de detalles del producto (o a donde desees)
        return redirect('producto')
        
        # Devuelve una respuesta JSON con los datos actualizados del Producto
        return JsonResponse({
            'id': producto.id,
            'cod': producto.cod,
            'nombre': producto.nombre,
            'descripcion': producto.descripcion,
        })
    
    # Maneja solicitudes GET para mostrar la página de actualización del producto
    elif request.method == 'GET':
        categorias = Categoria.objects.all()  # Obtén todas las categorías
        return render(request, 'Productos_fm.html', {
            'producto': producto,
            'categorias': categorias  # Pasa las categorías al contexto
        })
    
    # Si la solicitud no es ni POST ni GET, devuelve un error 405 (Método no permitido)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

#Elimina Producto
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('producto')
    
    context = {'object': producto}
    return render(request, 'productos_delete.html', context)

#Almacen lista
def almacen_lista(request):
    almacen = Almacen.objects.all()  # Obtiene todos los registros de Almacen
    compras = Compra.objects.all()  # Obtén todos los datos de compra

    context = {
        'title': 'Lista de Almacenes',
        'almacen': almacen,
        'compras': compras  # Incluye los datos de compra en el contexto
    }
    return render(request, 'almacenes_lista.html', context)



#Actualiza Almacen
def almacen_update(request, pk):
    # Obtén la instancia del Producto que deseas actualizar
    almacen = get_object_or_404(Almacen, pk=pk)
    
    if request.method == 'POST':  # Maneja solicitudes POST para actualizar el producto
        data = request.POST  # Obtiene los datos de la solicitud POST
        
        # Actualiza los campos del Producto con los datos proporcionados
        almacen.fecha = data.get('fecha', almacen.fecha)
        almacen.producto = data.get('producto', almacen.producto)
        almacen.categoria = data.get('categoria', almacen.categoria)
        almacen.cantidad = data.get('cantidad', almacen.cantidad)
        almacen.precioc = data.get('precioc', almacen.precioc)
        almacen.preciov = data.get('preciov', almacen.preciov)
        almacen.save()  # Guarda los cambios en la base de datos

        # Redirige
        return redirect('almacen_lista')
        
        # Devuelve una respuesta JSON con los datos actualizados del Producto
        return JsonResponse({
            'id': almacen.id,
            'fecha': almacen.fecha,
            'producto': almacen.producto,
            'categoria': almacen.categoria,
            'cantidad': almacen.cantidad,
            'precioc': almacen.precioc,
            'preciov': almacen.preciov,
        })
    
    # Maneja solicitudes GET para mostrar la página de actualización del producto
    elif request.method == 'GET':
        return render(request, 'almacenes_fm.html', {'almacen': almacen})
    
    # Si la solicitud no es ni POST ni GET, devuelve un error 405 (Método no permitido)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

#Elimina Almacen
def almacen_delete(request, pk):
    almacen = get_object_or_404(Almacen, pk=pk)
    if request.method == 'POST':
        almacen.delete()
        return redirect('almacen_lista')
    
    context = {'object': almacen}
    return render(request, 'almacenes_delete.html', context)


#Lista Categoria
def categoria_lista(request):
    # Ordenar las categorías por id en orden descendente
    categoria = Categoria.objects.all().order_by('-id')
    context = {
        'title': 'Lista de Categorías',
        'categoria': categoria
    }
    return render(request, 'categorias_lista.html', context)

# Crear Categoria
def categoria_create(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')

        categoria = Categoria.objects.create(
            nombre=nombre,
        )

        return redirect('categoria_lista')  

    return render(request, 'categorias_fm.html')  


# Detalles Producto
def categoria_detail(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    return render(request, 'categorias_detail.html', {'categoria': categoria})

#Actualiza Producto
def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST': 
        data = request.POST  
     
        categoria.nombre = data.get('nombre', categoria.nombre)
        categoria.save()  

        return redirect('categoria_lista')
        
        return JsonResponse({
            'nombre': categoria.nombre,
        })
    
    elif request.method == 'GET':
        return render(request, 'Categorias_fm.html', {'categoria': categoria})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

#Elimina Categoria
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categoria_lista')
    
    context = {'object': categoria}
    return render(request, 'categoria_delete.html', context)
