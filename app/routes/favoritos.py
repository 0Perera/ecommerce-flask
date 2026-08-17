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


@favoritos_bp.route("/<int:lista_id>/editar", methods=["GET", "POST"])
def editar(lista_id):
    lista = ListaFavoritos.query.get_or_404(lista_id)

    if request.method == "POST":
        lista.nome = request.form["nome"]
        db.session.commit()
        flash("Lista de favoritos atualizada!", "success")
        return redirect(url_for("favoritos.detalhe", lista_id=lista.id))

    return render_template("favoritos/editar.html", lista=lista)


@favoritos_bp.route("/<int:lista_id>/excluir", methods=["GET", "POST"])
def excluir(lista_id):
    """O GET exibe a confirmação; o POST efetiva a exclusão."""
    lista = ListaFavoritos.query.get_or_404(lista_id)

    if request.method == "POST":
        db.session.delete(lista)
        db.session.commit()
        flash("Lista de favoritos excluída!", "success")
        return redirect(url_for("favoritos.listar"))

    return render_template(
        "confirmar_exclusao.html",
        titulo="Excluir lista de favoritos",
        registro=lista.nome,
        aviso="Os itens da lista serão excluídos; os anúncios continuam cadastrados.",
        url_acao=url_for("favoritos.excluir", lista_id=lista.id),
        url_cancelar=url_for("favoritos.detalhe", lista_id=lista.id),
    )


@favoritos_bp.route("/itens/<int:item_id>/editar", methods=["GET", "POST"])
def editar_item(item_id):
    """Edição do item favorito: mover o anúncio para outra lista do usuário."""
    item = ItemFavorito.query.get_or_404(item_id)
    usuario_id = session.get("usuario_id")

    if request.method == "POST":
        item.lista_id = request.form["lista_id"]
        db.session.commit()
        flash("Item movido de lista!", "success")
        return redirect(url_for("favoritos.detalhe", lista_id=item.lista_id))

    listas = ListaFavoritos.query.filter_by(usuario_id=usuario_id).all()
    return render_template("favoritos/item_editar.html", item=item, listas=listas)


@favoritos_bp.route("/itens/<int:item_id>/excluir", methods=["GET", "POST"])
def excluir_item(item_id):
    """O GET exibe a confirmação; o POST efetiva a exclusão."""
    item = ItemFavorito.query.get_or_404(item_id)
    lista_id = item.lista_id

    if request.method == "POST":
        db.session.delete(item)
        db.session.commit()
        flash("Anúncio removido da lista!", "success")
        return redirect(url_for("favoritos.detalhe", lista_id=lista_id))

    return render_template(
        "confirmar_exclusao.html",
        titulo="Remover anúncio da lista",
        registro=item.anuncio.titulo,
        aviso="O anúncio continua cadastrado no sistema.",
        url_acao=url_for("favoritos.excluir_item", item_id=item.id),
        url_cancelar=url_for("favoritos.detalhe", lista_id=lista_id),
    )
