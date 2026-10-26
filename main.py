from flask import Flask
from routes.operacao_routes import iniciar_rotas
from daos.conexao import criar_tabela

app = Flask(__name__)

criar_tabela()
iniciar_rotas(app)


if __name__ == "__main__":
    app.run(debug=True)
