import json
import re

with open('C:/Users/Sergio/hemiciclo_data/lista_oficial.txt', 'r', encoding='utf-8') as f:
    text = f.read().lower()

with open('C:/Users/Sergio/hemiciclo_data/candidatos.json', 'r', encoding='utf-8') as f:
    candidatos = json.load(f)

# Limpiar texto para busqueda
text_clean = re.sub(r'[^a-záéíóúñ]', '', text)

mismatches = []
for c in candidatos:
    name_clean = re.sub(r'[^a-záéíóúñ]', '', c['name'].lower())
    # Buscar si todos los caracteres del nombre limpio estan en algun lado del texto de forma contigua, 
    # o mejor, si las palabras del nombre aparecen
    parts = c['name'].lower().split()
    found = True
    for p in parts:
        if p not in text:
            found = False
            break
    if not found:
        mismatches.append(c['name'])

print("Total en JSON:", len(candidatos))
print("Mismatches encontrados:", len(mismatches))
if mismatches:
    print(mismatches[:10])
