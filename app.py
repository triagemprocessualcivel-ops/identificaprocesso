#!/usr/bin/env python3
"""
Aplicação web Flask para consulta de juízo por número de processo CNJ.
"""

import json
import re
import os
from pathlib import Path
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Configuração
MATRIZ_PATH = Path(__file__).parent / "matriz_codigos_cnj.json"

# Mapa do dígito J (segmento de Justiça) -> chave usada na matriz + nome
MAPA_JUSTICA = {
    "1": ("justica_federal_j1", "Federal"),
    "2": ("justica_estadual_militar_j2", "Estadual Militar"),
    "3": ("justica_militar_uniao_j3", "Militar da União"),
    "4": ("justica_trabalho_j4", "Trabalho"),
    "5": ("justica_trabalho_j5", "Trabalho"),
    "6": ("justica_eleitoral_j6", "Eleitoral"),
    "7": ("justica_federal_j7", "Federal"),
    "8": ("justica_estadual_j8", "Estadual"),
    "9": ("justica_federal_j9", "Federal"),
}

# Regex oficial do padrão CNJ: NNNNNNN-DD.AAAA.J.TR.OOOO
REGEX_CNJ = re.compile(
    r"^(\d{7})-(\d{2})\.(\d{4})\.(\d{1})\.(\d{2})\.(\d{4})$"
)


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

    return f"{nome_unidade} — {nome_tribunal}"


# Carrega a matriz na inicialização
try:
    MATRIZ = carregar_matriz(MATRIZ_PATH)
except FileNotFoundError as e:
    MATRIZ = None
    print(f"AVISO: {e}")


@app.route("/")
def index():
    """Página inicial com formulário de consulta."""
    return render_template("index.html")


@app.route("/api/consultar", methods=["POST"])
def api_consultar():
    """API endpoint para consultar um processo."""
    if MATRIZ is None:
        return jsonify({"erro": "Matriz de códigos não disponível"}), 500

    data = request.get_json()
    numero_processo = data.get("numero_processo", "").strip()

    if not numero_processo:
        return jsonify({"erro": "Número de processo é obrigatório"}), 400

    try:
        juizo = consultar_juizo(numero_processo, MATRIZ)
        return jsonify({"sucesso": True, "juizo": juizo})
    except ValueError as e:
        return jsonify({"sucesso": False, "erro": str(e)}), 400


@app.route("/health")
def health():
    """Health check para monitoramento."""
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    # Para desenvolvimento local (não executar com gunicorn)
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
