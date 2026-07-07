import re
import json
import html

html_file = r"C:\Users\Sergio\.gemini\antigravity-cli\brain\a2883a1a-4e73-450c-b78a-3c67325ae1a7\.system_generated\steps\4\content.md"

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

content = html.unescape(content)

# We can find where the "diputados" section starts.
diputados_idx = content.find('"id":[0,"diputados"]')

# Reload the JSON
with open('C:/Users/Sergio/hemiciclo_data/candidatos.json', 'r', encoding='utf-8') as f:
    candidatos = json.load(f)

# Re-match the candidates and assign their chamber based on their position in the string
pattern = r'"dni":\[0,"(.*?)"\]'

for c in candidatos:
    match = re.search(r'"dni":\[0,"' + c['dni'] + r'"\]', content)
    if match:
        if match.start() < diputados_idx:
            c['chamber'] = 'senado'
        else:
            c['chamber'] = 'diputados'
    else:
        c['chamber'] = 'desconocido'

senadores_count = sum(1 for c in candidatos if c['chamber'] == 'senado')
diputados_count = sum(1 for c in candidatos if c['chamber'] == 'diputados')

print(f"Senadores: {senadores_count}, Diputados: {diputados_count}")

with open('C:/Users/Sergio/hemiciclo_data/candidatos.json', 'w', encoding='utf-8') as f:
    json.dump(candidatos, f, indent=4, ensure_ascii=False)
