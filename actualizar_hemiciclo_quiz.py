import os
import json
import shutil
import re
import pandas as pd

def normalize_name(name):
    # Convertir a minúsculas, remover tildes y caracteres especiales para un matcheo robusto
    name = str(name).lower().strip()
    replacements = (
        ("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("ñ", "n")
    )
    for a, b in replacements:
        name = name.replace(a, b)
    name = re.sub(r'[^a-z0-9\s]', '', name)
    return ' '.join(name.split())

def main():
    repo_dir = r'C:\Users\sergi\hemiciclo-quiz-app'
    json_path = os.path.join(repo_dir, 'candidatos.json')
    images_dir = os.path.join(repo_dir, 'images')
    excel_path = r'C:\Users\sergi\Base_Datos_Senadores_Diputados_2026.xlsx'
    
    print(f"--> Leyendo {json_path}...")
    with open(json_path, 'r', encoding='utf-8') as f:
        candidatos = json.load(f)
        
    print(f"--> Leyendo Excel con fotos oficiales: {excel_path}...")
    df = pd.read_excel(excel_path)
    
    # Crear diccionario mapeado por nombre normalizado
    excel_map = {}
    for idx, row in df.iterrows():
        nombre = str(row['Nombre Completo'])
        norm = normalize_name(nombre)
        excel_map[norm] = row
        
    print(f"--> Mapeando 190 parlamentarios entre el Excel y el Quiz JSON...")
    
    matched = 0
    unmatched = []
    
    for c in candidatos:
        cand_name = c['name']
        norm_cand = normalize_name(cand_name)
        
        # Búsqueda directa o por coincidencia de palabras clave
        matched_row = None
        if norm_cand in excel_map:
            matched_row = excel_map[norm_cand]
        else:
            # Buscar por similitud de palabras
            cand_words = set(norm_cand.split())
            best_match = None
            max_common = 0
            for ex_norm, ex_row in excel_map.items():
                ex_words = set(ex_norm.split())
                common = len(cand_words.intersection(ex_words))
                if common > max_common and common >= 2:
                    max_common = common
                    best_match = ex_row
            matched_row = best_match
            
        if matched_row is not None:
            matched += 1
            local_photo = str(matched_row['Ruta Foto Local']).strip()
            highres_url = str(matched_row['URL Foto Alta Res']).strip()
            camara_oficial = str(matched_row['Cámara']).lower().strip() # senado o diputados
            
            c['photoUrl'] = highres_url
            c['chamber'] = camara_oficial
            
            # Si existe la foto en alta resolución descargada, la copiamos a /images/ con el DNI del candidato
            if os.path.exists(local_photo):
                ext = os.path.splitext(local_photo)[1]
                if not ext: ext = ".jpg"
                
                target_filename = f"{c['dni']}{ext}"
                target_path = os.path.join(images_dir, target_filename)
                
                shutil.copy2(local_photo, target_path)
                c['localPhotoPath'] = f"images/{target_filename}"
        else:
            unmatched.append(cand_name)
            
    print(f"--> Coincidencias encontradas: {matched}/{len(candidatos)}")
    if unmatched:
        print(f"    Sin coincidencia directa: {unmatched}")
        
    # Guardar candidatos.json actualizado
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(candidatos, f, indent=4, ensure_ascii=False)
        
    print(f"--> ¡candidatos.json e imágenes en {images_dir} actualizados exitosamente!")

if __name__ == "__main__":
    main()
