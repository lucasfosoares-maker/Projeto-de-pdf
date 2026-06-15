from django.urls import path
from . import views

urlpatterns = [
    path('',              views.upload,     name='upload'),
    path('lista/',        views.lista,      name='lista'),
    path('doc/<int:pk>/', views.detalhe,    name='detalhe'),
    path('doc/<int:pk>/txt/',    views.baixar_txt, name='baixar_txt'),
    path('doc/<int:pk>/excluir/', views.excluir,   name='excluir'),
]
