/*
  --------------------------------------------------------------------------------------
  Função para obter as previsões existentes do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
    let url = 'http://127.0.0.1:5000/previsoes';
    fetch(url, {
      method: 'get',
    })
      .then((response) => response.json())
      .then((data) => {
        data.previsoes.forEach(item => insertList(item.nome_praia, item.ondulacao, item.vento, item.tamanho_onda, item.data_previsao))
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }
  
  /*
    --------------------------------------------------------------------------------------
    Chamada da função para carregamento inicial dos dados
    --------------------------------------------------------------------------------------
  */
  getList()
  
  
  /*
    --------------------------------------------------------------------------------------
    Função para colocar um item na lista do servidor via requisição POST
    --------------------------------------------------------------------------------------
  */
  const postItem = async (inputPred, inputDate, inputSwell, inputWind, inputSize) => {
    const formData = new FormData();
    formData.append('nome_praia', inputPred);
    formData.append('data_previsao', inputDate);
    formData.append('ondulacao', inputSwell);
    formData.append('vento', inputWind);
    formData.append('tamanho_onda', inputSize);
  
    let url = 'http://127.0.0.1:5000/previsao';
    fetch(url, {
      method: 'post',
      body: formData
    })
      .then((response) => response.json())
      .catch((error) => {
        console.error('Error:', error);
      });
  }
  
  
  /*
    --------------------------------------------------------------------------------------
    Função para criar um botão close para cada item da lista
    --------------------------------------------------------------------------------------
  */
  const insertButton = (parent) => {
    let span = document.createElement("span");
    let txt = document.createTextNode("\u00D7");
    span.className = "close";
    span.appendChild(txt);
    parent.appendChild(span);
  }
  
  
  /*
    --------------------------------------------------------------------------------------
    Função para remover um item da lista de acordo com o click no botão close
    --------------------------------------------------------------------------------------
  */
  const removeElement = () => {
    let close = document.getElementsByClassName("close");
    // var table = document.getElementById('myTable');
    let i;
    for (i = 0; i < close.length; i++) {
      close[i].onclick = function () {
        let div = this.parentElement.parentElement;
        const nomeItem = div.getElementsByTagName('td')[0].innerHTML
        if (confirm("Você tem certeza?")) {
          div.remove()
          deleteItem(nomeItem)
          alert("Removido!")
        }
      }
    }
  }
  
  /*
    --------------------------------------------------------------------------------------
    Função para deletar um item da lista do servidor via requisição DELETE
    --------------------------------------------------------------------------------------
  */
  const deleteItem = (item) => {
    console.log(item)
    let url = 'http://127.0.0.1:5000/previsao?nome=' + item;
    fetch(url, {
      method: 'delete'
    })
      .then((response) => response.json())
      .catch((error) => {
        console.error('Error:', error);
      });
  }
  
  /*
    --------------------------------------------------------------------------------------
    Função para adicionar nova previsão com nome da praia, data, ondulação, vento e tamanho da onda 
    --------------------------------------------------------------------------------------
  */
  const newItem = () => {
    let inputPred = document.getElementById("newPlace").value;
    let inputDate = document.getElementById("newDate").value;
    let inputSwell = document.getElementById("newSwell").value;
    let inputWind = document.getElementById("newWind").value;
    let inputSize = document.getElementById("newSize").value;
  
    if (inputProduct === '') {
      alert("Adicione uma previsão");
    } else if (isNaN(inputSize) || isNaN(inputSize)) {
      alert("Tamanho da onda precisa ser em número!");
    } else {
      insertList(inputPred, inputDate, inputSwell, inputWind, inputSize)
      postItem(inputPred, inputDate, inputSwell, inputWind, inputSize)
      alert("Previsão adicionada!")
    }
  }
  
  /*
    --------------------------------------------------------------------------------------
    Função para inserir items na lista apresentada
    --------------------------------------------------------------------------------------
  */
  const insertList = (namePred, date, swell, wind, size) => {
    var item = [namePred, date, swell, wind, size]
    var table = document.getElementById('myTable');
    var row = table.insertRow();
  
    for (var i = 0; i < item.length; i++) {
      var cel = row.insertCell(i);
      cel.textContent = item[i];
    }
    insertButton(row.insertCell(-1))
    document.getElementById("newPred").value = "";
    document.getElementById("newDate").value = "";
    document.getElementById("newSwell").value = "";
    document.getElementById("newWind").value = "";
    document.getElementById("newSize").value = "";
  
    removeElement()
  }