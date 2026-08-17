from flask import Blueprint, render_template, request, redirect, url_for, session, flash
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


@perguntas_bp.route("/")
def listar():
    """Lista todas as perguntas cadastradas."""
    perguntas = Pergunta.query.order_by(Pergunta.data_criacao.desc()).all()
    return render_template("perguntas/listar.html", perguntas=perguntas)


@perguntas_bp.route("/<int:pergunta_id>/editar", methods=["GET", "POST"])
def editar(pergunta_id):
    """Somente o autor pode editar a própria pergunta."""
    pergunta = Pergunta.query.get_or_404(pergunta_id)

    if session.get("usuario_id") != pergunta.usuario_id:
        flash("Somente o autor pode editar esta pergunta.", "danger")
        return redirect(url_for("anuncios.detalhe", anuncio_id=pergunta.anuncio_id))

    if request.method == "POST":
        pergunta.texto = request.form["texto"]
        db.session.commit()
        flash("Pergunta atualizada!", "success")
        return redirect(url_for("anuncios.detalhe", anuncio_id=pergunta.anuncio_id))

    return render_template("perguntas/editar.html", pergunta=pergunta)


@perguntas_bp.route("/<int:pergunta_id>/excluir", methods=["GET", "POST"])
def excluir(pergunta_id):
    """O GET exibe a confirmação; o POST efetiva a exclusão."""
    pergunta = Pergunta.query.get_or_404(pergunta_id)
    usuario_id = session.get("usuario_id")

    if usuario_id not in (pergunta.usuario_id, pergunta.anuncio.usuario_id):
        flash("Você não pode excluir esta pergunta.", "danger")
        return redirect(url_for("anuncios.detalhe", anuncio_id=pergunta.anuncio_id))

    if request.method == "POST":
        anuncio_id = pergunta.anuncio_id
        db.session.delete(pergunta)
        db.session.commit()
        flash("Pergunta excluída!", "success")
        return redirect(url_for("anuncios.detalhe", anuncio_id=anuncio_id))

    return render_template(
        "confirmar_exclusao.html",
        titulo="Excluir pergunta",
        registro=pergunta.texto,
        aviso="A resposta vinculada a esta pergunta, se existir, também será excluída.",
        url_acao=url_for("perguntas.excluir", pergunta_id=pergunta.id),
        url_cancelar=url_for("anuncios.detalhe", anuncio_id=pergunta.anuncio_id),
    )


@perguntas_bp.route("/respostas")
def listar_respostas():
    """Lista todas as respostas cadastradas."""
    respostas = Resposta.query.order_by(Resposta.data_resposta.desc()).all()
    return render_template("perguntas/respostas.html", respostas=respostas)


@perguntas_bp.route("/respostas/<int:resposta_id>/editar", methods=["GET", "POST"])
def editar_resposta(resposta_id):
    """Somente o dono do anúncio pode editar a resposta."""
    resposta = Resposta.query.get_or_404(resposta_id)

    if session.get("usuario_id") != resposta.pergunta.anuncio.usuario_id:
        flash("Somente o dono do anúncio pode editar esta resposta.", "danger")
        return redirect(url_for("anuncios.detalhe", anuncio_id=resposta.pergunta.anuncio_id))

    if request.method == "POST":
        resposta.texto = request.form["texto"]
        db.session.commit()
        flash("Resposta atualizada!", "success")
        return redirect(url_for("anuncios.detalhe", anuncio_id=resposta.pergunta.anuncio_id))

    return render_template("perguntas/resposta_editar.html", resposta=resposta)


@perguntas_bp.route("/respostas/<int:resposta_id>/excluir", methods=["GET", "POST"])
def excluir_resposta(resposta_id):
    """O GET exibe a confirmação; o POST efetiva a exclusão."""
    resposta = Resposta.query.get_or_404(resposta_id)
    anuncio_id = resposta.pergunta.anuncio_id

    if session.get("usuario_id") != resposta.pergunta.anuncio.usuario_id:
        flash("Somente o dono do anúncio pode excluir esta resposta.", "danger")
        return redirect(url_for("anuncios.detalhe", anuncio_id=anuncio_id))

    if request.method == "POST":
        db.session.delete(resposta)
        db.session.commit()
        flash("Resposta excluída!", "success")
        return redirect(url_for("anuncios.detalhe", anuncio_id=anuncio_id))

    return render_template(
        "confirmar_exclusao.html",
        titulo="Excluir resposta",
        registro=resposta.texto,
        aviso="A pergunta continua cadastrada, apenas sem resposta.",
        url_acao=url_for("perguntas.excluir_resposta", resposta_id=resposta.id),
        url_cancelar=url_for("anuncios.detalhe", anuncio_id=anuncio_id),
    )
