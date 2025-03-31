from flask import Flask, request, jsonify
import pandas as pd
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/buscar": {"origins": "*"}})  # Permitir CORS apenas para essa rota

# URL do CSV
CSV_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"

# Carregamento inicial do CSV
df = None

def carregar_dados():
    global df
    try:
        df = pd.read_csv(CSV_URL, sep=';', encoding='latin1')
        df.columns = df.columns.str.strip().str.replace(' ', '_')  # Padroniza os nomes das colunas
        print("Dados carregados com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar o CSV: {e}")
        df = None

carregar_dados()  # Chama ao iniciar o servidor

@app.route('/buscar', methods=['GET'])
def buscar_operadora():
    if df is None:
        return jsonify({"erro": "Dados indisponíveis"}), 500

    termo = request.args.get('q', '').strip()

    if not termo:
        return jsonify({"erro": "Nenhum termo de busca fornecido"}), 400

    if "Nome_Fantasia" not in df.columns:
        return jsonify({"erro": "Coluna Nome_Fantasia não encontrada"}), 500

    try:
        resultado = df[df["Nome_Fantasia"].str.contains(re.escape(termo), flags=re.IGNORECASE, na=False)]

        if resultado.empty:
            return jsonify([])  # Retorna lista vazia se não houver resultados

        return jsonify(resultado.to_dict(orient='records'))
    except Exception as e:
        return jsonify({"erro": f"Erro na busca: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
