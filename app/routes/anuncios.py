from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from app.models import Anuncio, Categoria, Usuario, ListaFavoritos

anuncios_bp = Blueprint("anuncios", __name__)


@anuncios_bp.route("/")
def listar():
    """Lista todos os anúncios (independente de status), com filtro por categoria."""
    categoria_id = request.args.get("categoria_id", type=int)
    query = Anuncio.query
    if categoria_id:
        query = query.filter_by(categoria_id=categoria_id)
    anuncios = query.order_by(Anuncio.data_criacao.desc()).all()
    categorias = Categoria.query.order_by(Categoria.nome).all()
    return render_template(
        "anuncios/listar.html", anuncios=anuncios, categorias=categorias, categoria_id=categoria_id
    )


@anuncios_bp.route("/novo", methods=["GET", "POST"])
def novo():
    """Criação de anúncio pelo usuário atualmente 'logado' (sessão)."""
    usuario_id = session.get("usuario_id")
    if not usuario_id:
        flash("Selecione um usuário em 'Entrar' antes de anunciar.", "warning")
        return redirect(url_for("usuarios.entrar"))

    if request.method == "POST":
        anuncio = Anuncio(
            titulo=request.form["titulo"],
            descricao=request.form.get("descricao"),
            preco=request.form["preco"],
            categoria_id=request.form["categoria_id"],
            usuario_id=usuario_id,
        )
        db.session.add(anuncio)
        db.session.commit()
        flash("Anúncio publicado com sucesso!", "success")
        return redirect(url_for("anuncios.detalhe", anuncio_id=anuncio.id))

    categorias = Categoria.query.order_by(Categoria.nome).all()
    return render_template("anuncios/novo.html", categorias=categorias)


@anuncios_bp.route("/<int:anuncio_id>")
def detalhe(anuncio_id):
    """Página de detalhe do anúncio: informações, perguntas e respostas."""
    anuncio = Anuncio.query.get_or_404(anuncio_id)
    usuario_atual_id = session.get("usuario_id")

    minhas_listas = []
    if usuario_atual_id:
        minhas_listas = ListaFavoritos.query.filter_by(usuario_id=usuario_atual_id).all()

    return render_template(
        "anuncios/detalhe.html",
        anuncio=anuncio,
        usuario_atual_id=usuario_atual_id,
        minhas_listas=minhas_listas,
    )
