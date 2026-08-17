from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash
from app import db
from app.models import Usuario, Compra, Anuncio

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/")
def listar():
    """Lista todos os usuários cadastrados."""
    usuarios = Usuario.query.order_by(Usuario.nome).all()
    return render_template("usuarios/listar.html", usuarios=usuarios)


@usuarios_bp.route("/novo", methods=["GET", "POST"])
def novo():
    """Cadastro de um novo usuário."""
    if request.method == "POST":
        usuario = Usuario(
            nome=request.form["nome"],
            email=request.form["email"],
            senha_hash=generate_password_hash(request.form["senha"]),
        )
        db.session.add(usuario)
        db.session.commit()
        flash("Usuário cadastrado com sucesso!", "success")
        return redirect(url_for("usuarios.listar"))
    return render_template("usuarios/novo.html")


@usuarios_bp.route("/entrar", methods=["GET", "POST"])
def entrar():
    """
    Seletor simples de 'usuário atual' via sessão.
    Substitui um login completo nesta etapa inicial do projeto -
    a autenticação com senha/hash será implementada em uma próxima
    entrega, já que o foco aqui é a estrutura de rotas e entidades.
    """
    if request.method == "POST":
        session["usuario_id"] = int(request.form["usuario_id"])
        flash("Usuário atual alterado.", "success")
        return redirect(url_for("main.home"))
    usuarios = Usuario.query.order_by(Usuario.nome).all()
    return render_template("usuarios/entrar.html", usuarios=usuarios)


@usuarios_bp.route("/<int:usuario_id>")
def perfil(usuario_id):
    """Perfil do usuário: dados básicos e seus anúncios."""
    usuario = Usuario.query.get_or_404(usuario_id)
    anuncios = Anuncio.query.filter_by(usuario_id=usuario_id).all()
    return render_template("usuarios/perfil.html", usuario=usuario, anuncios=anuncios)


@usuarios_bp.route("/<int:usuario_id>/vendas")
def relatorio_vendas(usuario_id):
    """Relatório de vendas: todas as compras feitas nos anúncios deste usuário."""
    usuario = Usuario.query.get_or_404(usuario_id)
    vendas = (
        Compra.query.join(Anuncio)
        .filter(Anuncio.usuario_id == usuario_id)
        .order_by(Compra.data_compra.desc())
        .all()
    )
    total = sum(float(v.valor_pago) for v in vendas)
    return render_template(
        "usuarios/relatorio_vendas.html", usuario=usuario, vendas=vendas, total=total
    )


@usuarios_bp.route("/<int:usuario_id>/compras")
def relatorio_compras(usuario_id):
    """Relatório de compras: tudo que este usuário comprou."""
    usuario = Usuario.query.get_or_404(usuario_id)
    compras = (
        Compra.query.filter_by(comprador_id=usuario_id)
        .order_by(Compra.data_compra.desc())
        .all()
    )
    total = sum(float(c.valor_pago) for c in compras)
    return render_template(
        "usuarios/relatorio_compras.html", usuario=usuario, compras=compras, total=total
    )


@usuarios_bp.route("/<int:usuario_id>/editar", methods=["GET", "POST"])
def editar(usuario_id):
    """Edição dos dados de um usuário já cadastrado."""
    usuario = Usuario.query.get_or_404(usuario_id)

    if request.method == "POST":
        usuario.nome = request.form["nome"]
        usuario.email = request.form["email"]
        senha = request.form.get("senha")
        if senha:
            usuario.senha_hash = generate_password_hash(senha)
        db.session.commit()
        flash("Usuário atualizado com sucesso!", "success")
        return redirect(url_for("usuarios.perfil", usuario_id=usuario.id))

    return render_template("usuarios/editar.html", usuario=usuario)


@usuarios_bp.route("/<int:usuario_id>/excluir", methods=["GET", "POST"])
def excluir(usuario_id):
    """
    Exclusão em duas etapas: o GET mostra a tela de confirmação e
    somente o POST remove o registro do banco.
    """
    usuario = Usuario.query.get_or_404(usuario_id)

    if request.method == "POST":
        db.session.delete(usuario)
        db.session.commit()
        if session.get("usuario_id") == usuario_id:
            session.pop("usuario_id")
        flash("Usuário excluído com sucesso!", "success")
        return redirect(url_for("usuarios.listar"))

    return render_template(
        "confirmar_exclusao.html",
        titulo="Excluir usuário",
        registro=usuario.nome,
        aviso="Os anúncios, perguntas, compras e listas de favoritos deste usuário também serão excluídos.",
        url_acao=url_for("usuarios.excluir", usuario_id=usuario.id),
        url_cancelar=url_for("usuarios.perfil", usuario_id=usuario.id),
    )
