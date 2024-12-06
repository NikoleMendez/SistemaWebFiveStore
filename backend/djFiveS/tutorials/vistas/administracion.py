from tutorials.decorators import permiso_requerido
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm, PermisoForm
from tutorials.models import Usuario
from tutorials.models import Rol, Permiso
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse


#@permiso_requerido('modulo_administracion')
def modulo_administracion (request):
    return render(request, 'administracion.html')

def permiso_lista(request):
    # Ordenar los permisos por el campo id en orden descendente
    permisos = Permiso.objects.all().order_by('-id')
    context = {
        'title': 'Lista de Permisos',
        'permisos': permisos
    }
    return render(request, 'permiso_lista.html', context)


# Crear Permisos
def permiso_create(request, pk=None):
    if pk:  # Si hay un pk, se trata de una actualización
        permiso = get_object_or_404(Permiso, pk=pk)
        form = PermisoForm(instance=permiso)
    else:  # Creación de nuevo permiso
        form = PermisoForm()

    if request.method == 'POST':
        form = PermisoForm(request.POST, instance=permiso if pk else None)
        if form.is_valid():
            nuevo_permiso = form.save(commit=False)  # No guardar aún en la base de datos

            # Asignar el rol seleccionado al permiso
            rol_id = request.POST.get('rol')  # Obtener el ID del rol seleccionado
            if rol_id:
                rol = Rol.objects.get(id=rol_id)
                nuevo_permiso.rol = rol

            nuevo_permiso.save()  # Ahora sí, guardar el permiso en la base de datos

            return redirect('permiso_lista')

    roles = Rol.objects.all()  # Obtener todos los roles para el formulario

    context = {
        'form': form,
        'roles': roles,
    }
    return render(request, 'permiso_fm.html', context)




def mostrar_modulos(request):
    # Obtener el usuario desde la sesión personalizada
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        # Redirigir al login si no está autenticado
        return redirect('login')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        # Manejar el caso en que el usuario no exista
        return redirect('login')
    
    rol = usuario.rol  # Obtener el rol del usuario
    if rol:
        permisos = Permiso.objects.filter(rol=rol)  # Obtener los permisos asociados al rol

        # Controlar los módulos basados en permisos
        modulos = {
            'modulo_administracion': any(permiso.modulo_administracion for permiso in permisos),
            'modulo_compra': any(permiso.modulo_compra for permiso in permisos),
            'modulo_venta': any(permiso.modulo_venta for permiso in permisos),
            'modulo_stock': any(permiso.modulo_stock for permiso in permisos),
            'modulo_informe': any(permiso.modulo_informe for permiso in permisos),
        }
    else:
        # Si el usuario no tiene rol, establecer todos los módulos en False
        modulos = {
            'modulo_administracion': False,
            'modulo_compra': False,
            'modulo_venta': False,
            'modulo_stock': False,
            'modulo_informe': False,
        }

    context = {'modulos': modulos}
    return render(request, 'modulos.html', context)




#Permiso Update
def permiso_update(request, pk):
    permiso = get_object_or_404(Permiso, pk=pk)
    if request.method == 'POST':
        form = PermisoForm(request.POST, instance=permiso)
        if form.is_valid():
            form.save()
            return redirect('permiso_lista')
    else:
        form = PermisoForm(instance=permiso)
    return render(request, 'permiso_fm.html', {'form': form})

#Eliminar permiso
def permiso_delete(request, pk):
    permiso = get_object_or_404(Permiso, pk=pk)
    if request.method == 'POST':
        permiso.delete()
        return redirect('permiso_lista')  # Redirect to the existing permiso_lista view
    
    context = {'object': permiso}
    return render(request, 'permiso_delete.html', context)

#Vista protegida
def vista_protegida(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        return redirect('login')

    rol = usuario.rol
    if rol:
        permisos = Permiso.objects.filter(rol=rol)
        context = {
            'puede_ver_administracion': any(p.modulo_administracion for p in permisos),
            'puede_ver_compra': any(p.modulo_compra for p in permisos),
            'puede_ver_venta': any(p.modulo_venta for p in permisos),
            'puede_ver_stock': any(p.modulo_stock for p in permisos),
            'puede_ver_informe': any(p.modulo_informe for p in permisos),
        }
        return render(request, 'vista_protegida.html', context)
    else:
        return render(request, 'acceso_denegado.html')




#Lista rol
def rol_lista(request):
    # Ordenar los roles por el campo id en orden descendente
    rol = Rol.objects.all().order_by('-id')
    context = {
        'title': 'Lista de Roles',
        'rol': rol
    }
    return render(request, 'rol_lista.html', context)


#rol create
def rol_create(request):
    permisos = Permiso.objects.all()

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')

        # Crear el nuevo rol
        rol = Rol.objects.create(nombre=nombre, descripcion=descripcion)
        return redirect('rol_lista')

    return render(request, 'rol_fm.html', {'permisos': permisos})


#Eliminar rol
def rol_delete(request, pk):
  rol = get_object_or_404(Rol, pk=pk)
  if request.method == 'POST':
    rol.delete()  # Call delete() on the retrieved object
    return redirect('rol_lista')  # Redirect to 'usuarios' URL after deletion
  
  context = {'object': rol}
  return render(request, 'rol_delete.html', context)

#Actualiza
def rol_update(request, pk):
    rol = get_object_or_404(Rol, pk=pk)
    
    if request.method == 'POST':  
        data = request.POST  
        
        # Actualiza los campos del Producto con los datos proporcionados
        rol.nombre = data.get('nombre', rol.nombre)
        rol.descripcion= data.get('descripcion', rol.descripcion)
        rol.save()  # Guarda los cambios en la base de datos

        # Redirige a la página de detalles del producto (o a donde desees)
        return redirect('rol_lista')
        
        # Devuelve una respuesta JSON con los datos actualizados del Producto
        return JsonResponse({
            'id': producto.id,
            'nombre': rol.nombre,
            'descripcion': rol.descripcion,
        })
    
    # Maneja solicitudes GET para mostrar la página de actualización del producto
    elif request.method == 'GET':
        return render(request, 'rol_fm.html', {'rol': rol})
    
    # Si la solicitud no es ni POST ni GET, devuelve un error 405 (Método no permitido)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# Detalles
def rol_detail(request, pk):
    rol = get_object_or_404(Rol, pk=pk)
    return render(request, 'rol_detail.html', {'rol': rol})



# Listar usuarios
def usuarios(request):
    # Ordenar usuarios por id en orden descendente
    usuarios_list = Usuario.objects.all().order_by('-id')  # Cambia '-id' si usas otro campo para ordenar
    context = {
        'title': 'Lista de Usuarios',
        'usuarios': usuarios_list
    }

    # Renderizar la plantilla con los usuarios ordenados
    return render(request, 'usuarios_lista.html', context)



#Crear usuario
def usuario_create(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)  # No guardamos todavía el usuario
            rol_id = request.POST.get('rol')  # Obtener el rol seleccionado
            rol = Rol.objects.get(id=rol_id)  # Buscar el rol por ID
            
            usuario.rol = rol  # Asignar el rol al usuario
            
            # Guardar el usuario en la base de datos
            usuario.save()

            return redirect('usuarios')  # Redirigir a la lista de usuarios
    else:
        form = RegistroForm()
    
    roles = Rol.objects.all()  # Obtener todos los roles para el dropdown
    return render(request, 'usuarios_fm.html', {'form': form, 'roles': roles})

# Detalles
def usuario_detail(request, pk):
    usuario = get_object_or_404(Usuario, id=pk)
    return render(request, 'usuarios_detail.html', {'usuario': usuario})

#Actualiza

def usuario_update (request):
    return render(request, 'usuario_update.html')

#Eliminar usuario
def usuario_delete(request, pk):
  usuario = get_object_or_404(Usuario, pk=pk)
  if request.method == 'POST':
    usuario.delete()  # Call delete() on the retrieved object
    return redirect('usuarios')  # Redirect to 'usuarios' URL after deletion
  
  context = {'object': usuario}
  return render(request, 'usuarios_delete.html', context)