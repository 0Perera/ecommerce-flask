# Plataforma de E-commerce &mdash; Projeto Flask (entrega inicial)

Projeto acadêmico da disciplina de desenvolvimento de software com Flask.
Esta entrega contém a **estrutura inicial** do sistema: modelos (entidades
do MER), rotas para cada entidade e o menu de navegação implementado.
Regras de negócio mais avançadas (autenticação completa, permissões,
paginação, validações de formulário, etc.) ficam para as próximas etapas.

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

## Mapa de rotas por entidade

| Entidade | Rota | Método | Descrição |
|---|---|---|---|
| Usuário | `/usuarios/` | GET | Lista usuários |
| Usuário | `/usuarios/novo` | GET/POST | Cadastro |
| Usuário | `/usuarios/entrar` | GET/POST | Seleciona o "usuário atual" (sessão) |
| Usuário | `/usuarios/<id>` | GET | Perfil + anúncios do usuário |
| Usuário | `/usuarios/<id>/vendas` | GET | Relatório de vendas |
| Usuário | `/usuarios/<id>/compras` | GET | Relatório de compras |
| Categoria | `/categorias/` | GET | Lista categorias |
| Categoria | `/categorias/nova` | GET/POST | Cria categoria |
| Anúncio | `/` | GET | Vitrine (home) |
| Anúncio | `/anuncios/` | GET | Lista todos os anúncios |
| Anúncio | `/anuncios/novo` | GET/POST | Cria anúncio |
| Anúncio | `/anuncios/<id>` | GET | Detalhe (perguntas, comprar, favoritar) |
| Pergunta | `/perguntas/nova` | POST | Cria pergunta em um anúncio |
| Pergunta | `/perguntas/<id>/responder` | POST | Dono do anúncio responde |
| Compra | `/compras/nova` | POST | Registra a compra de um anúncio |
| Lista de favoritos | `/favoritos/` | GET | Lista as listas do usuário atual |
| Lista de favoritos | `/favoritos/nova` | GET/POST | Cria lista |
| Lista de favoritos | `/favoritos/<id>` | GET | Vê itens da lista |
| Item favorito | `/favoritos/<lista_id>/adicionar` | POST | Adiciona anúncio à lista |
