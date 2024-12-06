import os
from tutorials.models import Cliente, Producto, Almacen, Venta, Cotizacion, DetalleVenta, Usuario
from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse,JsonResponse
from django.conf import settings
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


#@permiso_requerido('Permiso Venta')
def modulo_venta (request):
    return render(request, 'venta.html')

#Lista venta
def venta_lista(request):
    ventas = Venta.objects.all().order_by('-id')
    context = {
        'title': 'Lista de Ventas',
        'ventas': ventas
        
    }
    return render(request, 'ventas_lista.html', context)


#Elimina venta
def venta_delete(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        venta.delete()
        return redirect('venta_lista')
    
    context = {'object': venta}
    return render(request, 'ventas_delete.html', context)

#Crear venta
def venta_create(request):
    usuario_id = request.session.get('usuario_id')

    if not usuario_id:
        return redirect('login')

    usuario = get_object_or_404(Usuario, pk=usuario_id)
    productos = Producto.objects.all()
    almacenes = Almacen.objects.all()
    clientes = Cliente.objects.all()

    if request.method == 'POST':
        print("Datos recibidos:", request.POST)  # Depuración

        fecha = request.POST.get('fecha')
        cliente_id = request.POST.get('cliente')
        glosa = request.POST.get('glosa')
        tipo_pago = request.POST.get('tipo_pago')
        cantidades = request.POST.getlist('cantidad[]')
        precios = request.POST.getlist('preciov[]')
        productos_ids = request.POST.getlist('productos[]')

        if not productos_ids or not cantidades:
            return HttpResponse("Error: No se enviaron productos o cantidades.", status=400)

        if fecha and cliente_id:
            cliente = get_object_or_404(Cliente, pk=cliente_id)

            # Crear la venta sin los detalles
            venta = Venta.objects.create(
                fecha=fecha,
                cliente=cliente,
                glosa=glosa,
                tipo_pago=tipo_pago,
                usuario=usuario  # Asignar el usuario que realiza la venta
            )

            total_venta = 0

            for producto_id, cantidad_str, precio_str in zip(productos_ids, cantidades, precios):
                if not producto_id or producto_id.strip() == "":
                    print("Producto ID vacío o inválido.")  # Depuración
                    continue

                producto = get_object_or_404(Producto, pk=producto_id)
                cantidad = int(cantidad_str) if cantidad_str else 0
                precio = float(precio_str.replace(',', '.')) if precio_str else 0.0  # Manejar decimales con coma

                if cantidad > 0 and precio > 0:
                    almacenes = Almacen.objects.filter(producto=producto)

                    if almacenes.exists():
                        almacen = almacenes.first()

                        if almacen.cantidad >= cantidad:
                            total = cantidad * precio
                            total_venta += total

                            # Crear el detalle de la venta
                            DetalleVenta.objects.create(
                                venta=venta,
                                producto=producto,
                                cantidad=cantidad,
                                preciov=precio,
                                total=total,
                                usuario=usuario  # Asociar el usuario al detalle
                            )

                            # Actualizar el stock en el almacén
                            almacen.cantidad -= cantidad
                            almacen.save()
                        else:
                            return HttpResponse(f"Error: Stock insuficiente para {producto.nombre}.", status=400)
                    else:
                        return HttpResponse(f"Error: Producto {producto.nombre} no está en el almacén.", status=400)

            # Actualizar el total de la venta después de procesar todos los detalles
            venta.total = total_venta
            venta.save()

            return redirect('venta_lista')

    context = {
        'clientes': clientes,
        'productos': productos,
        'almacenes': almacenes,
    }
    return render(request, 'ventas_fm.html', context)





# Detalles Venta
def venta_detail(request, pk):
    # Obtener la venta específica
    venta = get_object_or_404(Venta, pk=pk)

    context = {
        'venta': venta,  # Asegúrate de pasar el objeto venta con la relación usuario
    }
    return render(request, 'ventas_detail.html', context)


def venta_pdf(request, pk):
    # Obtén la venta específica desde la base de datos usando pk
    venta = get_object_or_404(Venta, pk=pk)

    # Crear la respuesta HTTP con el tipo de contenido adecuado
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=detalleventa_{venta.pk}.pdf'

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
    elements.append(Paragraph(f'Reporte de Venta - #{venta.pk}', title_style))
    elements.append(Spacer(1, 0.2 * cm))

    # Línea de separación con sombra
    line = Table([[""]], colWidths=[480])
    line.setStyle(TableStyle([
        ('LINEBELOW', (0, 0), (-1, -1), 2, colors.grey),
    ]))
    elements.append(line)
    elements.append(Spacer(1, 0.3 * cm))

    # Información de venta y cliente
    registro_info_data = [
        [Paragraph(f"<b>Fecha de Venta:</b> {venta.fecha.strftime('%d/%m/%Y')}", normal_style),
         Paragraph(f"<b>Cliente:</b> {venta.cliente.nombre}", normal_style)],
        [Paragraph(f"<b>Tipo de Pago:</b> {venta.tipo_pago}", normal_style),
         Paragraph(f"<b>Glosa:</b> {venta.glosa}", normal_style)]
    ]

    # Obtener el usuario de la venta desde DetalleVenta
    primer_detalle = venta.detalles.first()
    if primer_detalle and hasattr(primer_detalle, 'usuario'):
        usuario_venta = primer_detalle.usuario.username
        registro_info_data.append([Paragraph(f"<b>Usuario Venta:</b> {usuario_venta}", normal_style)])

    registro_info_table = Table(registro_info_data, colWidths=[240, 240])
    registro_info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
    ]))
    elements.append(registro_info_table)
    elements.append(Spacer(1, 0.3 * cm))

    # Detalles de la venta (producto, categoría, cantidad, precio y total)
    data = [["Producto", "Categoría", "Cantidad", "Precio Venta", "Total"]]
    total_sum = 0

    # Iterar sobre los detalles para llenar la tabla
    for detalle in venta.detalles.all():
        subtotal = detalle.cantidad * detalle.preciov
        total_sum += subtotal
        data.append([
            detalle.producto.nombre,
            detalle.producto.categoria.nombre,
            detalle.cantidad,
            f"{detalle.preciov:.2f}",
            f"{subtotal:.2f}"
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

#cliente
def cliente_lista(request):
    # Ordenar los clientes por id en orden descendente
    cliente = Cliente.objects.all().order_by('-id')
    context = {
        'title': 'Lista de Clientes',
        'cliente': cliente
    }
    return render(request, 'clientes_lista.html', context)


def cliente_create (request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        email = request.POST.get('email')

        # Crear el proveedor en la base de datos
        cliente = Cliente.objects.create(
            nombre=nombre,
            telefono=telefono,
            direccion=direccion,
            email=email
        )

        # Redirigir a la lista de proveedor
        return redirect('cliente_lista')  # redirigir al nombre de la URL definida en urls.py

    # Si no es una solicitud POST, mostrar el formulario para crear un nuevo proveedor
    return render(request, 'clientes_fm.html')  # renderizar el formulario de creación de proveedor

#Actualiza
def cliente_update(request, pk):
    # Obtén la instancia del Producto que deseas actualizar
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':  # Maneja solicitudes POST para actualizar el producto
        data = request.POST  # Obtiene los datos de la solicitud POST
        
        # Actualiza los campos del Producto con los datos proporcionados
        cliente.nombre = data.get('nombre', cliente.nombre)
        cliente.telefono = data.get('telefono', cliente.telefono)
        cliente.direccion = data.get('direccion', cliente.direccion)
        cliente.email = data.get('email', cliente.email)
        cliente.save()  # Guarda los cambios en la base de datos

        # Redirige a la página de detalles del producto (o a donde desees)
        return redirect('cliente_lista')
        
        # Devuelve una respuesta JSON con los datos actualizados del Producto
        return JsonResponse({
            'id': cliente.id,
            'nombre': cliente.nombre,
            'telefono': cliente.telefono,
            'direccion': cliente.direccion,
            'email': cliente.email,
        })
    
    # Maneja solicitudes GET para mostrar la página de actualización del producto
    elif request.method == 'GET':
        return render(request, 'clientes_fm.html', {'cliente': cliente})
    
    # Si la solicitud no es ni POST ni GET, devuelve un error 405 (Método no permitido)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('cliente_lista')
    
    context = {'object': cliente}
    return render(request, 'clientes_delete.html', context)

# Detalles
def cliente_detail(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, 'clientes_detail.html', {'cliente': cliente})

# Cotizacion lista
def cotizacion_lista(request):
    # Ordenar las cotizaciones por id en orden descendente
    cotizacion = Cotizacion.objects.all().order_by('-id')
    context = {
        'cotizacion': cotizacion,
    }
    return render(request, 'cotizacion_lista.html', context)


# Cotizacion Create
def cotizacion_create(request):
    productos = Producto.objects.all()
    almacenes = Almacen.objects.all()
    clientes = Cliente.objects.all()

    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        cliente_id = request.POST.get('cliente')
        cotizacion = request.POST.get('cotizacion')
        cantidades = request.POST.getlist('cantidad[]') 
        preciov = request.POST.getlist('preciov[]') 
        productos_ids = request.POST.getlist('productos[]')  

        if fecha and cliente_id and cantidades and productos_ids:
            cliente = get_object_or_404(Cliente, pk=cliente_id)

            for producto_id, cantidad_str in zip(productos_ids, cantidades):
                cantidad = int(cantidad_str) if cantidad_str else 0  # Convertir la cantidad a entero

                if cantidad > 0:  
                    # Buscar el producto y el registro correspondiente en Almacen
                    producto = get_object_or_404(Producto, pk=producto_id)
                    almacen = get_object_or_404(Almacen, producto=producto)

                    # Verificar si hay suficiente stock sin modificar el almacén
                    if almacen.cantidad >= cantidad:
                        # Calcular el total usando el precio de venta del almacen
                        total = cantidad * almacen.preciov

                        # Crear el registro de la cotización sin afectar el stock en el almacén
                        Cotizacion.objects.create(
                            fecha=fecha,
                            cliente=cliente,
                            cotizacion=cotizacion,
                            producto=producto,
                            cantidad=cantidad,
                            preciov=almacen.preciov,
                            total=total,
                        )
                    else:
                        # Si no hay suficiente stock, mostrar un mensaje de error
                        print(f"No hay suficiente stock para el producto {producto.nombre}")
                        return redirect('cotizacion_create')  # Redirige en caso de error de stock

            return redirect('cotizacion_lista')

    context = {
        'clientes': clientes,
        'productos': productos,
        'almacenes': almacenes,
    }
    return render(request, 'cotizacion_fm.html', context)

# Detalles
def cotizacion_detail(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    precio_venta = cotizacion.producto.almacen_set.first().preciov if cotizacion.producto.almacen_set.exists() else None

    context = {
        'cotizacion': cotizacion,
        'precio_venta': precio_venta,
    }
    return render(request, 'cotizacion_detail.html', context)

#Cotizacion PDF
def cotizacion_pdf(request, pk):
    # Obtén la cotización específica desde la base de datos usando pk
    cotizacion = get_object_or_404(Cotizacion, pk=pk)

    # Crear la respuesta HTTP con el tipo de contenido adecuado
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=cotizacion_{cotizacion.pk}.pdf'

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
    header_text = Table([[
        Paragraph("<b>Five Store Bolivia</b><br/>Año: 2024<br/>Dirección: Av. Ejército Nacional", normal_style)
    ]], colWidths=[280])
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

    header_data = [[logo, header_text]]
    header_table = Table(header_data, colWidths=[200, 300])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))

    elements.append(header_table)
    elements.append(Spacer(1, 0.3 * cm))

    # Título del reporte antes de la línea
    elements.append(Paragraph(f'Cotización - #{cotizacion.pk}', title_style))
    elements.append(Spacer(1, 0.2 * cm))

    # Línea de separación con sombra
    line = Table([[""]], colWidths=[480])
    line.setStyle(TableStyle([('LINEBELOW', (0, 0), (-1, -1), 2, colors.grey)]))
    elements.append(line)
    elements.append(Spacer(1, 0.3 * cm))

    # Información de venta y cliente
    registro_info_data = [
        [Paragraph(f"<b>Fecha:</b> {cotizacion.fecha.strftime('%d/%m/%Y %H:%M:%S')}", normal_style),
         Paragraph(f"<b>Cliente:</b> {cotizacion.cliente.nombre}", normal_style)],
        [Paragraph(f"<b>Cotización:</b> {cotizacion.cotizacion}", normal_style)]
    ]
    registro_info_table = Table(registro_info_data, colWidths=[240, 240])
    registro_info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
    ]))
    elements.append(registro_info_table)
    elements.append(Spacer(1, 0.3 * cm))

    # Detalles de la venta (producto, categoría, cantidad, precio y total)
    data = [["Producto", "Categoría", "Cantidad", "Precio Venta", "Total"]]
    total_sum = 0

    # Validar datos y agregar fila
    cantidad = cotizacion.cantidad if cotizacion.cantidad is not None else 0
    preciov = cotizacion.preciov if cotizacion.preciov is not None else 0
    subtotal = cantidad * preciov
    total_sum += subtotal

    data.append([
        cotizacion.producto.nombre if cotizacion.producto else "Sin producto",
        cotizacion.producto.categoria.nombre if cotizacion.producto and cotizacion.producto.categoria else "Sin categoría",
        cantidad,
        f"{preciov:.2f}",
        f"{subtotal:.2f}"
    ])

    # Tabla de detalles de productos
    detail_table = Table(data, colWidths=[140, 100, 60, 80, 100], hAlign='CENTER')
    detail_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    elements.append(detail_table)
    elements.append(Spacer(1, 0.3 * cm))

    # Agregar monto total
    total_data = [[Paragraph("<b>Monto Total</b>", normal_style), f"{total_sum:.2f}"]]
    total_table = Table(total_data, colWidths=[400, 80])
    total_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
    ]))
    elements.append(total_table)

    # Generar el PDF con los elementos creados
    pdf.build(elements)
    return response