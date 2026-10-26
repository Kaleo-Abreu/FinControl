
from daos.operacao_dao import OperacaoDAO
from utils.validacoes import codigo_valido, data_valida


class Operacao:
    TIPO_OPERACAO = {
        1: "Compra",
        2: "Venda"
    }

    def __init__(self, dados):
        self._dados = dict(dados) if dados else {}
        self.errors = []

    def validate(self):
        self.errors = []

        data = self._dados.get("data")
        if not data_valida(data):
            self.errors.append("Informe uma data válida.")

        ativo = self._dados.get("ativo") or self._dados.get("codigo")
        if not codigo_valido(ativo):
            self.errors.append(
                "O ativo deve ter quatro letras maiúsculas "
                "seguidas de um ou dois números."
            )

        try:
            quantidade = int(self._dados.get("quantidade"))
            if quantidade <= 0:
                raise ValueError
        except (TypeError, ValueError):
            quantidade = 0
            self.errors.append("A quantidade deve ser um inteiro positivo.")

        try:
            valor_unitario = float(
                str(self._dados.get("valor_unitario", "")).replace(",", ".")
            )
            if valor_unitario <= 0:
                raise ValueError
        except (TypeError, ValueError):
            valor_unitario = 0
            self.errors.append("O valor unitário deve ser positivo.")

        try:
            tipo_operacao = int(self._dados.get("tipo_operacao"))
            if tipo_operacao not in self.TIPO_OPERACAO:
                raise ValueError
        except (TypeError, ValueError):
            tipo_operacao = 0
            self.errors.append("Selecione compra ou venda.")

        if self.errors:
            return False

        valor_bruto = round(quantidade * valor_unitario, 2)
        taxas = round(valor_bruto * 0.0003, 2)

        if tipo_operacao == 1:
            valor_liquido = round(valor_bruto + taxas, 2)
            tipo_texto = "compra"
        else:
            valor_liquido = round(valor_bruto - taxas, 2)
            tipo_texto = "venda"

        self._dados.update({
            "data": data,
            "ativo": ativo,
            "quantidade": quantidade,
            "valor_unitario": valor_unitario,
            "tipo_operacao": tipo_texto,
            "valor_bruto": valor_bruto,
            "taxas": taxas,
            "valor_liquido": valor_liquido
        })

        return True

    def save(self):
        if not self.validate():
            return False

        OperacaoDAO.inserir(self._dados)
        return True

    @property
    def id(self):
        return self._dados.get("id")

    @property
    def data(self):
        return self._dados.get("data")

    @property
    def ativo(self):
        return self._dados.get("ativo") or self._dados.get("codigo")

    @property
    def quantidade(self):
        return self._dados.get("quantidade")

    @property
    def valor_unitario(self):
        return self._dados.get("valor_unitario")

    @property
    def tipo_operacao(self):
        return self._dados.get("tipo_operacao")

    @property
    def valor_bruto(self):
        return self._dados.get("valor_bruto")

    @property
    def taxas(self):
        return self._dados.get("taxas")

    @property
    def valor_liquido(self):
        return self._dados.get("valor_liquido")
