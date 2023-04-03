from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base


class Interacao(Base):
    __tablename__ = 'interacoes'

    id = Column(Integer, primary_key=True)
    texto = Column(String(4000))
    autor = Column(String(400))
    data_previsao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre as interações e uma previsão.
    # Aqui está sendo definido a coluna 'previsão' que vai guardar
    # a referencia à previsão registrada, a chave estrangeira que relaciona
    # uma previsão em data e praia específica à sua interação.
    previsao = Column(Integer, ForeignKey("previsao.pk_previsao"), nullable=False)

    def __init__(self, autor:str, texto:str, data_previsao:Union[DateTime, None] = None):
        """
        Cria uma Interacao

        Arguments:
            texto: o texto de uma interação.
            data_previsao: data de quando a previsão foi registrada ou inserida na base.
        """
        self.autor = autor
        self.texto = texto
        if data_previsao:
            self.previsao = data_previsao
