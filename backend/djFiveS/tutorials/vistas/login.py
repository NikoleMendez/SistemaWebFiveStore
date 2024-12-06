from tutorials.models import Usuario
from django.shortcuts import render, redirect
from django.http import JsonResponse


def mensaje(request):
    mensaje = "¡Hola desde Django!"
    return JsonResponse({'mensaje': mensaje})

def sesion(request): 
    return render(request, 'sesion.html')


def login_view(request):
    msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Username: {username}, Password: {password}")  # Debugging

        try:
            user = Usuario.objects.get(username=username)
            if user.check_password(password):
                request.session['usuario_id'] = user.id
                return redirect('home')
            else:
                msg = 'Contraseña incorrecta'
        except Usuario.DoesNotExist:
            msg = 'Usuario no encontrado'

    return render(request, 'login.html', {'msg': msg})


#perfil
def perfil(request):
    user_id = request.session.get('usuario_id')  # Obtener usuario_id desde la sesión
    if not user_id:
        return redirect('login')

    try:
        user = Usuario.objects.get(id=user_id)
        return render(request, 'perfil.html', {'user': user})
    except Usuario.DoesNotExist:
        return redirect('login')


def signout(request):
    if 'usuario_id' in request.session:
        del request.session['usuario_id']  # Elimina usuario_id de la sesión

    return redirect('login')  # Redirige al usuario al login después de cerrar sesión

def logout(request):
    response = redirect('login')
    response.delete_cookie('user_id')
    return response