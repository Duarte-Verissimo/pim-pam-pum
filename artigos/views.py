from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ArtigoForm, ComentarioForm, RatingForm
from .models import Artigo, Like, Rating
from .utils import user_is_blogger


def lista_artigos(request):
    artigos = (
        Artigo.objects.select_related('autor')
        .annotate(
            media_rating=Avg('ratings__pontuacao'),
            total_likes=Count('likes', distinct=True),
            total_ratings=Count('ratings', distinct=True),
        )
        .order_by('-data_criacao')
    )

    return render(
        request,
        'artigos/lista_artigos.html',
        {
            'artigos': artigos,
            'user_is_blogger': user_is_blogger(request.user),
        },
    )


def detalhe_artigo(request, artigo_id):
    artigo = get_object_or_404(
        Artigo.objects.select_related('autor'),
        id=artigo_id,
    )
    comentarios = artigo.comentarios.select_related('autor')
    comentario_form = ComentarioForm(
        mostrar_nome_visitante=not request.user.is_authenticated,
    )
    rating_atual = None
    rating_stats = artigo.ratings.aggregate(
        media_rating=Avg('pontuacao'),
        total_ratings=Count('id'),
    )

    liked = False
    if request.user.is_authenticated:
        liked = artigo.likes.filter(user=request.user).exists()
        rating_atual = artigo.ratings.filter(user=request.user).first()
    elif request.session.session_key:
        liked = artigo.likes.filter(
            user__isnull=True,
            session_key=request.session.session_key,
        ).exists()
        rating_atual = artigo.ratings.filter(
            user__isnull=True,
            session_key=request.session.session_key,
        ).first()

    rating_form = RatingForm(
        initial={'pontuacao': rating_atual.pontuacao if rating_atual else None},
    )

    return render(
        request,
        'artigos/detalhe_artigo.html',
        {
            'artigo': artigo,
            'comentarios': comentarios,
            'comentario_form': comentario_form,
            'rating_form': rating_form,
            'media_rating': rating_stats['media_rating'],
            'total_ratings': rating_stats['total_ratings'],
            'likes_count': artigo.likes.count(),
            'liked': liked,
            'pode_editar': user_is_blogger(request.user) and request.user == artigo.autor,
        },
    )


@login_required
def criar_artigo(request):
    if not user_is_blogger(request.user):
        return HttpResponseForbidden("Nao tem permissao para criar artigos.")

    form = ArtigoForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        artigo = form.save(commit=False)
        artigo.autor = request.user
        artigo.save()
        return redirect('detalhe_artigo', artigo_id=artigo.id)

    return render(
        request,
        'artigos/form_artigo.html',
        {
            'form': form,
            'titulo_pagina': 'Criar artigo',
            'texto_botao': 'Criar artigo',
        },
    )


@login_required
def editar_artigo(request, artigo_id):
    artigo = get_object_or_404(Artigo, id=artigo_id)

    if not user_is_blogger(request.user):
        return HttpResponseForbidden("Nao tem permissao para editar artigos.")

    if artigo.autor != request.user:
        return HttpResponseForbidden("Nao pode editar artigos de outro autor.")

    form = ArtigoForm(
        request.POST or None,
        request.FILES or None,
        instance=artigo,
    )

    if form.is_valid():
        form.save()
        return redirect('detalhe_artigo', artigo_id=artigo.id)

    return render(
        request,
        'artigos/form_artigo.html',
        {
            'form': form,
            'artigo': artigo,
            'titulo_pagina': 'Editar artigo',
            'texto_botao': 'Guardar alteracoes',
        },
    )


@require_POST
def like_artigo(request, artigo_id):
    artigo = get_object_or_404(Artigo, id=artigo_id)

    if request.user.is_authenticated:
        like = Like.objects.filter(artigo=artigo, user=request.user).first()
        if like:
            like.delete()
        else:
            Like.objects.create(artigo=artigo, user=request.user)
    else:
        if not request.session.session_key:
            request.session.save()

        like = Like.objects.filter(
            artigo=artigo,
            user__isnull=True,
            session_key=request.session.session_key,
        ).first()
        if like:
            like.delete()
        else:
            Like.objects.create(
                artigo=artigo,
                session_key=request.session.session_key,
            )

    return redirect('detalhe_artigo', artigo_id=artigo.id)


@require_POST
def comentar_artigo(request, artigo_id):
    artigo = get_object_or_404(Artigo, id=artigo_id)
    form = ComentarioForm(
        request.POST,
        mostrar_nome_visitante=not request.user.is_authenticated,
    )

    if form.is_valid():
        comentario = form.save(commit=False)
        comentario.artigo = artigo
        if request.user.is_authenticated:
            comentario.autor = request.user
            comentario.nome_visitante = ''
        comentario.save()

    return redirect('detalhe_artigo', artigo_id=artigo.id)


@require_POST
def avaliar_artigo(request, artigo_id):
    artigo = get_object_or_404(Artigo, id=artigo_id)
    form = RatingForm(request.POST)

    if form.is_valid():
        pontuacao = form.cleaned_data['pontuacao']

        if request.user.is_authenticated:
            Rating.objects.update_or_create(
                artigo=artigo,
                user=request.user,
                defaults={
                    'pontuacao': pontuacao,
                    'session_key': None,
                },
            )
        else:
            if not request.session.session_key:
                request.session.save()

            Rating.objects.update_or_create(
                artigo=artigo,
                user=None,
                session_key=request.session.session_key,
                defaults={'pontuacao': pontuacao},
            )

    return redirect('detalhe_artigo', artigo_id=artigo.id)
