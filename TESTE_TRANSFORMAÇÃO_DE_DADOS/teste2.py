import os
import zipfile
import pdfplumber
import pandas as pd

pdf_path = os.path.join(os.path.dirname(__file__), '..', '..', 'desafioTech', 'TESTE_WEB_SCRAPING', 'Anexos_ans', 'Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf')
pdf_path = os.path.abspath(pdf_path)

abreviacao = {
    "OD": "Seg. Odontológica",
    "AMB": "Seg. Ambulatorial"
}

tabelas_extraidas = []

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):  # Percorre todas as páginas
        tables = page.extract_tables()

        if tables:
            for tabela in tables:
                df = pd.DataFrame(tabela[1:], columns=tabela[0])  # Criando DataFrame
                
                # Substituindo valores em todas as colunas, se existirem
                df.replace(abreviacao, inplace=True)

                tabelas_extraidas.append(df)

if tabelas_extraidas:
    df_final = pd.concat(tabelas_extraidas, ignore_index=True)

    csv_path = "tabelas_extraidas.csv"
    df_final.to_csv(csv_path, index=False)

    zip_file = "tabelas_extraidas.zip"
    with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(csv_path, os.path.basename(csv_path))

    os.remove(csv_path)

    print(f"Tabelas extraídas e salvas em {zip_file}")
else:
    print("Nenhuma tabela encontrada no PDF.")
