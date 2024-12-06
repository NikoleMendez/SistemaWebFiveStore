import os
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage


def cargar_qr(request):
    if request.method == 'POST' and request.FILES.get('qr_image'):
        qr_image = request.FILES['qr_image']
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'qr_images'), base_url=settings.MEDIA_URL + 'qr_images/')
        filename = fs.save(qr_image.name, qr_image)
        qr_image_url = fs.url(filename)
        
        # Guarda la URL de la última imagen cargada en la sesión
        request.session['qr_image_url'] = qr_image_url
        
        return JsonResponse({'qr_image_url': qr_image_url})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

from django.contrib import messages

def prueba_mensajes(request):
    messages.error(request, "Mensaje de prueba: este es un mensaje de error.")
    print("Mensajes generados:", list(messages.get_messages(request)))  # Imprime los mensajes
    return render(request, 'ventas_fm.html', {})