from django.shortcuts import render


def configuracion (request): 
    return render(request, 'configuracion.html')