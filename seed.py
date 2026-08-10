"""
Script opcional para popular o banco com dados de exemplo,
facilitando a demonstração de todas as funcionalidades
(usuários, categorias, anúncios, perguntas, respostas, compras
e favoritos) logo após clonar o repositório.

Uso:
    python seed.py
"""
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import (
    Usuario, Categoria, Anuncio, Pergunta, Resposta, Compra,
    ListaFavoritos, ItemFavorito,
)

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    ana = Usuario(nome="Ana Silva", email="ana@example.com", senha_hash=generate_password_hash("123456"))
    bruno = Usuario(nome="Bruno Costa", email="bruno@example.com", senha_hash=generate_password_hash("123456"))
    db.session.add_all([ana, bruno])
    db.session.commit()

    eletronicos = Categoria(nome="Eletrônicos", descricao="Celulares, notebooks e acessórios")
    livros = Categoria(nome="Livros", descricao="Livros novos e usados")
    db.session.add_all([eletronicos, livros])
    db.session.commit()

    anuncio1 = Anuncio(
        titulo="Notebook Gamer 16GB RAM",
        descricao="Pouco uso, com nota fiscal e garantia.",
        preco=3200.00,
        usuario_id=ana.id,
        categoria_id=eletronicos.id,
    )
    anuncio2 = Anuncio(
        titulo="Coleção Senhor dos Anéis",
        descricao="Box com os 3 livros, capa dura.",
        preco=150.00,
        usuario_id=bruno.id,
        categoria_id=livros.id,
    )
    db.session.add_all([anuncio1, anuncio2])
    db.session.commit()

    pergunta1 = Pergunta(texto="Ainda tem garantia de fábrica?", anuncio_id=anuncio1.id, usuario_id=bruno.id)
    db.session.add(pergunta1)
    db.session.commit()

    resposta1 = Resposta(texto="Sim, garantia até dezembro de 2026.", pergunta_id=pergunta1.id)
    db.session.add(resposta1)
    db.session.commit()

    lista = ListaFavoritos(nome="Quero comprar depois", usuario_id=bruno.id)
    db.session.add(lista)
    db.session.commit()

    item = ItemFavorito(lista_id=lista.id, anuncio_id=anuncio1.id)
    db.session.add(item)
    db.session.commit()

    print("Banco populado com dados de exemplo!")
    print("Usuários: ana@example.com / bruno@example.com (senha: 123456)")
