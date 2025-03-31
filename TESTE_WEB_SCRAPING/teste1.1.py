import requests
from bs4 import BeautifulSoup
import os
import zipfile

url = requests.get('https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos')

os.makedirs('Anexos_ans', exist_ok=True)

informacoes = BeautifulSoup(url.text, 'html.parser')



pdf_links = []

for link in informacoes.find_all('a', href=True):
    if "Anexo" in link.text and link["href"].endswith(".pdf"):
        pdf_links.append(link["href"])


for link in pdf_links :
    response = requests.get(link)

    if response.status_code == 200:
        arquivo_path = os.path.join('Anexos_ans', os.path.basename(link))
        with open(arquivo_path, 'wb') as f:
            f.write(response.content)
            print(f"Baixando: {arquivo_path}")
    else:
        print(f"Erro ao baixar {link}: status {response.status_code}")

zip_path = "Anexos_ans.zip"
with zipfile.ZipFile(zip_path, "w") as zipf:
    for file in os.listdir('Anexos_ans'):
        zipf.write(os.path.join('Anexos_ans', file), file)

print(f"Todos os arquivos foram compactados em {zip_path}")