from flask import Blueprint, request, redirect, url_for, session, flash
from app import db
from app.models import Pergunta, Resposta, Anuncio

perguntas_bp = Blueprint("perguntas", __name__)


@perguntas_bp.route("/nova", methods=["POST"])
def nova():
    """Qualquer usuário logado pode perguntar em um anúncio de outro usuário."""
    usuario_id = session.get("usuario_id")
    if not usuario_id:
        flash("Selecione um usuário em 'Entrar' antes de perguntar.", "warning")
        return redirect(url_for("usuarios.entrar"))

    anuncio_id = request.form["anuncio_id"]
    pergunta = Pergunta(
        texto=request.form["texto"], anuncio_id=anuncio_id, usuario_id=usuario_id
    )
    db.session.add(pergunta)
    db.session.commit()
    flash("Pergunta enviada!", "success")
    return redirect(url_for("anuncios.detalhe", anuncio_id=anuncio_id))


@perguntas_bp.route("/<int:pergunta_id>/responder", methods=["POST"])
def responder(pergunta_id):
    """Apenas o dono do anúncio pode responder a pergunta."""
    pergunta = Pergunta.query.get_or_404(pergunta_id)
    usuario_id = session.get("usuario_id")

    if usuario_id != pergunta.anuncio.usuario_id:
        flash("Somente o dono do anúncio pode responder esta pergunta.", "danger")
        return redirect(url_for("anuncios.detalhe", anuncio_id=pergunta.anuncio_id))

    resposta = Resposta(texto=request.form["texto"], pergunta_id=pergunta.id)
    db.session.add(resposta)
    db.session.commit()
    flash("Resposta enviada!", "success")
    return redirect(url_for("anuncios.detalhe", anuncio_id=pergunta.anuncio_id))
