from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, render_template
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Previsao
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Wave Prediction", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
previsao_tag = Tag(name="Previsao", description="Adição, visualização e remoção de previsões à base geral")
interacao_tag = Tag(name="Interacao", description="Adição de um comentário à uma previsão cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/previsao', tags=[previsao_tag],
          responses={"200": PrevisaoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_revisao(form: PrevisaoSchema):
    """Adiciona uma nova Previsão à base de dados

    Retorna uma representação das previsões e comentários associados.
    """
    previsao = Previsao(
        nome_praia=form.nome_praia,
        ondulacao=form.ondulacao,
        vento=form.vento,
        tamanho_onda=form.tamanho_onda)
    logger.debug(f"Adicionando a previsão do local: '{previsao.nome_praia}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando previsao
        session.add(previsao)
        # efetivando o camando de adição de novo registro na tabela
        session.commit()
        logger.debug(f"Adicionada previsão do local: '{previsao.nome_praia}'")
        return apresenta_previsao(previsao), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Previsão para este local já adicionada :/"
        logger.warning(f"Erro ao adicionar previsão '{previsao.nome_praia}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo registro :/"
        logger.warning(f"Erro ao adicionar previsao '{previsao.nome_praia}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/previsoes', tags=[previsao_tag],
         responses={"200": ListagemPrevisoesSchema, "404": ErrorSchema})
def get_previsoes():
    """Faz a busca por todas as previsões cadastradas

    Retorna uma representação da listagem de previsões recentes.
    """
    logger.debug(f"Coletando previsões ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    previsoes = session.query(Previsao).all()

    if not previsoes:
        # se não há previsoes cadastrados
        return {"previsões": []}, 200
    else:
        logger.debug(f"%d previsões econtradas" % len(previsoes))
        # retorna a representação da previsão
        print(previsoes)
        return apresenta_previsoes(previsoes), 200


@app.get('/previsao', tags=[previsao_tag],
         responses={"200": PrevisaoViewSchema, "404": ErrorSchema})
def get_produto(query: PrevisaoBuscaSchema):
    """Faz a busca por uma previsao a partir do id do registro

    Retorna uma representação das previsões e comentários associados.
    """
    nome_praia = query.nome_praia
    logger.debug(f"Coletando dados sobre a previsão #{nome_praia}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    previsao = session.query(Previsao).filter(Previsao.id == nome_praia).first()

    if not previsao:
        # se o produto não foi encontrado
        error_msg = "Previsao não encontrada na base :/"
        logger.warning(f"Erro ao buscar previsao '{nome_praia}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Previsão encontrada: '{previsao.nome_praia}'")
        # retorna a representação de produto
        return apresenta_previsao(previsao), 200


@app.delete('/previsao', tags=[previsao_tag],
            responses={"200": PrevisaoDelSchema, "404": ErrorSchema})
def del_previsao(query: PrevisaoBuscaSchema):
    """Deleta uma previsão a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    previsao_nome = unquote(unquote(query.nome_praia))
    print(previsao_nome)
    logger.debug(f"Deletando dados sobre a previsão #{previsao_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Previsao).filter(Previsao.nome_praia == previsao_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletada previsão #{previsao_nome}")
        return {"mesage": "Previsao removida", "id": previsao_nome}
    else:
        # se a previsao não foi encontrada
        error_msg = "Previsao não encontrada na base :/"
        logger.warning(f"Erro ao deletar previsao #'{previsao_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
