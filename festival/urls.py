from django.urls import path
from . import views

urlpatterns = [
    path('inicio/', views.inicio, name='inicio'),
    path('', views.index, name='index'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login, name='login'),

    path(
        'categorias/',
        views.categorias_votacion,
        name='categorias_votacion'
    ),

    path(
        'votar/<int:categoria_id>/',
        views.votar,
        name='votar'
    ),

    path(
        'mis-votos/',
        views.mis_votos,
        name='mis_votos'
    ),

    path(
    'resultados/',
    views.resultados,
    name='resultados'
    ),

    path(
    'logout/',
    views.logout,
    name='logout'
    ),

    path(
    'api/categorias/',
    views.api_categorias,
    name='api_categorias'
    ),
]

