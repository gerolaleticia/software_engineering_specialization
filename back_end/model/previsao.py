from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Interacao


class Previsao(Base):
    __tablename__ = 'previsao'

    id = Column("pk_previsao", Integer, primary_key=True)
    nome_praia = Column(String(140))
    ondulacao = Column(String(140))
    vento = Column(String(140))
    tamanho_onda = Column(Float)
    data_previsao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre a previsão do swell e a interação com os surfistas.

    interacoes = relationship("Interacao")

    def __init__(self, nome_praia:str, ondulacao:str, vento:str, 
                 tamanho_onda=float, data_previsao:Union[DateTime, None] = None):
        """
        Cria uma Previsão

        Arguments:
            nome_praia: nome da praia.
            ondulação: direção da ondulação predominante naquela data.
            vento: direção do vento predominante naquela data.
            tamanha_onda: tamanho da onda esperada em metros.
            data_previsao: data de quando a previsão de onda foi averiguada
        """
        self.nome_praia = nome_praia
        self.ondulacao = ondulacao
        self.vento = vento
        self.tamanho_onda = tamanho_onda

        # se não for informada, será utilizada a data da inserção no banco
        if data_previsao:
            self.data_previsao = data_previsao

    def adiciona_interacao(self, interacoes:Interacao):
        """ Adiciona uma nova interacao à previsão litorânea
        """
        self.interacao.append(interacoes)