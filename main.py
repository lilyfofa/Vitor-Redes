from flask import Flask, request, render_template
from funcao import AnaliseNodal
import os

app = Flask(__name__)

dados = []
parametros = []


@app.route('/')
def formulario():
    return render_template('formulario.html', dados=dados, resultado=None, parametros=parametros)


@app.route('/processar', methods=['POST'])
def processar():
    global dados, parametros
    if not parametros:
        v1 = request.form['nos']
        v2 = request.form['referencia']
        v3 = request.form['nominal']
        v4 = request.form['tensao_nominal']
        v5 = request.form['injecao']
        v6 = request.form['no_injecao']
        v7 = request.form['valor_injecao']
    v8 = request.form['dados']
    v9 = request.form['no1']
    v10 = request.form['no2']
    if v4 != '0' and v1 != '' and v2 != '' and v3 != '' and v4 != '':
        if int(v1) != 0 and int(v2) < int(v1) and int(v3) < int(v1) and int(v3) != int(v2):
            if v5 != 'nao':
                if v7 != '0' and v5 != '' and v6 != '' and v7 != '':
                    if int(v6) < int(v1) and int(v6) != int(v2) and int(v6) != int(v2):
                        parametros = [v1, v2, v3, v4, v5, v6, v7]
            else:
                parametros = [v1, v2, v3, v4, v5, v6, v7]
    if v8 != '' and v9 != '' and v9 != '':
        if int(v9) != int(v10) and int(v9) < int(v1) and int(v10) < int(v1):
            dado = [v8, v9, v10]
            dados.append(dado)
    return render_template('formulario.html', dados=dados, resultado=None, parametros=parametros)


@app.route('/limpar-parametros', methods=['POST'])
def limpar_parametros():
    global parametros
    parametros = []
    return render_template('formulario.html', dados=dados, resultado=None, parametros=parametros)


@app.route('/remover-ultimo', methods=['POST'])
def remover_ultimo():
    global dados

    if dados:
        dados.pop()

    return render_template('formulario.html', dados=dados, resultado=None, parametros=parametros)


@app.route('/remover-todos', methods=['POST'])
def remover_todos():
    global dados
    if dados:
        dados = []
    return render_template('formulario.html', dados=dados, resultado=None, parametros=parametros)


@app.route('/calcular', methods=['POST'])
def calcular():
    global dados, parametros
    if dados and parametros:
        resultado = AnaliseNodal(dados, parametros)
    else:
        resultado = ['Nenhum dado inserido!']
    return render_template('formulario.html', dados=dados, resultado=resultado, parametros=parametros)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000), host="0.0.0.0")
