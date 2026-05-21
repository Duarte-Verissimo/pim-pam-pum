from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q


class Artigo(models.Model):
    titulo = models.CharField(max_length=200)
    texto = models.TextField()
    fotografia = models.ImageField(upload_to='artigos/', blank=True, null=True)
    link_externo = models.URLField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artigos')

    class Meta:
        ordering = ['-data_criacao']

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    artigo = models.ForeignKey(
        Artigo,
        on_delete=models.CASCADE,
        related_name='comentarios',
    )
    autor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='comentarios_artigos',
    )
    nome_visitante = models.CharField(max_length=80, blank=True)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data_criacao']

    def __str__(self):
        return f"Comentario de {self.nome_autor} em {self.artigo.titulo}"

    @property
    def nome_autor(self):
        if self.autor:
            return self.autor.username
        return self.nome_visitante.strip() or 'Visitante'


class Like(models.Model):
    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='likes_artigos',
    )
    session_key = models.CharField(max_length=40, blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['artigo', 'user'],
                condition=Q(user__isnull=False),
                name='unique_like_por_user_artigo',
            ),
            models.UniqueConstraint(
                fields=['artigo', 'session_key'],
                condition=Q(session_key__isnull=False) & ~Q(session_key=''),
                name='unique_like_por_sessao_artigo',
            ),
        ]

    def __str__(self):
        if self.user:
            return f"Like de {self.user.username} em {self.artigo.titulo}"
        return f"Like anonimo em {self.artigo.titulo}"


class Rating(models.Model):
    PONTUACAO_CHOICES = [(valor, str(valor)) for valor in range(1, 6)]

    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name='ratings')
    pontuacao = models.PositiveSmallIntegerField(
        choices=PONTUACAO_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='ratings_artigos',
    )
    session_key = models.CharField(max_length=40, blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-data_atualizacao']
        constraints = [
            models.CheckConstraint(
                condition=Q(pontuacao__gte=1) & Q(pontuacao__lte=5),
                name='rating_pontuacao_entre_1_e_5',
            ),
            models.UniqueConstraint(
                fields=['artigo', 'user'],
                condition=Q(user__isnull=False),
                name='unique_rating_por_user_artigo',
            ),
            models.UniqueConstraint(
                fields=['artigo', 'session_key'],
                condition=Q(session_key__isnull=False) & ~Q(session_key=''),
                name='unique_rating_por_sessao_artigo',
            ),
        ]

    def __str__(self):
        if self.user:
            return f"{self.pontuacao}/5 de {self.user.username} em {self.artigo.titulo}"
        return f"{self.pontuacao}/5 anonimo em {self.artigo.titulo}"
