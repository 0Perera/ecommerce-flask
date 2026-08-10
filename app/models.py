"""
Modelos (entidades) do sistema de e-commerce.

Cada classe abaixo representa uma entidade do MER e é mapeada para uma
tabela no banco via SQLAlchemy. Os relacionamentos (db.relationship)
espelham exatamente as associações definidas no Modelo
Entidade-Relacionamento entregue junto com este projeto.
"""
from datetime import datetime
from app import db


class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    # Um usuário pode ter vários anúncios (como anunciante)
    anuncios = db.relationship(
        "Anuncio", back_populates="anunciante", foreign_keys="Anuncio.usuario_id"
    )
    # Um usuário pode fazer várias perguntas
    perguntas = db.relationship("Pergunta", back_populates="autor")
    # Um usuário pode realizar várias compras
    compras = db.relationship("Compra", back_populates="comprador")
    # Um usuário pode criar várias listas de favoritos
    listas_favoritos = db.relationship("ListaFavoritos", back_populates="usuario")

    def __repr__(self):
        return f"<Usuario {self.id} {self.nome}>"


class Categoria(db.Model):
    __tablename__ = "categoria"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    descricao = db.Column(db.String(255))

    anuncios = db.relationship("Anuncio", back_populates="categoria")

    def __repr__(self):
        return f"<Categoria {self.id} {self.nome}>"


class Anuncio(db.Model):
    __tablename__ = "anuncio"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default="ativo")  # ativo | vendido | inativo
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)

    anunciante = db.relationship(
        "Usuario", back_populates="anuncios", foreign_keys=[usuario_id]
    )
    categoria = db.relationship("Categoria", back_populates="anuncios")
    perguntas = db.relationship("Pergunta", back_populates="anuncio")
    compras = db.relationship("Compra", back_populates="anuncio")
    itens_favoritos = db.relationship("ItemFavorito", back_populates="anuncio")

    def __repr__(self):
        return f"<Anuncio {self.id} {self.titulo}>"


class Pergunta(db.Model):
    __tablename__ = "pergunta"

    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    anuncio_id = db.Column(db.Integer, db.ForeignKey("anuncio.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    anuncio = db.relationship("Anuncio", back_populates="perguntas")
    autor = db.relationship("Usuario", back_populates="perguntas")
    # 1:1 -> cada pergunta tem no máximo uma resposta
    resposta = db.relationship(
        "Resposta", back_populates="pergunta", uselist=False
    )

    def __repr__(self):
        return f"<Pergunta {self.id}>"


class Resposta(db.Model):
    __tablename__ = "resposta"

    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    data_resposta = db.Column(db.DateTime, default=datetime.utcnow)

    pergunta_id = db.Column(
        db.Integer, db.ForeignKey("pergunta.id"), unique=True, nullable=False
    )

    pergunta = db.relationship("Pergunta", back_populates="resposta")

    def __repr__(self):
        return f"<Resposta {self.id}>"


class Compra(db.Model):
    __tablename__ = "compra"

    id = db.Column(db.Integer, primary_key=True)
    data_compra = db.Column(db.DateTime, default=datetime.utcnow)
    valor_pago = db.Column(db.Numeric(10, 2), nullable=False)

    anuncio_id = db.Column(db.Integer, db.ForeignKey("anuncio.id"), nullable=False)
    comprador_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    anuncio = db.relationship("Anuncio", back_populates="compras")
    comprador = db.relationship("Usuario", back_populates="compras")

    def __repr__(self):
        return f"<Compra {self.id}>"


class ListaFavoritos(db.Model):
    __tablename__ = "lista_favoritos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    usuario = db.relationship("Usuario", back_populates="listas_favoritos")
    itens = db.relationship("ItemFavorito", back_populates="lista")

    def __repr__(self):
        return f"<ListaFavoritos {self.id} {self.nome}>"


class ItemFavorito(db.Model):
    """Entidade associativa N:N entre ListaFavoritos e Anuncio."""
    __tablename__ = "item_favorito"

    id = db.Column(db.Integer, primary_key=True)
    data_adicao = db.Column(db.DateTime, default=datetime.utcnow)

    lista_id = db.Column(
        db.Integer, db.ForeignKey("lista_favoritos.id"), nullable=False
    )
    anuncio_id = db.Column(db.Integer, db.ForeignKey("anuncio.id"), nullable=False)

    lista = db.relationship("ListaFavoritos", back_populates="itens")
    anuncio = db.relationship("Anuncio", back_populates="itens_favoritos")

    __table_args__ = (
        db.UniqueConstraint("lista_id", "anuncio_id", name="uq_lista_anuncio"),
    )

    def __repr__(self):
        return f"<ItemFavorito lista={self.lista_id} anuncio={self.anuncio_id}>"
