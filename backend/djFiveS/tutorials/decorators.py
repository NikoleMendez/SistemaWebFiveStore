from functools import wraps
from django.http import HttpResponse

def permiso_requerido(nombre_permiso):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            permisos = request.session.get('permisos', [])
            if nombre_permiso in permisos:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('No tienes permiso para acceder a esta página.', status=403)
        return _wrapped_view
    return decorator