from django.urls import path

from . import views


urlpatterns = [
    path('', views.lista_artigos, name='lista_artigos'),
    path('novo/', views.criar_artigo, name='criar_artigo'),
    path('<int:artigo_id>/', views.detalhe_artigo, name='detalhe_artigo'),
    path('<int:artigo_id>/editar/', views.editar_artigo, name='editar_artigo'),
    path('<int:artigo_id>/like/', views.like_artigo, name='like_artigo'),
    path('<int:artigo_id>/comentar/', views.comentar_artigo, name='comentar_artigo'),
    path('<int:artigo_id>/avaliar/', views.avaliar_artigo, name='avaliar_artigo'),
]
