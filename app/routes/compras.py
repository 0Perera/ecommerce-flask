from flask import Blueprint, request, redirect, url_for, session, flash
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
