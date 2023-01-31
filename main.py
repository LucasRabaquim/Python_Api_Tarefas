from flask import Flask, jsonify, request, session, url_for, redirect
import json
import copy

# Id do usuário, o mesmo que está na tarefa que ele criou.
idUsuario = None

app = Flask(__name__)

# Chave de Api visível apenas para finalidade de estudo
app.secret_key = b'1457388d76a3fd5b516cee1af0732442d465f32223f0e14258e1b05e2d320e4f'
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["username"] = request.form["username"]
        idUsuario = session["username"]
        return "logado"
    return """
        <form method="post">
            <p>Usuario: <input type=text name=username>
            <p>Entrar <input type=submit value=Login>
        </form>
    """

@app.route("/logout")
def logout():
    session.pop("username", None)
    idUsuario = None
    return redirect(url_for("index"))

jsonFile = open("./data.json")
listaTarefa = json.loads(jsonFile.read())

@app.route("/")
def index():
    if "username" in session:
        return f'Você logou como: {session["username"]} = {idUsuario}'
    return "Você não está logado(a)"

@app.route("/tarefa", methods=["GET"])
def select_all():
    listaTarefaShow = copy.deepcopy(listaTarefa)
    for tarefa in listaTarefaShow:
        del tarefa["userId"]
    return jsonify(listaTarefaShow)

@app.route("/tarefa/<int:id>", methods=["GET"])
def select_tarefa_by_id(id):
    listaTarefaShow = copy.deepcopy(listaTarefa)
    for tarefa in listaTarefaShow:
        if tarefa.get("id") == id:
            del tarefa["userId"]
            return jsonify(tarefa)
    return "Tarefa não encontrada"

@app.route("/tarefa/<int:id>", methods=["PUT"])
def update_tarefa_by_id(id):
    tarefaUpdate = request.get_json()
    for index, tarefa in enumerate(listaTarefa):
        if tarefa.get("id") == id:
            if tarefa.get("userId") == idUsuario:
                listaTarefa[index].update(tarefaUpdate)
                return jsonify(listaTarefa[index])
            return "Acesso Negado"
    return "Tarefa não encontrada"

@app.route("/tarefa", methods=["POST"])
def insert_tarefa():
    tarefaInsert = request.get_json()
    listaTarefa.append(tarefaInsert)
    return jsonify(listaTarefa)

@app.route("/tarefa/<int:id>", methods=["DELETE"])
def delete_tarefa_by_id(id):

    for index, tarefa in enumerate(listaTarefa):
        if tarefa.get("id") == id:
            if tarefa.get("userId") == idUsuario:
                del listaTarefa[index]
                return "Deletado"
            return "Acesso Negado"
    return "Tarefa não encontrada"

app.run(port=5000, host="localhost", debug=True)