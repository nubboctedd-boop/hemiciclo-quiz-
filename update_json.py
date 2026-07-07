import json

parties = {
    22: "Renovación Popular (RP)",
    1264: "Juntos por el Perú (JP)",
    1366: "Fuerza Popular (FP)",
    2941: "Partido Cívico Obras (OBRAS)",
    2956: "País para Todos (PPT)",
    2961: "Partido del Buen Gobierno (BG)",
    2980: "Ahora Nación (AN)"
}

with open('C:/Users/Sergio/hemiciclo_data/candidatos.json', 'r', encoding='utf-8') as f:
    candidatos = json.load(f)

for c in candidatos:
    c['partyName'] = parties.get(c['partyCode'], str(c['partyCode']))

with open('C:/Users/Sergio/hemiciclo_data/candidatos.json', 'w', encoding='utf-8') as f:
    json.dump(candidatos, f, indent=4, ensure_ascii=False)

print("Updated JSON with party names")
