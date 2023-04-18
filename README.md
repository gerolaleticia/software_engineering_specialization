# Wave Prediction

Este projeto faz parte da entrega da sprint 1 do curso de pós graduação em **Engenharia de Software - PUC Rio** 

O objetivo da aplicação é trazer, em uma única tela interativa, as previsões de ondas do litoral paulista considerando direção da ondulação, direção do vento e o tamanho de onda esperado. A ideia é facilitar a organização e programação dos surfistas da cidade. 

---
## Como executar - back end


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5002
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5002 --reload
```

Abra o [http://localhost:5002/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

Ilustração do conteúdo front-end da aplicação Let Me Sea, construído como MVP da Sprint 1 da Pós Graduação em Engenharia de Software (PUC-RIO).

---
## Como executar - front-end

Basta fazer o download do projeto e abrir o arquivo index.html no seu browser.