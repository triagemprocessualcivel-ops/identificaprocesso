#!/usr/bin/env python3
"""
Consulta de Juízo por Número Único de Processo (CNJ - Resolução 65/2008)
=========================================================================

Formato do número: NNNNNNN-DD.AAAA.J.TR.OOOO

  NNNNNNN = número sequencial do processo
  DD      = dígito verificador
  AAAA    = ano de ajuizamento
  J       = código do segmento de Justiça (1 dígito)
  TR      = código do Tribunal (2 dígitos)
  OOOO    = código da unidade de origem (4 dígitos)

Este script:
  1. Solicita ao usuário o número do processo.
  2. Valida o formato via regex.
  3. Extrai os campos J, TR e OOOO.
  4. Consulta a matriz de códigos (matriz_codigos_cnj.json) para
     identificar Justiça, Tribunal e Unidade de Origem.
  5. Retorna SOMENTE o juízo onde o processo tramita.

Uso:
  python3 consulta_juizo_cnj.py
  python3 consulta_juizo_cnj.py 0010507-38.2021.5.18.0008
"""

import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

MATRIZ_PATH = Path(__file__).parent / "matriz_codigos_cnj.json"

# Mapa do dígito J (segmento de Justiça) -> chave usada na matriz + nome
MAPA_JUSTICA = {
    "1": ("justica_federal_j1", "Federal"),
    "2": ("justica_estadual_militar_j2", "Estadual Militar"),
    "3": ("justica_militar_uniao_j3", "Militar da União"),
    "4": ("justica_trabalho_j4", "Trabalho"),  # variação, caso exista
    "5": ("justica_trabalho_j5", "Trabalho"),
    "6": ("justica_eleitoral_j6", "Eleitoral"),
    "7": ("justica_federal_j7", "Federal"),  # variação, caso exista
    "8": ("justica_estadual_j8", "Estadual"),
    "9": ("justica_federal_j9", "Federal"),  # variação, caso exista
}

# Regex oficial do padrão CNJ: NNNNNNN-DD.AAAA.J.TR.OOOO
REGEX_CNJ = re.compile(
    r"^(\d{7})-(\d{2})\.(\d{4})\.(\d{1})\.(\d{2})\.(\d{4})$"
)


# ---------------------------------------------------------------------------
# Funções principais
# ---------------------------------------------------------------------------

def carregar_matriz(caminho: Path) -> dict:
    """Carrega a matriz de códigos CNJ a partir do arquivo JSON."""
    if not caminho.exists():
        raise FileNotFoundError(
            f"Matriz de códigos não encontrada em: {caminho}\n"
            "Certifique-se de que 'matriz_codigos_cnj.json' está na mesma "
            "pasta deste script."
        )
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def extrair_campos(numero_processo: str) -> dict:
    """
    Extrai N, DD, AAAA, J, TR, OOOO do número do processo.
    Lança ValueError se o formato for inválido.
    """
    numero_limpo = numero_processo.strip()
    match = REGEX_CNJ.match(numero_limpo)
    if not match:
        raise ValueError(
            "Número de processo em formato inválido. "
            "Esperado: NNNNNNN-DD.AAAA.J.TR.OOOO "
            "(ex: 0010507-38.2021.5.18.0008)"
        )
    numero, dv, ano, justica, tribunal, origem = match.groups()
    return {
        "numero_sequencial": numero,
        "digito_verificador": dv,
        "ano": ano,
        "justica_codigo": justica,
        "tribunal_codigo": tribunal,
        "unidade_codigo": origem,
    }


def consultar_juizo(numero_processo: str, matriz: dict) -> str:
    """
    Recebe o número do processo e a matriz de códigos.
    Retorna uma string única com o juízo (unidade + tribunal).
    Lança ValueError com mensagem clara em caso de dado não encontrado.
    """
    campos = extrair_campos(numero_processo)

    codigo_j = campos["justica_codigo"]
    codigo_tr = campos["tribunal_codigo"]
    codigo_oooo = campos["unidade_codigo"]

    if codigo_j not in MAPA_JUSTICA:
        raise ValueError(f"Código de Justiça '{codigo_j}' não reconhecido.")

    chave_justica, _nome_justica = MAPA_JUSTICA[codigo_j]

    bloco_justica = matriz.get(chave_justica)
    if bloco_justica is None:
        raise ValueError(
            f"Segmento de Justiça '{chave_justica}' não está cadastrado "
            "na matriz de códigos disponível."
        )

    tribunais = bloco_justica.get("tribunais", {})
    tribunal_info = tribunais.get(codigo_tr)
    if tribunal_info is None:
        raise ValueError(
            f"Tribunal com código '{codigo_tr}' não está cadastrado na "
            f"matriz para o segmento '{chave_justica}'."
        )

    nome_tribunal = tribunal_info.get("nome_tribunal", f"Tribunal {codigo_tr}")
    unidades = tribunal_info.get("unidades_origem_oooo", {})
    nome_unidade = unidades.get(codigo_oooo)

    if nome_unidade is None:
        raise ValueError(
            f"Unidade de origem com código '{codigo_oooo}' não encontrada "
            f"na tabela do {nome_tribunal}. Consulte a tabela oficial do "
            "tribunal para confirmar o nome exato dessa unidade."
        )

    return f"Juízo: {nome_unidade} — {nome_tribunal}"


# ---------------------------------------------------------------------------
# Interface de linha de comando
# ---------------------------------------------------------------------------

def main():
    matriz = carregar_matriz(MATRIZ_PATH)

    # Número pode vir como argumento de linha de comando ou ser solicitado
    if len(sys.argv) > 1:
        numero_processo = sys.argv[1]
    else:
        numero_processo = input(
            "Informe o número do processo (NNNNNNN-DD.AAAA.J.TR.OOOO): "
        )

    try:
        resultado = consultar_juizo(numero_processo, matriz)
    except (ValueError, FileNotFoundError) as erro:
        print(f"Erro: {erro}")
        sys.exit(1)

    print(resultado)


if __name__ == "__main__":
    main()
