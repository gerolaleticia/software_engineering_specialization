from pydantic import BaseModel


class InteracaoSchema(BaseModel):
    """ Define como um nova interação a ser inserida deve ser representada
    """
    previsao_id: int = 1
    texto: str = "Checar as condições de correnteza quando chegar ao local!"