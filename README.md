# Plataforma de E-commerce &mdash; Projeto Flask

Projeto acadêmico da disciplina de desenvolvimento de software com Flask.
O sistema implementa o **CRUD completo das oito entidades do MER** —
usuários, categorias, anúncios, perguntas, respostas, compras, listas de
favoritos e itens de favoritos —, com listagem, cadastro, edição e
exclusão com confirmação para cada uma delas.

O acesso é feito selecionando o usuário ativo em `/usuarios/entrar`, sem
verificação de senha nesta etapa.

## Requisitos do sistema (recapitulando o enunciado)

- Usuários podem anunciar e comprar produtos;
- Cada usuário possui vários anúncios;
- Anúncios são organizados em categorias;
- Usuários podem perguntar em anúncios; o dono do anúncio responde;
- Compra é feita por anúncio, sem carrinho de compras;
- Usuários podem criar listas de anúncios favoritos;
- Usuários podem consultar relatório de vendas e de compras.

## Estrutura de pastas

```
ecommerce_flask/
├── app/
│   ├── __init__.py        # application factory, registra os Blueprints
│   ├── models.py          # entidades do MER (SQLAlchemy)
│   ├── routes/
│   │   ├── main.py        # página inicial (vitrine de anúncios)
│   │   ├── usuarios.py    # cadastro, perfil, sessão, relatórios
│   │   ├── categorias.py
│   │   ├── anuncios.py
│   │   ├── perguntas.py
│   │   ├── compras.py
│   │   └── favoritos.py
│   ├── templates/         # Jinja2 (base.html contém o menu de navegação)
│   └── static/css/style.css
├── config.py
├── run.py
├── seed.py                 # popula o banco com dados de exemplo
├── requirements.txt
└── README.md
```

## Como rodar localmente

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# (opcional, mas recomendado para testar todas as telas já com dados)
python seed.py

python run.py
```

Acesse **http://localhost:5000**.

> O banco usado nesta etapa é SQLite (arquivo `ecommerce.db`, criado
> automaticamente). Isso evita dependências externas para rodar o
> projeto — a troca para PostgreSQL/MySQL em produção é só trocar a
> variável de ambiente `DATABASE_URL`.

## Como funciona a exclusão

A exclusão acontece em duas etapas: o `GET` em `/<entidade>/<id>/excluir`
apenas exibe a tela de confirmação, identificando o registro e avisando o
efeito da operação; a remoção só ocorre no `POST` enviado pelo botão de
confirmação.

Nos relacionamentos em que o dependente não existe sozinho a exclusão é
em cascata: excluir um anúncio remove suas perguntas, respostas, compras
e itens de favoritos; excluir uma pergunta remove a resposta; excluir uma
lista remove seus itens, sem afetar os anúncios. Já a categoria apenas
classifica os anúncios, então a exclusão de uma categoria com anúncios
vinculados é bloqueada.

## Mapa de rotas por entidade

| Entidade | Rota | Método | Descrição |
|---|---|---|---|
| Usuário | `/usuarios/` | GET | Lista usuários |
| Usuário | `/usuarios/novo` | GET/POST | Cadastro |
| Usuário | `/usuarios/entrar` | GET/POST | Seleciona o "usuário atual" (sessão) |
| Usuário | `/usuarios/<id>` | GET | Perfil + anúncios do usuário |
| Usuário | `/usuarios/<id>/editar` | GET/POST | Edita nome, e-mail e senha |
| Usuário | `/usuarios/<id>/excluir` | GET/POST | Confirma e exclui o usuário |
| Usuário | `/usuarios/<id>/vendas` | GET | Relatório de vendas |
| Usuário | `/usuarios/<id>/compras` | GET | Relatório de compras |
| Categoria | `/categorias/` | GET | Lista categorias |
| Categoria | `/categorias/nova` | GET/POST | Cria categoria |
| Categoria | `/categorias/<id>/editar` | GET/POST | Edita nome e descrição |
| Categoria | `/categorias/<id>/excluir` | GET/POST | Confirma e exclui (bloqueado se houver anúncios) |
| Anúncio | `/` | GET | Vitrine (home) |
| Anúncio | `/anuncios/` | GET | Lista todos os anúncios |
| Anúncio | `/anuncios/novo` | GET/POST | Cria anúncio |
| Anúncio | `/anuncios/<id>` | GET | Detalhe (perguntas, comprar, favoritar) |
| Anúncio | `/anuncios/<id>/editar` | GET/POST | Edita o anúncio (só o dono) |
| Anúncio | `/anuncios/<id>/excluir` | GET/POST | Confirma e exclui (só o dono) |
| Pergunta | `/perguntas/` | GET | Lista todas as perguntas |
| Pergunta | `/perguntas/nova` | POST | Cria pergunta em um anúncio |
| Pergunta | `/perguntas/<id>/editar` | GET/POST | Edita a pergunta (só o autor) |
| Pergunta | `/perguntas/<id>/excluir` | GET/POST | Confirma e exclui (autor ou dono do anúncio) |
| Resposta | `/perguntas/<id>/responder` | POST | Dono do anúncio responde |
| Resposta | `/perguntas/respostas` | GET | Lista todas as respostas |
| Resposta | `/perguntas/respostas/<id>/editar` | GET/POST | Edita a resposta (só o dono do anúncio) |
| Resposta | `/perguntas/respostas/<id>/excluir` | GET/POST | Confirma e exclui a resposta |
| Compra | `/compras/` | GET | Lista todas as compras |
| Compra | `/compras/nova` | POST | Registra a compra de um anúncio |
| Compra | `/compras/<id>/editar` | GET/POST | Edita o valor pago (só o comprador) |
| Compra | `/compras/<id>/excluir` | GET/POST | Confirma, exclui e reabre o anúncio |
| Lista de favoritos | `/favoritos/` | GET | Lista as listas do usuário atual |
| Lista de favoritos | `/favoritos/nova` | GET/POST | Cria lista |
| Lista de favoritos | `/favoritos/<id>` | GET | Vê itens da lista |
| Lista de favoritos | `/favoritos/<id>/editar` | GET/POST | Renomeia a lista |
| Lista de favoritos | `/favoritos/<id>/excluir` | GET/POST | Confirma e exclui a lista e seus itens |
| Item favorito | `/favoritos/<lista_id>/adicionar` | POST | Adiciona anúncio à lista |
| Item favorito | `/favoritos/itens/<id>/editar` | GET/POST | Move o anúncio para outra lista |
| Item favorito | `/favoritos/itens/<id>/excluir` | GET/POST | Remove o anúncio da lista |
