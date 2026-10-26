
from flask import render_template, request, redirect, url_for
from daos.operacao_dao import OperacaoDAO
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
    operacoes = OperacaoDAO.listar()

    return render_template("operacoes.html", operacoes=operacoes)


from daos.operacao_dao import OperacaoDAO


def pesquisar_operacao():
    tipo = request.args.get("tipo", "id")
    termo = request.args.get("termo", "").strip()
    data_inicio = request.args.get("data_inicio", "")
    data_fim = request.args.get("data_fim", "")

    operacoes = []
    erro = None

    if tipo == "id" and termo:
        try:
            operacao = OperacaoDAO.buscar_por_id(int(termo))
            if operacao:
                operacoes = [operacao]
        except ValueError:
            erro = "Informe um ID numérico válido."

    elif tipo == "ativo" and termo:
        operacoes = OperacaoDAO.buscar_por_ativo(termo.upper())

    elif tipo == "periodo":
        if data_inicio and data_fim and data_inicio <= data_fim:
            operacoes = OperacaoDAO.buscar_por_periodo(
                data_inicio, data_fim
            )
        else:
            erro = "Informe duas datas válidas e em ordem."

    return render_template(
        "pesquisar.html",operacoes=operacoes,tipo=tipo,termo=termo,data_inicio=data_inicio,data_fim=data_fim,erro=erro,pesquisou=bool(termo or data_inicio or data_fim))


def detalhes_operacao():
    id_operacao = request.args.get("id", "")

    try:
        id_operacao = int(id_operacao)
    except ValueError:
        return render_template("erro.html", mensagem="ID Inválido."), 400

    operacao = OperacaoDAO.buscar_por_id(id_operacao)

    if operacao is None:
        return render_template("erro.html", mensagem="Operação não encontrada."), 404

    return render_template("detalhes.html", operacao=operacao)


def editar_operacao(id_operacao):
    operacao = OperacaoDAO.buscar_por_id(id_operacao)

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
    operacao_atual = OperacaoDAO.buscar_por_id(id_operacao)

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

    if not operacao.validate():
        return render_template(
            "editar.html",
            operacao={**dados, "id": id_operacao},
            erros=operacao.errors
        ), 400

    OperacaoDAO.atualizar(id_operacao, operacao._dados)

    return redirect(url_for("listar_operacoes"))


def excluir_operacao(id_operacao):
    operacao = OperacaoDAO.buscar_por_id(id_operacao)

    if operacao is None:
        return render_template(
            "erro.html",
            mensagem="Operação não encontrada."
        ), 404

    OperacaoDAO.excluir(id_operacao)

    return redirect(url_for("listar_operacoes"))
