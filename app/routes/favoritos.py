from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from app.models import ListaFavoritos, ItemFavorito, Anuncio

favoritos_bp = Blueprint("favoritos", __name__)


@favoritos_bp.route("/")
def listar():
    """Lista as listas de favoritos do usuário atualmente na sessão."""
    usuario_id = session.get("usuario_id")
    if not usuario_id:
        flash("Selecione um usuário em 'Entrar' para ver seus favoritos.", "warning")
        return redirect(url_for("usuarios.entrar"))

    listas = ListaFavoritos.query.filter_by(usuario_id=usuario_id).all()
    return render_template("favoritos/listar.html", listas=listas)


@favoritos_bp.route("/nova", methods=["GET", "POST"])
def nova():
    usuario_id = session.get("usuario_id")
    if not usuario_id:
        flash("Selecione um usuário em 'Entrar' antes de criar uma lista.", "warning")
        return redirect(url_for("usuarios.entrar"))

    if request.method == "POST":
        lista = ListaFavoritos(nome=request.form["nome"], usuario_id=usuario_id)
        db.session.add(lista)
        db.session.commit()
        flash("Lista de favoritos criada!", "success")
        return redirect(url_for("favoritos.listar"))
    return render_template("favoritos/nova.html")


@favoritos_bp.route("/<int:lista_id>")
def detalhe(lista_id):
    lista = ListaFavoritos.query.get_or_404(lista_id)
    return render_template("favoritos/detalhe.html", lista=lista)


@favoritos_bp.route("/<int:lista_id>/adicionar", methods=["POST"])
def adicionar_item(lista_id):
    """Adiciona um anúncio a uma lista de favoritos (associação N:N)."""
    anuncio_id = request.form["anuncio_id"]

    ja_existe = ItemFavorito.query.filter_by(
        lista_id=lista_id, anuncio_id=anuncio_id
    ).first()
    if not ja_existe:
        item = ItemFavorito(lista_id=lista_id, anuncio_id=anuncio_id)
        db.session.add(item)
        db.session.commit()
        flash("Anúncio adicionado aos favoritos!", "success")
    else:
        flash("Este anúncio já está nesta lista.", "warning")

    return redirect(url_for("anuncios.detalhe", anuncio_id=anuncio_id))
