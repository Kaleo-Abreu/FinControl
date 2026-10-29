
from flask import render_template, request, redirect, url_for
from models.operacao import Operacao


def inicio():
    return render_template("index.html")


def pagina_cadastro():
    return render_template("cadastro.html",erros=[],dados={})


def cadastrar():
    dados = {
        "data": request.form.get("data"),
        "ativo": request.form.get("ativo"),
        "quantidade": request.form.get("quantidade"),
        "valor_unitario": request.form.get("valor_unitario"),
        "tipo_operacao": request.form.get("tipo_operacao")
    }

    operacao = Operacao(dados)

    if operacao.save():
        return render_template("resultado.html", mensagem="Operação cadastrada com sucesso!")

    return render_template("cadastro.html", erros=operacao.errors,dados=dados)

def listar_operacoes():
    operacoes = Operacao.exibir_operacoes()

    return render_template("operacoes.html", operacoes=operacoes)


def pesquisar_operacao():
    tipo = request.args.get("tipo", "id")
    termo = request.args.get("termo", "").strip()
    termo_ativo = request.args.get("termo_ativo", "").strip().upper()
    data_inicio = request.args.get("data_inicio", "")
    data_fim = request.args.get("data_fim", "")

    operacoes = []
    erro = None
    pesquisou = False

    if tipo == "id":
        pesquisou = bool(termo)

        if termo:
            try:
                operacao = Operacao.verificar_id(int(termo))

                if operacao:
                    operacoes = [operacao]
            except ValueError:
                erro = "Informe um ID numérico válido."

    elif tipo == "ativo":
        pesquisou = bool(termo_ativo)

        if termo_ativo:
            operacoes = Operacao.verificar_ativo(termo_ativo)

    elif tipo == "data":
        pesquisou = bool(data_inicio or data_fim)

        if data_inicio and data_fim:
            if data_inicio > data_fim:
                erro = "A data inicial não pode ser posterior à data final."
            else:
                operacoes = Operacao.verificar_periodo(
                    data_inicio, data_fim
                )
        elif not data_inicio or not data_fim:
            erro = "Informe a data inicial e a data final."

    else:
        erro = "Selecione um tipo de pesquisa."

    return render_template(
        "pesquisar.html",
        operacoes=operacoes,
        erro=erro,
        pesquisou=pesquisou,
        tipo=tipo,
        termo=termo,
        termo_ativo=termo_ativo,
        data_inicio=data_inicio,
        data_fim=data_fim
    )


def detalhes_operacao():
    id_operacao = request.args.get("id", "")

    try:
        id_operacao = int(id_operacao)
    except ValueError:
        return render_template("erro.html", mensagem="ID Inválido."), 400

    operacao = Operacao.verificar_id(id_operacao)

    if operacao is None:
        return render_template("erro.html", mensagem="Operação não encontrada."), 404

    return render_template("detalhes.html", operacao=operacao)


def editar_operacao(id_operacao):
    operacao = Operacao.verificar_id(id_operacao)

    if operacao is None:
        return render_template(
            "erro.html",
            mensagem="Operação não encontrada."
        ), 404

    return render_template(
        "editar.html",
        operacao=operacao,
        erros=[]
    )


def salvar_edicao(id_operacao):
    operacao_atual = Operacao.verificar_id(id_operacao)

    if operacao_atual is None:
        return render_template(
            "erro.html",
            mensagem="Operação não encontrada."
        ), 404

    dados = {
        "data": request.form.get("data"),
        "ativo": request.form.get("ativo"),
        "quantidade": request.form.get("quantidade"),
        "valor_unitario": request.form.get("valor_unitario"),
        "tipo_operacao": request.form.get("tipo_operacao")
    }

    operacao = Operacao(dados)

    if not operacao.validate(id_ignorar=id_operacao):
        return render_template(
            "editar.html",
            operacao={**dados, "id": id_operacao},
            erros=operacao.errors
        ), 400

    Operacao.atualizar_operacao(id_operacao, operacao._dados)

    return redirect(url_for("listar_operacoes"))


def excluir_operacao(id_operacao):
    operacao = Operacao.verificar_id(id_operacao)

    if operacao is None:
        return render_template(
            "erro.html",
            mensagem="Operação não encontrada."
        ), 404

    Operacao.excluir_operacao(id_operacao)

    return redirect(url_for("listar_operacoes"))
