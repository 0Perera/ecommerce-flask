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
