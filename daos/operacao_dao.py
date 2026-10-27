
from daos.conexao import conectar


class OperacaoDAO:

    @staticmethod
    def inserir(dados):
        conexao = conectar()

        try:
            resultado = conexao.execute(
                "SELECT MAX(id) AS maior_id FROM operacoes"
            ).fetchone()

            if resultado["maior_id"] is None:
                novo_id = 1000000000
            else:
                novo_id = resultado["maior_id"] + 1

            conexao.execute("""
                INSERT INTO operacoes (
                    id,
                    data,
                    ativo,
                    quantidade,
                    valor_unitario,
                    tipo_operacao,
                    valor_bruto,
                    taxas,
                    valor_liquido
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                novo_id,
                dados["data"],
                dados["ativo"],
                dados["quantidade"],
                dados["valor_unitario"],
                dados["tipo_operacao"],
                dados["valor_bruto"],
                dados["taxas"],
                dados["valor_liquido"]
            ))

            conexao.commit()
            return novo_id

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()


    @staticmethod
    def listar():
        conexao = conectar()

        try:
            operacoes = conexao.execute(
                "SELECT * FROM operacoes ORDER BY data DESC"
            ).fetchall()

            return operacoes
        finally:
            conexao.close()

    @staticmethod
    def buscar_por_id(id_operacao):
        conexao = conectar()

        try:
            operacao = conexao.execute(
                "SELECT * FROM operacoes WHERE id = ?",
                (id_operacao,)
            ).fetchone()

            return operacao
        finally:
            conexao.close()

    @staticmethod
    def buscar_por_ativo(ativo):
        conexao = conectar()

        try:
            operacao = conexao.execute(
                "SELECT * FROM operacoes WHERE ativo = ? ORDER BY data DESC",
                (ativo,)
            ).fetchall()

            return operacao
        finally:
            conexao.close()

    @staticmethod
    def buscar_por_periodo(data_inicio, data_fim):
        conexao = conectar()

        try:
            operacao = conexao.execute(
                "SELECT * FROM operacoes WHERE data BETWEEN ? AND ? ORDER BY data DESC",
                (data_inicio, data_fim)
            ).fetchall()

            return operacao
        finally:
            conexao.close()

    
    @staticmethod
    def atualizar(id_operacao, dados):
        conexao = conectar()

        try:
            conexao.execute("""
                UPDATE operacoes
                SET data = ?,
                    ativo = ?,
                    quantidade = ?,
                    valor_unitario = ?,
                    tipo_operacao = ?,
                    valor_bruto = ?,
                    taxas = ?,
                    valor_liquido = ?
                WHERE id = ?
            """, (
                dados["data"],
                dados["ativo"],
                dados["quantidade"],
                dados["valor_unitario"],
                dados["tipo_operacao"],
                dados["valor_bruto"],
                dados["taxas"],
                dados["valor_liquido"],
                id_operacao
            ))

            conexao.commit()
            return True

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()

    
    @staticmethod
    def excluir(id_operacao):
        conexao = conectar()

        try:
            conexao.execute(
                "DELETE FROM operacoes WHERE id = ?",
                (id_operacao,)
            )

            conexao.commit()
        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()
