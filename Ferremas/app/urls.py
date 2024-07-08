from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.inicio),
    path('inicio', views.inicio, name='inicio'),

    # Login
    path('login_registro', views.login_registro, name='login_registro'),
    path("logout/", views.logout_view, name="logout"),
    
    # Agregar producto (solo para administradores)
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),
    path('load-subcategorias/', views.load_subcategorias, name='load_subcategorias'),

    # Lista de productos
    path('productos/', views.lista_productos, name='lista_productos'),


   # Carrito
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('comprar-producto/', views.comprar_producto, name='comprar_producto'),
    path('sumar-producto/', views.sumar_producto, name='sumar_producto'),
    path('restar-producto/', views.restar_producto, name='restar_producto'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)