#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validar_casos_reglamento.py
Auditoría y control de calidad forense del banco de casos prácticos del Reglamento del Congreso Bicameral.
"""

import os
import sys
import json

def validar():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "casos_reglamento.json")
    
    if not os.path.exists(json_path):
        print(f"❌ Error: Archivo no encontrado en {json_path}")
        sys.exit(1)
        
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            casos = json.load(f)
    except Exception as e:
        print(f"❌ Error al decodificar JSON: {e}")
        sys.exit(1)
        
    if not isinstance(casos, list) or len(casos) == 0:
        print("❌ Error: 'casos_reglamento.json' debe ser una lista no vacía de casos.")
        sys.exit(1)
        
    required_fields = [
        "id", "categoria", "camara", "dificultad", "titulo",
        "caso", "pregunta", "opciones", "respuesta_correcta",
        "base_normativa", "fundamentacion"
    ]
    
    ids_vistos = set()
    errores = []
    
    for idx, c in enumerate(casos):
        cid = c.get("id", f"INDEX_{idx}")
        
        # Validar unicidad de ID
        if cid in ids_vistos:
            errores.append(f"[{cid}] ID duplicado en el registro {idx}.")
        ids_vistos.add(cid)
        
        # Validar campos obligatorios
        for field in required_fields:
            if field not in c or not str(c[field]).strip():
                errores.append(f"[{cid}] Campo obligatorio ausente o vacío: '{field}'.")
                
        # Validar opciones
        opciones = c.get("opciones", [])
        if not isinstance(opciones, list) or len(opciones) != 4:
            errores.append(f"[{cid}] Debe contener exactamente 4 opciones de respuesta (encontradas {len(opciones)}).")
        else:
            opt_ids = [o.get("id") for o in opciones if isinstance(o, dict)]
            if opt_ids != ["a", "b", "c", "d"]:
                errores.append(f"[{cid}] Los IDs de las opciones deben ser ['a', 'b', 'c', 'd']. Encontrado: {opt_ids}")
            for o in opciones:
                if not o.get("texto", "").strip():
                    errores.append(f"[{cid}] Opción '{o.get('id')}' tiene texto vacío.")
                    
        # Validar respuesta correcta
        resp_correcta = c.get("respuesta_correcta")
        if resp_correcta not in ["a", "b", "c", "d"]:
            errores.append(f"[{cid}] 'respuesta_correcta' inválida: '{resp_correcta}'. Debe ser 'a', 'b', 'c' o 'd'.")

    # Resumen
    print("=" * 65)
    print("🏛️ AUDITORÍA DE CASOS PRÁCTICOS DEL REGLAMENTO BICAMERAL")
    print("=" * 65)
    print(f"Total de casos auditados: {len(casos)}")
    
    # Distribución por categorías
    cats = {}
    for c in casos:
        cat = c.get("categoria", "Sin Categoría")
        cats[cat] = cats.get(cat, 0) + 1
        
    print("\n📊 Distribución por Eje Temático:")
    for cat, cnt in cats.items():
        print(f"  • {cat}: {cnt} casos")
        
    if errores:
        print("\n❌ Se detectaron los siguientes errores de integridad:")
        for err in errores:
            print(f"  - {err}")
        sys.exit(1)
    else:
        # Sincronizar automáticamente casos_reglamento.js para soporte file://
        js_path = os.path.join(base_dir, "casos_reglamento.js")
        with open(js_path, "w", encoding="utf-8") as f:
            f.write("window.CASOS_REGLAMENTO_DATA = " + json.dumps(casos, ensure_ascii=False, indent=2) + ";\n")
        print("\n✅ VALIDACIÓN EXITOSA: 100% de casos cumplen con los estándares de integridad.")
        print(f"📦 Sincronizado automáticamente: {os.path.basename(js_path)}")
        print("=" * 65)

if __name__ == "__main__":
    validar()
