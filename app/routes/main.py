from flask import Blueprint, render_template, request
from app.models import Anuncio, Categoria

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    """Página inicial: vitrine de anúncios ativos, com filtro opcional por categoria."""
    categoria_id = request.args.get("categoria_id", type=int)

    query = Anuncio.query.filter_by(status="ativo")
    if categoria_id:
        query = query.filter_by(categoria_id=categoria_id)

    anuncios = query.order_by(Anuncio.data_criacao.desc()).all()
    categorias = Categoria.query.order_by(Categoria.nome).all()

    return render_template(
        "home.html", anuncios=anuncios, categorias=categorias, categoria_id=categoria_id
    )
