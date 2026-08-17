from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Categoria

categorias_bp = Blueprint("categorias", __name__)


@categorias_bp.route("/")
def listar():
    categorias = Categoria.query.order_by(Categoria.nome).all()
    return render_template("categorias/listar.html", categorias=categorias)


@categorias_bp.route("/nova", methods=["GET", "POST"])
def nova():
    if request.method == "POST":
        categoria = Categoria(
            nome=request.form["nome"], descricao=request.form.get("descricao")
        )
        db.session.add(categoria)
        db.session.commit()
        flash("Categoria criada com sucesso!", "success")
        return redirect(url_for("categorias.listar"))
    return render_template("categorias/nova.html")


@categorias_bp.route("/<int:categoria_id>/editar", methods=["GET", "POST"])
def editar(categoria_id):
    categoria = Categoria.query.get_or_404(categoria_id)

    if request.method == "POST":
        categoria.nome = request.form["nome"]
        categoria.descricao = request.form.get("descricao")
        db.session.commit()
        flash("Categoria atualizada com sucesso!", "success")
        return redirect(url_for("categorias.listar"))

    return render_template("categorias/editar.html", categoria=categoria)


@categorias_bp.route("/<int:categoria_id>/excluir", methods=["GET", "POST"])
def excluir(categoria_id):
    """O GET exibe a confirmação; o POST efetiva a exclusão."""
    categoria = Categoria.query.get_or_404(categoria_id)

    if request.method == "POST":
        # A categoria apenas classifica os anúncios: se houver anúncios
        # vinculados a exclusão é bloqueada, em vez de apagá-los junto.
        if categoria.anuncios:
            flash("Não é possível excluir uma categoria que possui anúncios.", "danger")
            return redirect(url_for("categorias.listar"))

        db.session.delete(categoria)
        db.session.commit()
        flash("Categoria excluída com sucesso!", "success")
        return redirect(url_for("categorias.listar"))

    return render_template(
        "confirmar_exclusao.html",
        titulo="Excluir categoria",
        registro=categoria.nome,
        aviso="A exclusão é bloqueada se existirem anúncios nesta categoria.",
        url_acao=url_for("categorias.excluir", categoria_id=categoria.id),
        url_cancelar=url_for("categorias.listar"),
    )
