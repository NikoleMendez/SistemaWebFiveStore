from tutorials.models import Usuario
from django.shortcuts import render, redirect


def home(request):
    user_id = request.session.get('usuario_id')  # Obtener el usuario_id desde la sesión
    if not user_id:
        return redirect('login')  # Si no hay usuario en la sesión, redirigir al login

    try:
        user = Usuario.objects.get(id=user_id)  # Buscar al usuario por su id
        return render(request, 'home.html', {'user': user})  # Renderizar la página 'home' con el usuario
    except Usuario.DoesNotExist:
        return redirect('login')  # Si el usuario no existe, redirigir al login

   