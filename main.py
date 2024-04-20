from flask import Flask, request, render_template
from funcao import AnaliseNodal

app = Flask(__name__)

dados = []
parametros = []


@app.route('/')
def formulario():
    return render_template('formulario.html', dados=dados, resultado=None, parametros=parametros)


@app.route('/processar', methods=['POST'])
def processar():
    print(request.form.keys())
    global dados, parametros
    if not parametros:
        parametros = [request.form['nos'], request.form['referencia'], request.form['nominal'],
                      request.form['tensao_nominal'], request.form['injecao'], request.form['no_injecao'],
                      request.form['valor_injecao']]
    dado = [request.form['dados'], request.form['no1'], request.form['no2']]
    if dado[0] != '0' and dado[1] != '0' and dado[1] != dado[2]:
        dados.append(dado)
    print(dados)
    print(parametros)
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
    app.run(debug=True, port=5000, host='0.0.0.0')
