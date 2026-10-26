
import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path(__file__).resolve().parent.parent / "fincontrol.db"


def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_tabela():
    conexao = conectar()

    try:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS operacoes (
                id INTEGER PRIMARY KEY
                    CHECK (
                        id BETWEEN 1000000000 AND 9999999999
                        AND id % 1000000000 = 0
                    ),

                data TEXT NOT NULL,
                ativo TEXT NOT NULL,
                quantidade INTEGER NOT NULL CHECK (quantidade > 0),
                valor_unitario NUMERIC NOT NULL
                    CHECK (valor_unitario > 0),

                tipo_operacao TEXT NOT NULL
                    CHECK (tipo_operacao IN ('compra', 'venda')),

                valor_bruto NUMERIC NOT NULL,
                taxas NUMERIC NOT NULL,
                valor_liquido NUMERIC NOT NULL
            )
        """)

        conexao.commit()

    finally:
        conexao.close()
