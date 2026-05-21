# Pim Pam Pum

Aplicacao web em Django desenvolvida como portfolio academico e profissional.
O projeto junta paginas de apresentacao, gestao de conteudos, artigos com
interacao de visitantes, autenticacao e integracao com servicos externos.

Este README serve tambem como mapa rapido para avaliacao e leitura assistida
por IA, para que seja possivel perceber a estrutura do projeto sem abrir todos
os ficheiros.

## Resumo

O site apresenta informacao academica, projetos, tecnologias, competencias,
formacoes, experiencias profissionais, TFCs e artigos. A aplicacao segue a
arquitetura MVT do Django:

- Models: definem entidades, campos, relacoes e regras de dados.
- Views: tratam pedidos HTTP, consultas, permissoes e formularios.
- Templates: renderizam as paginas HTML apresentadas ao utilizador.
- URLs: ligam rotas publicas as views de cada app.

## Apps Principais

### `portfolio`

App principal do portfolio. Contem a maior parte das entidades de apresentacao:

- `Licenciatura`
- `Docente`
- `UnidadeCurricular`
- `TipoTecnologia`
- `Tecnologia`
- `Projeto`
- `TFC`
- `Competencia`
- `Formacao`
- `ExperienciaProfissional`
- `MakingOf`

Tambem contem paginas publicas para listar licenciaturas, docentes, disciplinas,
tecnologias, projetos, TFCs, competencias, formacoes, experiencias e making of.

Existe CRUD para algumas entidades do portfolio, protegido por login e pelo
grupo `gestor-portfolio`.

### `artigos`

App responsavel por artigos e interacao com leitores.

Funcionalidades principais:

- listagem e detalhe de artigos;
- criacao e edicao de artigos por utilizadores do grupo `bloggers`;
- comentarios de utilizadores autenticados e visitantes;
- likes por utilizador autenticado ou por sessao anonima;
- ratings de 1 a 5 por utilizador autenticado ou por sessao anonima;
- calculo de media de ratings e total de likes.

Os modelos `Like` e `Rating` usam constraints para evitar duplicados por artigo.
Para visitantes anonimos, a identificacao e feita atraves de `session_key`.

### `accounts`

App de autenticacao e regras de utilizador.

Funcionalidades principais:

- login e logout;
- registo de utilizadores;
- magic login por email;
- integracao com Google via `django-allauth`;
- configuracao de email em base de dados;
- associacao automatica de utilizadores ao grupo `bloggers` em certos fluxos.

### `escola`

App simples com entidades academicas de apoio:

- `Professor`
- `Aluno`
- `Curso`

## Permissoes

O projeto usa grupos do Django para separar responsabilidades:

- `gestor-portfolio`: pode gerir conteudos do portfolio, como projetos,
  tecnologias, competencias e formacoes.
- `bloggers`: pode criar artigos; cada autor so pode editar os seus proprios
  artigos.

As permissoes sao aplicadas nas views com `login_required` e verificacoes
explicitas antes de criar, editar ou apagar conteudos.

## Dados E Relacoes

Exemplos de relacoes importantes:

- `Projeto` tem uma `ForeignKey` opcional para `UnidadeCurricular`.
- `Projeto` tem varias `Tecnologia` atraves de `ManyToManyField`.
- `UnidadeCurricular` relaciona-se com `Licenciatura` e `Docente`.
- `TFC` relaciona-se com `Licenciatura`, `Docente` e `Tecnologia`.
- `Competencia` relaciona-se com `Projeto` e `Formacao`.
- `Artigo` pertence a um `User`.
- `Comentario`, `Like` e `Rating` pertencem a um `Artigo`.

Foram usados `select_related` e `prefetch_related` em views de listagem para
reduzir consultas repetidas a base de dados.

## Autenticacao

O projeto suporta varios fluxos:

- autenticacao tradicional com username e password;
- registo de novo utilizador;
- login Google com `django-allauth`;
- magic login, onde o utilizador recebe um link temporario por email.

O magic login cria um token unico, associa-o a um utilizador e invalida-o depois
de ser usado. O token tambem tem uma janela de validade limitada.

## Ficheiros E Servicos Externos

O projeto usa:

- `Cloudinary` para armazenamento de media em producao;
- `WhiteNoise` para servir ficheiros estaticos em producao;
- `SQLite` em desenvolvimento/local;
- `PostgreSQL` via `DATABASE_URL` em ambiente de producao;
- variaveis de ambiente carregadas com `django-environ`.

As credenciais devem ficar em `.env` ou em secrets do ambiente de deploy, nunca
diretamente no codigo.

## Estrutura De URLs

O ficheiro `project/urls.py` inclui as rotas principais:

- `/admin/`
- `/accounts/`
- `/artigos/`
- `/portfolio/`
- `/escola/`
- `/` apontando para as rotas do portfolio

Cada app tem o seu proprio ficheiro `urls.py`, mantendo o roteamento organizado.

## Como Correr Localmente

1. Criar e ativar ambiente virtual.

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Instalar dependencias.

```bash
pip install -r requirements.txt
```

3. Criar ficheiro `.env` com as variaveis necessarias.

Exemplo minimo para desenvolvimento:

```env
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
CLOUDINARY_CLOUD_NAME=dummy-cloud
CLOUDINARY_API_KEY=dummy-key
CLOUDINARY_API_SECRET=dummy-secret
```

4. Aplicar migrations.

```bash
python manage.py migrate
```

5. Criar superutilizador, se necessario.

```bash
python manage.py createsuperuser
```

6. Iniciar servidor.

```bash
python manage.py runserver
```

## Pontos Importantes Para Defesa

Temas que podem ser perguntados numa defesa oral:

- explicar a arquitetura MVT no projeto;
- descrever a responsabilidade de cada app;
- justificar relacoes `ForeignKey` e `ManyToManyField`;
- explicar `on_delete=CASCADE`, `SET_NULL` e `PROTECT`;
- explicar como funcionam os grupos `gestor-portfolio` e `bloggers`;
- mostrar onde as permissoes sao verificadas nas views;
- explicar como visitantes anonimos conseguem comentar, gostar e avaliar;
- justificar o uso de `session_key` nos likes e ratings;
- explicar `select_related` e `prefetch_related`;
- explicar como adicionar uma nova pagina;
- explicar como adicionar um novo campo a um model e criar migration;
- explicar como funcionam static files, media files, Cloudinary e WhiteNoise;
- explicar como variaveis sensiveis sao separadas do codigo;
- explicar como testar uma view, um form ou uma regra de permissao.

## Modificacoes Praticas Provaveis

Exemplos de tarefas que podem ser pedidas durante a defesa:

- adicionar um novo campo a `Projeto` e mostra-lo no template;
- criar um filtro por tecnologia ou ano;
- adicionar pesquisa por titulo;
- alterar permissoes de criacao/edicao;
- acrescentar uma pagina nova ao menu;
- validar um formulario;
- impedir duplicacao de interacoes;
- criar ou ajustar uma migration;
- corrigir uma rota ou erro de template;
- adicionar um teste simples.

## Tecnologias

- Python
- Django
- Django Allauth
- Django Environ
- Cloudinary
- WhiteNoise
- SQLite
- PostgreSQL
- HTML
- CSS
- JavaScript

## Repositorio

Repositorio principal:

```text
https://github.com/Duarte-Verissimo/pim-pam-pum
```
