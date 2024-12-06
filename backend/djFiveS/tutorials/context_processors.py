# context_processors.py
from tutorials.models import Usuario
from django.core import signing
# tutorials/context_processors.py

from .models import Usuario, Permiso

def modulos_permitidos(request):
    modulos = {
        'modulo_administracion': False,
        'modulo_compra': False,
        'modulo_venta': False,
        'modulo_stock': False,
        'modulo_informe': False,
    }

    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            rol = usuario.rol
            if rol:
                permisos = Permiso.objects.filter(rol=rol)
                for permiso in permisos:
                    modulos['modulo_administracion'] |= permiso.modulo_administracion
                    modulos['modulo_compra'] |= permiso.modulo_compra
                    modulos['modulo_venta'] |= permiso.modulo_venta
                    modulos['modulo_stock'] |= permiso.modulo_stock
                    modulos['modulo_informe'] |= permiso.modulo_informe
        except Usuario.DoesNotExist:
            pass

    return {'modulos': modulos}