from django.contrib import admin
from django.db.models import Avg

from .models import Artigo, Comentario, Like, Rating


@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'data_criacao', 'total_likes', 'rating_medio')
    list_filter = ('data_criacao', 'autor')
    search_fields = ('titulo', 'texto', 'autor__username')

    def total_likes(self, obj):
        return obj.likes.count()

    total_likes.short_description = 'Likes'

    def rating_medio(self, obj):
        media = obj.ratings.aggregate(media=Avg('pontuacao'))['media']
        if media is None:
            return '-'
        return f'{media:.1f}'

    rating_medio.short_description = 'Rating medio'


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('artigo', 'nome_do_autor', 'data_criacao')
    list_filter = ('data_criacao', 'autor')
    search_fields = ('texto', 'nome_visitante', 'artigo__titulo', 'autor__username')

    def nome_do_autor(self, obj):
        return obj.nome_autor

    nome_do_autor.short_description = 'Autor'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('artigo', 'user', 'session_key', 'data_criacao')
    list_filter = ('data_criacao',)
    search_fields = ('artigo__titulo', 'user__username', 'session_key')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('artigo', 'pontuacao', 'user', 'session_key', 'data_criacao', 'data_atualizacao')
    list_filter = ('pontuacao', 'data_criacao', 'data_atualizacao')
    search_fields = ('artigo__titulo', 'user__username', 'session_key')
