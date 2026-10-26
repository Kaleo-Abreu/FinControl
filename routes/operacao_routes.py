from flask import Flask
import controller.operacao_controller

def iniciar_rotas(app: Flask):
    app.add_url_rule("/", view_func=controller.operacao_controller.inicio, methods=["GET"], endpoint="inicio")
    app.add_url_rule("/operacoes/cadastrar",view_func=controller.operacao_controller.pagina_cadastro,methods=["GET"],endpoint="pagina_cadastro")
    app.add_url_rule("/operacoes/cadastrar", view_func=controller.operacao_controller.cadastrar, methods=["POST"], endpoint="cadastrar")
    app.add_url_rule("/operacoes", view_func=controller.operacao_controller.listar_operacoes, methods=["GET"], endpoint="listar_operacoes")
    app.add_url_rule("/operacoes/pesquisar",view_func=controller.operacao_controller.pesquisar_operacao,methods=["GET"],endpoint="pesquisar_operacao")
    app.add_url_rule("/operacoes/detalhes", view_func=controller.operacao_controller.detalhes_operacao, methods=["GET"], endpoint="detalhes_operacao")
    app.add_url_rule("/operacoes/editar/<int:id_operacao>",view_func=controller.operacao_controller.editar_operacao,methods=["GET"],endpoint="editar_operacao")
    app.add_url_rule("/operacoes/editar/<int:id_operacao>",view_func=controller.operacao_controller.salvar_edicao,methods=["POST"],endpoint="salvar_edicao")
    app.add_url_rule("/operacoes/excluir/<int:id_operacao>",view_func=controller.operacao_controller.excluir_operacao,methods=["POST"],endpoint="excluir_operacao")