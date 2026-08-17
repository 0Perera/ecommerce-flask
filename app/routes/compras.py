from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from app.models import Compra, Anuncio

compras_bp = Blueprint("compras", __name__)


@compras_bp.route("/nova", methods=["POST"])
def nova():
    """
    Registra a compra de UM anúncio por vez (não existe carrinho de compras).
    Ao ser comprado, o anúncio muda de status para 'vendido'.
    """
    usuario_id = session.get("usuario_id")
    if not usuario_id:
        flash("Selecione um usuário em 'Entrar' antes de comprar.", "warning")
        return redirect(url_for("usuarios.entrar"))

    anuncio_id = request.form["anuncio_id"]
    anuncio = Anuncio.query.get_or_404(anuncio_id)

    if anuncio.status != "ativo":
        flash("Este anúncio não está mais disponível para compra.", "danger")
        return redirect(url_for("anuncios.detalhe", anuncio_id=anuncio_id))

    if anuncio.usuario_id == usuario_id:
        flash("Você não pode comprar o seu próprio anúncio.", "danger")
        return redirect(url_for("anuncios.detalhe", anuncio_id=anuncio_id))

    compra = Compra(anuncio_id=anuncio_id, comprador_id=usuario_id, valor_pago=anuncio.preco)
    anuncio.status = "vendido"
    db.session.add(compra)
    db.session.commit()

    flash("Compra realizada com sucesso!", "success")
    return redirect(url_for("usuarios.relatorio_compras", usuario_id=usuario_id))


@compras_bp.route("/")
def listar():
    """Lista todas as compras registradas."""
    compras = Compra.query.order_by(Compra.data_compra.desc()).all()
    return render_template("compras/listar.html", compras=compras)


@compras_bp.route("/<int:compra_id>/editar", methods=["GET", "POST"])
def editar(compra_id):
    """
    Somente o comprador pode editar a compra, e apenas o valor pago:
    trocar o anúncio de uma compra já registrada reescreveria o histórico.
    """
    compra = Compra.query.get_or_404(compra_id)

    if session.get("usuario_id") != compra.comprador_id:
        flash("Somente o comprador pode editar esta compra.", "danger")
        return redirect(url_for("compras.listar"))

    if request.method == "POST":
        compra.valor_pago = request.form["valor_pago"]
        db.session.commit()
        flash("Compra atualizada com sucesso!", "success")
        return redirect(url_for("compras.listar"))

    return render_template("compras/editar.html", compra=compra)


@compras_bp.route("/<int:compra_id>/excluir", methods=["GET", "POST"])
def excluir(compra_id):
    """O GET exibe a confirmação; o POST efetiva a exclusão."""
    compra = Compra.query.get_or_404(compra_id)

    if session.get("usuario_id") != compra.comprador_id:
        flash("Somente o comprador pode excluir esta compra.", "danger")
        return redirect(url_for("compras.listar"))

    if request.method == "POST":
        # Cancelada a compra, o anúncio volta a ficar disponível
        compra.anuncio.status = "ativo"
        db.session.delete(compra)
        db.session.commit()
        flash("Compra excluída e anúncio reaberto!", "success")
        return redirect(url_for("compras.listar"))

    return render_template(
        "confirmar_exclusao.html",
        titulo="Excluir compra",
        registro="Compra do anúncio " + compra.anuncio.titulo,
        aviso="O anúncio voltará ao status ativo e poderá ser comprado novamente.",
        url_acao=url_for("compras.excluir", compra_id=compra.id),
        url_cancelar=url_for("compras.listar"),
    )
