from django.contrib.auth.models import User
from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .models import Artigo, Comentario, Rating
from .utils import get_bloggers_group


TEST_STORAGES = settings.STORAGES.copy()
TEST_STORAGES['staticfiles'] = {
    'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
}


@override_settings(STORAGES=TEST_STORAGES)
class InteracaoArtigoTests(TestCase):
    def setUp(self):
        self.autor = User.objects.create_user(
            username='autor',
            password='teste123',
        )
        self.visitante = User.objects.create_user(
            username='visitante',
            password='teste123',
        )
        self.artigo = Artigo.objects.create(
            titulo='Artigo de teste',
            texto='Texto do artigo',
            autor=self.autor,
        )

    def test_visitante_anonimo_consegue_comentar(self):
        response = self.client.post(
            reverse('comentar_artigo', args=[self.artigo.id]),
            {
                'nome_visitante': 'Ana',
                'texto': 'Gostei do artigo.',
            },
        )

        self.assertRedirects(
            response,
            reverse('detalhe_artigo', args=[self.artigo.id]),
        )
        comentario = Comentario.objects.get()
        self.assertIsNone(comentario.autor)
        self.assertEqual(comentario.nome_visitante, 'Ana')
        self.assertEqual(comentario.nome_autor, 'Ana')

        detalhe = self.client.get(reverse('detalhe_artigo', args=[self.artigo.id]))
        self.assertContains(detalhe, 'Ana')
        self.assertContains(detalhe, 'Gostei do artigo.')

    def test_comentario_anonimo_sem_nome_aparece_como_visitante(self):
        self.client.post(
            reverse('comentar_artigo', args=[self.artigo.id]),
            {
                'nome_visitante': '',
                'texto': 'Comentario sem nome.',
            },
        )

        comentario = Comentario.objects.get()
        self.assertEqual(comentario.nome_autor, 'Visitante')

        detalhe = self.client.get(reverse('detalhe_artigo', args=[self.artigo.id]))
        self.assertContains(detalhe, 'Visitante')
        self.assertContains(detalhe, 'Comentario sem nome.')

    def test_utilizador_autenticado_comenta_com_username(self):
        self.client.force_login(self.visitante)

        self.client.post(
            reverse('comentar_artigo', args=[self.artigo.id]),
            {'texto': 'Comentario autenticado.'},
        )

        comentario = Comentario.objects.get()
        self.assertEqual(comentario.autor, self.visitante)
        self.assertEqual(comentario.nome_visitante, '')
        self.assertEqual(comentario.nome_autor, 'visitante')

    def test_rating_anonimo_cria_sessao_e_mostra_media(self):
        response = self.client.post(
            reverse('avaliar_artigo', args=[self.artigo.id]),
            {'pontuacao': '4'},
        )

        self.assertRedirects(
            response,
            reverse('detalhe_artigo', args=[self.artigo.id]),
        )
        rating = Rating.objects.get()
        self.assertIsNone(rating.user)
        self.assertTrue(rating.session_key)
        self.assertEqual(rating.pontuacao, 4)

        detalhe = self.client.get(reverse('detalhe_artigo', args=[self.artigo.id]))
        self.assertContains(detalhe, 'Media: 4.0 / 5')
        self.assertContains(detalhe, '1 avaliacoes')

    def test_rating_repetido_da_mesma_sessao_atualiza(self):
        url = reverse('avaliar_artigo', args=[self.artigo.id])

        self.client.post(url, {'pontuacao': '5'})
        self.client.post(url, {'pontuacao': '2'})

        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(Rating.objects.get().pontuacao, 2)

    def test_media_usa_multiplas_avaliacoes(self):
        self.client.post(
            reverse('avaliar_artigo', args=[self.artigo.id]),
            {'pontuacao': '5'},
        )
        outro_cliente = Client()
        outro_cliente.post(
            reverse('avaliar_artigo', args=[self.artigo.id]),
            {'pontuacao': '3'},
        )

        self.assertEqual(Rating.objects.count(), 2)
        detalhe = self.client.get(reverse('detalhe_artigo', args=[self.artigo.id]))
        self.assertContains(detalhe, 'Media: 4.0 / 5')
        self.assertContains(detalhe, '2 avaliacoes')

    def test_rating_fora_da_escala_nao_e_guardado(self):
        self.client.post(
            reverse('avaliar_artigo', args=[self.artigo.id]),
            {'pontuacao': '6'},
        )

        self.assertEqual(Rating.objects.count(), 0)

    def test_blogger_autenticado_consegue_criar_artigo(self):
        blogger = User.objects.create_user(
            username='blogger',
            password='teste123',
        )
        blogger.groups.add(get_bloggers_group())
        self.client.force_login(blogger)

        response = self.client.post(
            reverse('criar_artigo'),
            {
                'titulo': 'Novo artigo',
                'texto': 'Conteudo do novo artigo.',
                'link_externo': '',
            },
        )

        artigo = Artigo.objects.get(titulo='Novo artigo')
        self.assertRedirects(response, reverse('detalhe_artigo', args=[artigo.id]))
        self.assertEqual(artigo.autor, blogger)

    def test_utilizador_autenticado_sem_grupo_bloggers_nao_cria_artigo(self):
        self.client.force_login(self.visitante)

        response = self.client.post(
            reverse('criar_artigo'),
            {
                'titulo': 'Artigo bloqueado',
                'texto': 'Nao deve ser criado.',
            },
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Artigo.objects.filter(titulo='Artigo bloqueado').exists())
