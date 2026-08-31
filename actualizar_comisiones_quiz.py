# -*- coding: utf-8 -*-
"""
Actualiza candidatos.json integrando la información completa y precisa de comisiones y cargos
tanto para Senadores como para Diputados (Periodo 2026-2027).
"""

import os
import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

def normalizar_texto(texto):
    texto = str(texto).lower().strip()
    reemplazos = (
        ("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("ñ", "n")
    )
    for a, b in reemplazos:
        texto = texto.replace(a, b)
    texto = re.sub(r'[^a-z0-9\s]', ' ', texto)
    return ' '.join(texto.split())

def jerarquia_cargo(cargo):
    c = cargo.lower()
    if 'presiden' in c and 'vice' not in c:
        return 1
    if 'vice' in c:
        return 2
    if 'secretar' in c:
        return 3
    if 'titular' in c:
        return 4
    if 'suplente' in c:
        return 5
    return 6

def limpiar_nombre_comision(nom):
    limpio = nom.replace("Comisión en asuntos de ", "").replace("Comisión de ", "").replace("Comisión ", "")
    return limpio.strip().rstrip('.')

def calcular_similitud(palabras_cand, palabras_parl):
    inter = len(palabras_cand.intersection(palabras_parl))
    union = len(palabras_cand.union(palabras_parl))
    return inter / union if union > 0 else 0

def main():
    repo_dir = r"C:\Users\sergi\hemiciclo-quiz-app"
    json_candidatos = os.path.join(repo_dir, "candidatos.json")
    
    json_diputados = r"C:\Users\sergi\Diputados_Comisiones_Congreso_2026_2027\comisiones_completas.json"
    json_senadores = r"C:\Users\sergi\Senadores_Comisiones_Congreso_2026_2027\comisiones_completas.json"
    
    print(f"--> Cargando candidatos desde {json_candidatos}...")
    with open(json_candidatos, 'r', encoding='utf-8') as f:
        candidatos = json.load(f)
        
    print(f"--> Cargando comisiones de Diputados desde {json_diputados}...")
    with open(json_diputados, 'r', encoding='utf-8') as f:
        com_diputados = json.load(f)
        
    print(f"--> Cargando comisiones de Senadores desde {json_senadores}...")
    with open(json_senadores, 'r', encoding='utf-8') as f:
        com_senadores = json.load(f)
        
    # Construir mapa de personas a comisiones: clave = nombre_normalizado_persona
    # En comisiones: m['nombre'] es "Apellidos, Nombres"
    dip_map = {}
    for c_name, members in com_diputados.items():
        for m in members:
            raw_nom = m['nombre']
            norm_nom = normalizar_texto(raw_nom)
            if norm_nom not in dip_map:
                dip_map[norm_nom] = {
                    'raw_name': raw_nom,
                    'words': set(norm_nom.split()),
                    'comisiones': []
                }
            dip_map[norm_nom]['comisiones'].append({
                'comision': c_name,
                'comision_corta': limpiar_nombre_comision(c_name),
                'cargo': m['cargo'],
                'grupo': m.get('grupo', ''),
                'email': m.get('email', '')
            })
            
    sen_map = {}
    for c_name, members in com_senadores.items():
        for m in members:
            raw_nom = m['nombre']
            norm_nom = normalizar_texto(raw_nom)
            if norm_nom not in sen_map:
                sen_map[norm_nom] = {
                    'raw_name': raw_nom,
                    'words': set(norm_nom.split()),
                    'comisiones': []
                }
            sen_map[norm_nom]['comisiones'].append({
                'comision': c_name,
                'comision_corta': limpiar_nombre_comision(c_name),
                'cargo': m['cargo'],
                'grupo': m.get('grupo', ''),
                'email': m.get('email', '')
            })
            
    print(f"--> Total de parlamentarios a enriquecer: {len(candidatos)}")
    
    total_con_comisiones = 0
    total_sin_comisiones = 0
    
    for c in candidatos:
        cand_name = c['name']
        cand_norm = normalizar_texto(cand_name)
        cand_words = set(cand_norm.split())
        
        target_map = sen_map if c.get('chamber') == 'senado' else dip_map
        
        # Encontrar el mejor match usando Jaccard similarity
        best_sim = 0
        best_match_data = None
        for p_norm, p_data in target_map.items():
            sim = calcular_similitud(cand_words, p_data['words'])
            if sim > best_sim:
                best_sim = sim
                best_match_data = p_data
                
        # Caso especial para Wilfredo Verano
        if 'wilfredo' in cand_norm and 'verano' in cand_norm and c.get('chamber') == 'senado':
            for p_norm, p_data in target_map.items():
                if 'wilfredo' in p_norm and 'verano' in p_norm:
                    best_sim = 1.0
                    best_match_data = p_data
                    break

        # Exigir un umbral alto de similitud (>= 0.6) para evitar falsos positivos
        if best_sim >= 0.6 and best_match_data:
            coms = best_match_data['comisiones']
            coms_ordenadas = sorted(coms, key=lambda x: (jerarquia_cargo(x['cargo']), x['comision_corta']))
            c['comisiones'] = coms_ordenadas
            total_con_comisiones += 1
        else:
            c['comisiones'] = []
            total_sin_comisiones += 1
            print(f"    [i] Sin comisiones en portal oficial: {c.get('chamber').upper()} - {cand_name} (Similitud máx: {best_sim:.2f})")
            
    with open(json_candidatos, 'w', encoding='utf-8') as f:
        json.dump(candidatos, f, ensure_ascii=False, indent=4)
        
    print(f"\n--> candidatos.json actualizado con éxito:")
    print(f"    - Parlamentarios con comisiones asignadas: {total_con_comisiones} / {len(candidatos)}")
    print(f"    - Parlamentarios sin comisiones asignadas: {total_sin_comisiones} / {len(candidatos)}")

if __name__ == '__main__':
    main()
