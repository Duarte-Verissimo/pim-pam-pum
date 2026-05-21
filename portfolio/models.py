from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


#Representa uma licenciatura
class Licenciatura(models.Model):
    nome = models.CharField(max_length=200)
    sigla = models.CharField(max_length=10)
    descricao = models.TextField(blank=True)
    objetivos = models.TextField(blank=True)
    ects_total = models.IntegerField(blank=True, null=True)
    duracao_anos = models.IntegerField(default=3)
    url_oficial = models.URLField(blank=True, null=True)
    departamento = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

#Representa um Docente
class Docente(models.Model):
    nome = models.CharField(max_length=200)
    url_pagina_lusofona = models.URLField(blank=True, null=True)
    foto = models.ImageField(upload_to='docentes/', blank=True, null=True)    

    def __str__(self):
        return self.nome


# Representa uma unidade curricular em abstrato
class UnidadeCurricular(models.Model):

    nome = models.CharField(max_length=150)
    sigla = models.CharField(max_length=20, blank=True)
    descricao = models.TextField(blank=True)
    ects = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    imagem = models.ImageField(upload_to='ucs/', blank=True, null=True)
    ano_curricular = models.IntegerField(blank=True, null=True)
    semestre = models.CharField(max_length=30, blank=True)
    objetivos = models.TextField(blank=True)
    conteudos = models.TextField(blank=True)
    bibliografia = models.TextField(blank=True)
    apresentacao = models.TextField(blank=True)
    licenciaturas = models.ManyToManyField(Licenciatura, related_name='ucs', blank=True)
    docentes = models.ManyToManyField(Docente, related_name='ucs', blank=True)

    def __str__(self):
        return self.nome

#Representa um tipo de tecnologia
class TipoTecnologia(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


#Representa uma Tecnologia
class Tecnologia(models.Model):

    nome = models.CharField(max_length=200)
    tipo = models.ForeignKey(TipoTecnologia, on_delete=models.PROTECT, related_name='tecnologias')
    descricao = models.TextField(blank=True)
    logo = models.ImageField(upload_to='tecnologias/', blank=True, null=True)
    url_oficial = models.URLField(blank=True, null=True)
    nivel_interesse = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])


    def __str__(self):
        return self.nome


# Representa um projeto
class Projeto(models.Model):
    AMBITO_CHOICES = [
        ('academico', 'Académico'),
        ('pessoal', 'Pessoal'),
        ('profissional', 'Profissional'),
        ('freelance', 'Freelance'),
        ('outro', 'Outro'),
    ]

    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    ambito = models.CharField(max_length=50, choices=AMBITO_CHOICES, default='academico')
    conceitos_aplicados = models.TextField(blank=True, null=True)
    url_github = models.URLField(blank=True, null=True)
    url_demo = models.URLField(blank=True, null=True)
    imagem = models.ImageField(upload_to='projetos/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    ano = models.IntegerField(blank=True, null=True)
    uc = models.ForeignKey(UnidadeCurricular, on_delete=models.SET_NULL, related_name='projetos', blank=True, null=True)
    tecnologias = models.ManyToManyField(Tecnologia, related_name='projetos', blank=True)

    def __str__(self):
        return self.titulo


# Representa um Trabalho Final de Curso
class TFC(models.Model):
    titulo = models.CharField(max_length=255)
    resumo = models.TextField(blank=True)
    ano = models.IntegerField(blank=True, null=True)
    imagem_url = models.URLField(blank=True, null=True)
    pdf_url = models.URLField(blank=True, null=True)
    nivel_interesse = models.IntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    parceiro = models.CharField(max_length=200, blank=True, null=True)
    palavras_chave = models.TextField(blank=True)
    areas = models.TextField(blank=True)

    # Relações
    orientadores = models.ManyToManyField(Docente, related_name='tfcs_orientados', blank=True)
    licenciatura = models.ForeignKey(Licenciatura, on_delete=models.SET_NULL, null=True, blank=True)
    tecnologias = models.ManyToManyField(Tecnologia, related_name='tfcs', blank=True)

    def __str__(self):
        return self.titulo


# Representa uma competência
class Competencia(models.Model):
    nome = models.CharField(max_length=200)
    categoria =  models.CharField(max_length=100, blank=True) 
    descricao = models.TextField(blank=True, null=True)
    nivel = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    projetos = models.ManyToManyField('Projeto', related_name='competencias', blank=True)
    formacoes = models.ManyToManyField('Formacao', related_name='competencias', blank=True)

    def __str__(self):
        return self.nome

# Representa uma formação académica ou certificação
class Formacao(models.Model):
    TIPO_CHOICES = [
        ('Mestrado', 'Mestrado'),
        ('Curso de Curta Duração', 'Curso de Curta Duração'),
        ('Workshop', 'Workshop'),
    ]

    titulo = models.CharField(max_length=200)
    instituicao = models.CharField(max_length=200)
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)
    certificado = models.ImageField(upload_to='certificados/', blank=True, null=True)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)

    def __str__(self):
        return f"{self.titulo} - {self.instituicao}"

# Representa uma experiência profissional
class ExperienciaProfissional(models.Model):
    TIPO_CHOICES = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Estágio', 'Estágio'),
    ]

    empresa = models.CharField(max_length=200)
    cargo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    descricao = models.TextField(blank=True, null=True)
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)
    tecnologias = models.ManyToManyField(Tecnologia, related_name='experiencias', blank=True)
    competencias = models.ManyToManyField(Competencia, related_name='experiencias', blank=True)

    def __str__(self):
        return f"{self.cargo} - {self.empresa}"


# Representa o Making Of
class MakingOf(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    decisoes = models.TextField(blank=True, null=True)
    erros_correcoes = models.TextField(blank=True, null=True)
    data_registo = models.DateTimeField(auto_now_add=True)
    entidade_referida = models.CharField(max_length=200, blank=True)
    foto_papel = models.ImageField(upload_to='making_of/', blank=True, null=True)
    uso_ia = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titulo


