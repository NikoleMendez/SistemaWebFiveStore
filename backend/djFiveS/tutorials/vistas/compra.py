import os
from datetime import datetime
from tutorials.models import Proveedor, Producto, Compra, Almacen, DetalleCompra, Usuario
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image


#Principal
def modulo_compra (request):
    return render(request, 'compra.html')


#Lista compra
def compra_lista(request):
    # Ordenar las compras por id en orden descendente
    compras = Compra.objects.all().order_by('-id')
    context = {
        'title': 'Lista de Compras',
        'compras': compras
    }
    return render(request, 'compras_lista.html', context)



# Crear Compra
def compra_create(request):
    proveedores = Proveedor.objects.all()
    productos = Producto.objects.all()

    if request.method == 'POST':
        fecha_registro = request.POST.get('fecha_registro')
        proveedor_id = request.POST.get('proveedor')

        if fecha_registro and proveedor_id:
            proveedor = get_object_or_404(Proveedor, pk=proveedor_id)

            total_compra = 0  # Para calcular el total de la compra
            i = 0
            while True:
                # Obtener datos del producto
                producto_id = request.POST.get(f'producto_{i}')
                cantidad = request.POST.get(f'cantidad_{i}')
                precio_compra = request.POST.get(f'precio_compra_{i}')
                precio_venta = request.POST.get(f'precio_venta_{i}')

                if producto_id and cantidad and precio_compra:
                    producto = get_object_or_404(Producto, pk=producto_id)
                    cantidad = int(cantidad)
                    precio_compra = float(precio_compra)

                    # Verificar si ya existe el producto en el almacén
                    almacen_existente = Almacen.objects.filter(producto=producto).first()

                    if almacen_existente:
                        # Si el precio de compra es igual, solo sumar la cantidad
                        if almacen_existente.precioc == precio_compra:
                            almacen_existente.cantidad += cantidad
                        else:
                            # Calcular el nuevo precio ponderado
                            total_costo_actual = almacen_existente.cantidad * almacen_existente.precioc
                            total_costo_nuevo = cantidad * precio_compra
                            nueva_cantidad = almacen_existente.cantidad + cantidad

                            nuevo_precio_ponderado = (total_costo_actual + total_costo_nuevo) / nueva_cantidad

                            # Actualizar precio de compra y calcular nuevo precio de venta
                            almacen_existente.precioc = nuevo_precio_ponderado
                            almacen_existente.preciov = nuevo_precio_ponderado * 1.30  # Aplicar el 30% de ganancia
                            almacen_existente.cantidad = nueva_cantidad

                        almacen_existente.fecha = fecha_registro  # Actualizar la fecha
                        almacen_existente.save()
                    else:
                        # Si no existe, crear el registro inicial
                        almacen_existente = Almacen.objects.create(
                            producto=producto,
                            categoria=producto.categoria,
                            cantidad=cantidad,
                            precioc=precio_compra,
                            preciov=precio_compra * 1.30,
                            fecha=fecha_registro
                        )

                    # Registrar el detalle de la compra
                    total_detalle = precio_compra * cantidad
                    total_compra += total_detalle  # Sumar al total de la compra

                    # Crear el registro de la compra
                    Compra.objects.create(
                        fecha=fecha_registro,
                        proveedor=proveedor,
                        producto=producto,
                        cantidad=cantidad,
                        precioc=precio_compra,
                        preciov=almacen_existente.preciov,
                        total=total_detalle
                    )

                    i += 1
                else:
                    break

            return redirect('compra_lista')

    context = {
        'proveedores': proveedores,
        'productos': productos
    }
    return render(request, 'compras_fm.html', context)




# Detalles Compra
def compra_detail(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    return render(request, 'compras_detail.html', {'compra': compra})



#Elimina compra
def compra_delete(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    
    # Simplemente elimina la compra sin tocar el almacen
    compra.delete()
    
    return redirect('compras_delete')


#compra PDF
def compra_pdf(request, pk):
    # Obtén la compra específica desde la base de datos usando pk
    compra = get_object_or_404(Compra, pk=pk)

    # Crear la respuesta HTTP con el tipo de contenido adecuado
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=detallecompra_{compra.pk}.pdf'

    # Crear el documento PDF con márgenes de 2 cm
    pdf = SimpleDocTemplate(response, pagesize=letter, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    elements = []

    # Estilos de texto
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(name='Title', fontSize=14, alignment=1, leading=14, fontName="Helvetica-Bold")
    normal_style = styles['BodyText']

    # Agregar logotipo centrado (logo más ancho)
    logo_path = os.path.join(settings.STATICFILES_DIRS[0], 'img', 'FiveStore.jpg')
    logo = Image(logo_path, width=200, height=80)  # Logo más ancho
    logo.hAlign = 'CENTER'

    # Encabezado principal con información de la empresa
    header_text = Table([
        [Paragraph("<b>Five Store Bolivia</b><br/>Año: 2024<br/>Dirección: av. Ejercito Nacional", normal_style)]
    ], colWidths=[280])

    header_text.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ('ROUNDRECT', (0, 0), (-1, -1), 20, 1, colors.black),
    ]))

    header_data = [
        [logo, header_text]
    ]
    header_table = Table(header_data, colWidths=[200, 300])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))

    elements.append(header_table)
    elements.append(Spacer(1, 0.3 * cm))

    # Título del reporte antes de la línea
    elements.append(Paragraph(f'Reporte de Detalle Compra - #{compra.pk}', title_style))
    elements.append(Spacer(1, 0.2 * cm))

    # Línea de separación con sombra
    line = Table([[""]], colWidths=[480])
    line.setStyle(TableStyle([
        ('LINEBELOW', (0, 0), (-1, -1), 2, colors.grey),
    ]))
    elements.append(line)
    elements.append(Spacer(1, 0.3 * cm))

    # Información de compra y proveedor
    current_date = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    registro_info_data = [
        [Paragraph(f"<b>Fecha de Compra:</b> {compra.fecha.strftime('%d/%m/%Y %H:%M:%S')}", normal_style), 
         Paragraph(f"<b>Proveedor:</b> {compra.proveedor.nombre}", normal_style)],
    ]
    registro_info_table = Table(registro_info_data, colWidths=[240, 240])
    registro_info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
    ]))
    elements.append(registro_info_table)
    elements.append(Spacer(1, 0.3 * cm))

    # Detalles de la compra (producto, categoría, cantidad, precio y total)
    data = [["Producto", "Categoría", "Cantidad", "Precio Compra", "Total"]]
    total_sum = 0

    # Itera sobre los productos en la compra
    subtotal = compra.cantidad * compra.preciov
    total_sum += subtotal
    data.append([
        compra.producto.nombre, 
        compra.producto.categoria.nombre, 
        compra.cantidad, 
        compra.preciov, 
        subtotal
    ])
    # Tabla de detalles de productos
    detail_table = Table(data, colWidths=[140, 100, 60, 80, 100], hAlign='CENTER')
    detail_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    elements.append(detail_table)
    elements.append(Spacer(1, 0.3 * cm))

    # Agregar monto total
    total_data = [
        [Paragraph("<b>Monto Total</b>", normal_style), f"{total_sum:.2f}"]
    ]
    total_table = Table(total_data, colWidths=[400, 80])
    total_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
    ]))
    elements.append(total_table)

    # Generar el PDF con los elementos creados
    pdf.build(elements)
    return response


#Proveedor Lista
def proveedor_lista(request):
    # Ordenar proveedores por id en orden descendente
    proveedores = Proveedor.objects.all().order_by('-id')
    context = {
        'title': 'Lista de Proveedores',
        'proveedor': proveedores
    }
    return render(request, 'proveedor_lista.html', context)

def proveedor_create (request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        email = request.POST.get('email')

        # Crear el proveedor en la base de datos
        proveedor = Proveedor.objects.create(
            nombre=nombre,
            telefono=telefono,
            direccion=direccion,
            email=email
        )

        # Redirigir a la lista de proveedor
        return redirect('proveedor_lista')  # redirigir al nombre de la URL definida en urls.py

    # Si no es una solicitud POST, mostrar el formulario para crear un nuevo proveedor
    return render(request, 'proveedor_fm.html')  # renderizar el formulario de creación de proveedor

def proveedor_delete(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('proveedor_lista')
    
    context = {'object': proveedor}
    return render(request, 'proveedor_delete.html', context)

# Detalles
def proveedor_detail(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    return render(request, 'proveedor_detail.html', {'proveedor': proveedor})

#Actualiza
def proveedor_update(request, pk):
    # Obtén la instancia del Producto que deseas actualizar
    proveedor = get_object_or_404(Proveedor, pk=pk)
    
    if request.method == 'POST':  # Maneja solicitudes POST para actualizar el producto
        data = request.POST  # Obtiene los datos de la solicitud POST
        
        # Actualiza los campos del Producto con los datos proporcionados
        proveedor.nombre = data.get('nombre', proveedor.nombre)
        proveedor.telefono = data.get('telefono', proveedor.telefono)
        proveedor.direccion = data.get('direccion', proveedor.direccion)
        proveedor.email = data.get('email', proveedor.email)
        proveedor.save()  # Guarda los cambios en la base de datos

        # Redirige a la página de detalles del producto (o a donde desees)
        return redirect('proveedor_lista')
        
        # Devuelve una respuesta JSON con los datos actualizados del Producto
        return JsonResponse({
            'id': proveedor.id,
            'nombre': proveedor.nombre,
            'telefono': proveedor.telefono,
            'direccion': proveedor.direccion,
            'email': proveedor.email,

        })
    
    # Maneja solicitudes GET para mostrar la página de actualización del producto
    elif request.method == 'GET':
        return render(request, 'proveedor_fm.html', {'proveedor': proveedor})
    
    # Si la solicitud no es ni POST ni GET, devuelve un error 405 (Método no permitido)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


