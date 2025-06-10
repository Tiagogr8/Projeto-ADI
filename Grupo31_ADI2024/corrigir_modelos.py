import csv
import pandas as pd
from tqdm import tqdm
from difflib import get_close_matches
from fuzzywuzzy import process


with open('aligned_data1.csv', 'r') as file:
    reader = csv.reader(file)
    data1 = list(reader)

aligned_data = {}
for row in data1:
    if row[0].lower() not in aligned_data:
        aligned_data[row[0].lower()] = []
    aligned_data[row[0].lower()].append(row[1])

def find_match1(modelo_errado, modelos_corretos):
    modelo_errado = ' '.join(modelo_errado.split()[:3])
    print(modelo_errado)
    match, score = process.extractOne(modelo_errado, modelos_corretos)

    return match if score > 80 else None  # Only return match if score is greater than 80
def find_match2(modelo_errado, modelos_corretos):
    modelo_errado = ' '.join(modelo_errado.split()[:3])
    print(modelo_errado)
    #se a primeira paralvra for f150 ou f250 ou f350 trocar a primeira palavra por f-150, f-250, f-350
    if modelo_errado.split()[0] == "f150":
        modelo_errado = "F-150" + modelo_errado[4:]
    elif modelo_errado.split()[0] == "f250":
        modelo_errado = "F-250" + modelo_errado[4:]
    elif modelo_errado.split()[0] == "f350":
        modelo_errado = "F-350" + modelo_errado[4:]
    elif modelo_errado.split()[0] == "f450":
        modelo_errado = "F-450" + modelo_errado[4:]
    match = get_close_matches(modelo_errado, modelos_corretos, n=3, cutoff=0.5)
    # find the best
    match = sorted(match, key=lambda x: process.extractOne(modelo_errado, x)[1], reverse=True)
    if not match:
        match = get_close_matches(modelo_errado, modelos_corretos, n=3, cutoff=0.3)
        match = sorted(match, key=lambda x: process.extractOne(modelo_errado, x)[1], reverse=True)
    return match[0] if match else None  # Only return match if match is found

correspondencia = []


with open('marcas_corrigidos2.csv', 'r') as file:
    reader = csv.reader(file)
    data = list(reader)
    # List of only 100rows
    print(aligned_data)
    for row in tqdm(data, desc="Processing", unit="rows"):
        #pocurar no dicionario de marcas corrigidas se existe a marca na 3 coluna do csv
        if isinstance(row[3], str) and row[3].lower() in aligned_data:
            #se existir, procurar o modelo correto
            if row[3] == "ford":
                correspondencia.append((row[0],row[3], find_match2(row[2], aligned_data[row[3]])))
            else:
                correspondencia.append((row[0],row[3], find_match1(row[2], aligned_data[row[3]])))
            print(f"Corrigindo modelo {row[2]} para {correspondencia[-1][2]}")
        else:
            print(f"Marca {row[2]} não encontrada no dicionário de marcas corrigidas")

print(aligned_data)
print("Correção concluída!")
with open('maosca_corrigidos2.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for row in correspondencia:
        writer.writerow(row)