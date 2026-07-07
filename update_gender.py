import json

# Lista de nombres femeninos comunes que no terminan en 'a'
female_names = [
    "carmen", "pilar", "beatriz", "isabel", "leonor", "luz", "marisol", 
    "flor", "miriam", "esther", "gladys", "ruth", "ines", "rosario", 
    "milagros", "consuelo", "lourdes", "betty", "nelly", "jenny", "mabel", "shirley",
    "katherine", "judith", "susana", "edith", "mirtha", "margot", "evelyn",
    "abigail", "raquel", "liz", "maribel", "sol", "iris", "jeanette", "carol",
    "marlene", "lilian", "yvonne", "doris"
]

# Lista de nombres masculinos que pueden terminar en 'a'
male_names_a = ["luca", "andrea", "elias", "josias", "isaias", "jose maria"]

with open('C:/Users/Sergio/hemiciclo_data/candidatos.json', 'r', encoding='utf-8') as f:
    candidatos = json.load(f)

for c in candidatos:
    full_name = c['name'].lower().strip()
    first_name = full_name.split()[0]
    
    # Manejar "Jose Maria" u otros compuestos si es necesario
    if full_name.startswith("jose maria"):
        c['gender'] = 'M'
        continue
    if full_name.startswith("maria del ") or full_name.startswith("maria de ") or full_name.startswith("maria "):
        c['gender'] = 'F'
        continue
        
    if first_name in female_names:
        c['gender'] = 'F'
    elif first_name in male_names_a:
        c['gender'] = 'M'
    elif first_name.endswith('a'):
        c['gender'] = 'F'
    else:
        c['gender'] = 'M'

# Count them to see
males = sum(1 for c in candidatos if c['gender'] == 'M')
females = sum(1 for c in candidatos if c['gender'] == 'F')
print(f"Males: {males}, Females: {females}")

with open('C:/Users/Sergio/hemiciclo_data/candidatos.json', 'w', encoding='utf-8') as f:
    json.dump(candidatos, f, indent=4, ensure_ascii=False)
