from django.contrib import admin
from django.urls import include, path
from tutorials.vistas import login, ventas, header, inicio,administracion, stock,compra, informe, configuracion, views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('admin/', admin.site.urls),
    
    #LOGIN
    path('', login.login_view, name='login'),
    path('signout/', login.signout, name='signout'),
    path('perfil/', login.perfil, name='perfil'),
    path('prueba-mensajes/', views.prueba_mensajes, name='prueba_mensajes'),

    path('home/', inicio.home, name='home'),

    #ACCESORIOS
    path('header/', header.header, name='header'),
    
    #CONFIGURACION
    path('configuracion/', configuracion.configuracion ,name='configuracion'),
    path('configuracion/qr', views.cargar_qr ,name='cargar_qr'),

    #ADMINISTRACION
    path('administracion/', administracion.modulo_administracion ,name='modulo_administracion'),

    #ROL
    path('adm/add/rol/', administracion.rol_lista ,name='rol_lista'),
    path('rol/create/', administracion.rol_create, name='rol_create'),
    path('rol/update/<int:pk>/', administracion.rol_update, name = 'rol_update'),
    path('rol/delete/<int:pk>/', administracion.rol_delete, name = 'rol_delete'),
    path('rol/detail/<int:pk>/', administracion.rol_detail, name='rol_detail'),

    #permisos
    path('adm/add/permiso/', administracion.permiso_lista ,name='permiso_lista'),
    path('permiso/create/', administracion.permiso_create, name='permiso_create'),
    path('permiso/delete/<int:pk>/', administracion.permiso_delete, name = 'permiso_delete'),
    
    #usuarios
    path('usuarios/list/', administracion.usuarios ,name='usuarios'),
    path('usuarios/create/', administracion.usuario_create, name='usuario_create'),
    path('delete/<int:pk>/', administracion.usuario_delete, name = 'usuario_delete'),
    path('detail/<int:pk>/', administracion.usuario_detail, name = 'usuario_detail'),
    path('adm/update/<int:pk>/', administracion.usuario_update, name = 'usuario_update'),
   

    #COMPRA
    path('compra/', compra.modulo_compra ,name='modulo_compra'),
    #COMPRAS
    path('compra/list/', compra.compra_lista ,name='compra_lista'),
    path('compra/create/', compra.compra_create ,name='compra_create'),
    path('compra/detail/<int:pk>/', compra.compra_detail, name='compra_detail'),
    path('compra/delete/<int:pk>/',  compra.compra_delete, name = 'compra_delete'),
    path('compra/<int:pk>/pdf/', compra.compra_pdf, name='compra_pdf'),

    #proveedores
    path('proveedor/list/', compra.proveedor_lista ,name='proveedor_lista'),
    path('proveedor/create/', compra.proveedor_create, name='proveedor_create'),
    path('proveedor/delete/<int:pk>/',  compra.proveedor_delete, name = 'proveedor_delete'),
    path('proveedor/detail/<int:pk>/', compra.proveedor_detail, name='proveedor_detail'),
    path('proveedor/update/<int:pk>/', compra.proveedor_update, name = 'proveedor_update'),


    #MODULO VENTA
    path('venta/', ventas.modulo_venta ,name='modulo_venta'),
    #Ventas
    path('venta/list/', ventas.venta_lista ,name='venta_lista'),
    path('ventas/create/', ventas.venta_create, name='venta_create'),
    path('venta/delete/<int:pk>/',  ventas.venta_delete, name = 'venta_delete'),
    path('venta/detail/<int:pk>/', ventas.venta_detail, name='venta_detail'),
    path('ventas/<int:pk>/pdf/', ventas.venta_pdf, name='venta_pdf'),


    #clientes
    path('ventas/cliente/list/', ventas.cliente_lista ,name='cliente_lista'),
    path('ventas/cliente/create/', ventas.cliente_create, name='cliente_create'),
    path('ventas/update/<int:pk>/', ventas.cliente_update, name = 'cliente_update'),
    path('venta/cliente/delete/<int:pk>/',  ventas.cliente_delete, name = 'cliente_delete'),
    path('venta/cliente/detail/<int:pk>/', ventas.cliente_detail, name='cliente_detail'),

    #Cotizacion
    path('ventas/cotizacion/list/', ventas.cotizacion_lista ,name='cotizacion_lista'),
    path('ventas/cotizacion/create/', ventas.cotizacion_create ,name='cotizacion_create'),
    path('ventas/cotizacion/detail/<int:pk>/', ventas.cotizacion_detail ,name='cotizacion_detail'),
    path('ventas/cotizacion/<int:pk>/pdf/', ventas.cotizacion_pdf, name='cotizacion_pdf'),


    #MODULO ALMACEN
    path('stock/', stock.modulo_stock ,name='modulo_stock'),
    #Productos
    path('stock/producto/list/', stock.producto ,name='producto'),
    path('producto/create/', stock.producto_create, name='producto_create'),
    path('producto/detail/<int:pk>/', stock.producto_detail, name='producto_detail'),
    path('producto/update/<int:pk>/', stock.producto_update, name = 'producto_update'),
    path('producto/delete/<int:pk>/',  stock.producto_delete, name = 'producto_delete'),

    #Almacen
    path('almacen/list/', stock.almacen_lista ,name='almacen_lista'),
    path('almacen/update/<int:pk>/', stock.almacen_update, name = 'almacen_update'),
    path('almacen/delete/<int:pk>/',  stock.almacen_delete, name = 'almacen_delete'),

    #Categoria
    path('categoria/list/', stock.categoria_lista ,name='categoria_lista'),
    path('categoria/create/', stock.categoria_create, name='categoria_create'),
    path('categoria/detail/<int:pk>/', stock.categoria_detail, name='categoria_detail'),
    path('categoria/update/<int:pk>/', stock.categoria_update, name = 'categoria_update'),
    path('categoria/delete/<int:pk>/',  stock.categoria_delete, name = 'categoria_delete'),
    
    
    
    #MODULO DE REPORTES
    path('informe/', informe.modulo_informe ,name='modulo_informe'),

    #Informe Compras
    path('informe/compras/', informe.informecompra_lista ,name='informecompra_lista'),
    path('informe/ventas/', informe.informeventa_lista ,name='informeventa_lista'),
    path('informe/stock/', informe.informestock_lista ,name='informestock_lista'),

    #Informe Ventas
    path('informe/compras/excel/', informe.compra_excel ,name='compra_excel'),
    path('informe/compras/pdf/', informe.compra_pdf ,name='compra_pdf'),
    path('informe/ventas/excel/', informe.venta_excel ,name='venta_excel'),
    path('informe/ventas/pdf/', informe.venta_pdf ,name='venta_pdf'),

    #Informe Stock
    path('informe/stock/excel/', informe.stock_excel ,name='stock_excel'),
    path('informe/stock/pdf/', informe.stock_pdf ,name='stock_pdf'),


    #Margen
    path('margen/create/', stock.margen_create ,name='margen_create'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
