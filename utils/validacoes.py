import re
from datetime import date


def codigo_valido(codigo):
    if not isinstance(codigo, str):
        return False

    return re.fullmatch(r"[A-Z]{4}\d{1,2}", codigo) is not None


def data_valida(data):
    if not isinstance(data, str):
        return False

    try:
        data_convertida = date.fromisoformat(data)
        return data_convertida <= date.today()
    except ValueError:
        return False
