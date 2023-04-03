from pydantic import BaseModel
from typing import Optional, List
from model.previsao import Previsao

from schemas import InteracaoSchema


class PrevisaoSchema(BaseModel):
    """ Define como uma nova previsão a ser inserida deve ser representada
    """
    nome_praia: str = "Maresias"
    data_previsao: str = '04-03-2022'
    ondulacao: str = 'sul'
    vento: str = 'leste'
    tamanho_onda: float = 1.5


class PrevisaoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca, que será feita apenas com o nome da praia
    """
    nome: str = "Teste"


class ListagemPrevisoesSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    previsoes:List[PrevisaoSchema]


def apresenta_previsoes(previsoes: List[Previsao]):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    result = []
    for previsao in previsoes:
        result.append({
            "nome da praia": previsao.nome_praia,
            "data_previsao": previsao.data_previsao,
            "ondulação": previsao.ondulacao,
            "vento": previsao.vento,
            "tamanho da onda": previsao.tamanho_onda,
        })

    return {"previsoes": result}


class PrevisaoViewSchema(BaseModel):
    """ Define como uma previsão será retornada: previsão + comentário.
    """
    previsao_id: int = 1
    nome_praia: Optional[int] = 12
    data_previsao: Optional[int] = 12
    ondulacao: Optional[int] = 12
    vento: Optional[int] = 12
    tamanho_onda: Optional[float] 
    total_cometarios: int = 1
    comentarios:List[InteracaoSchema]


class PrevisaoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_previsao(previsao: Previsao):
    """ Retorna uma representação da previsao seguindo o schema definido em
        PrevisaoViewSchema.
    """
    return {
        "id": previsao.id,
        "nome da praia": previsao.nome_praia,
        "data_previsao": previsao.data_previsao,
        "ondulacao": previsao.ondulacao,
        "vento": previsao.vento,
        "tamanho_onda": previsao.tamanho_onda,
        "total_interacoes": len(previsao.interacoes),
        "interacoes": [{"texto": c.texto} for c in previsao.interacoes]
    }
