from flask import Flask, request, send_from_directory, render_template
from sqlalchemy.exc import IntegrityError

from model import Session, Previsao
from model.interacao import Interacao


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html"), 200


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/x-icon')


@app.route('/add_previsao', methods=['POST'])
def add_previsao():
    session = Session()
    previsao = Previsao(
        nome_praia=request.form.get("nome_praia"),
        ondulacao=request.form.get("ondulacao"),
        vento=request.form.get("vento"),
        tamanho_onda=request.form.get("tamanho_onda"),
    )
    try:
        # adicionando previsão
        session.add(previsao)
        # efetivando o camando de adição de nova previsão de onda na tabela
        session.commit()
        return render_template("previsao.html", previsao=previsao), 200
    except IntegrityError as e:
        error_msg = "Previsão já registrada na base"
        return render_template("error.html", error_code=409, error_msg=error_msg), 409
    except Exception as e:
        error_msg = "Não foi possível registrar nova previsão"
        print(str(e))
        return render_template("error.html", error_code=400, error_msg=error_msg), 400


@app.route('/get_previsao/<previsao_id>', methods=['GET'])
def get_previsao(previsao_id):
    session = Session()
    previsao = session.query(Previsao).filter(Previsao.id == previsao_id).first()
    if not previsao:
        error_msg = "Previsão não registrada na base :/"
        return render_template("error.html", error_code= 404, error_msg=error_msg), 404
    else:
        return render_template("previsao.html", previsao=previsao), 200


@app.route('/del_previsao/<previsao_id>', methods=['DELETE'])
def del_previsao(previsao_id):
    session = Session()
    count = session.query(Previsao).filter(Previsao.id == previsao_id).delete()
    session.commit()
    if count ==1:
        return render_template("deletado.html", previsao_id=previsao_id), 200
    else: 
        error_msg = "Previsão não registrada na base :/"
        return render_template("error.html", error_code=404, error_msg=error_msg), 404


@app.route('/add_interacao/<previsao_id>', methods=['POST'])
def add_interacao(previsao_id):
    session = Session()
    previsao = session.query(Previsao).filter(Previsao.id == previsao_id).first()
    if not previsao:
        error_msg = "Previsão não registrada na base :/"
        return render_template("error.html", error_code= 404, error_msg=error_msg), 404

    autor = request.form.get("autor")
    texto = request.form.get("texto")
    n_estrelas = request.form.get("n_estrela")
    if n_estrelas:
        n_estrelas = int(n_estrelas)

    interacao = Interacao(autor, texto, n_estrelas)
    previsao.adiciona_interacao(interacao)
    session.commit()
    return render_template("previsao.html", previsao=previsao), 200
