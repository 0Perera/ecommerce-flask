"""
Application factory do sistema de e-commerce.

Aqui é criada a instância do Flask, configurado o SQLAlchemy e
registrados todos os Blueprints — um por entidade do MER — além do
Blueprint 'main' que concentra a página inicial e o menu de navegação.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_object="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)

    # Importa os modelos para que o SQLAlchemy conheça as tabelas
    # antes de criar o banco (necessário para o db.create_all()).
    from app import models  # noqa: F401

    # Registro dos Blueprints — cada um concentra as rotas de uma entidade
    from app.routes.main import main_bp
    from app.routes.usuarios import usuarios_bp
    from app.routes.categorias import categorias_bp
    from app.routes.anuncios import anuncios_bp
    from app.routes.perguntas import perguntas_bp
    from app.routes.compras import compras_bp
    from app.routes.favoritos import favoritos_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
    app.register_blueprint(categorias_bp, url_prefix="/categorias")
    app.register_blueprint(anuncios_bp, url_prefix="/anuncios")
    app.register_blueprint(perguntas_bp, url_prefix="/perguntas")
    app.register_blueprint(compras_bp, url_prefix="/compras")
    app.register_blueprint(favoritos_bp, url_prefix="/favoritos")

    with app.app_context():
        db.create_all()

    return app
