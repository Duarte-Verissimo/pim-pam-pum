"""
Script para descarregar dados do curso LEI e das UCs
a partir da API pública da Universidade Lusófona.
Guarda os JSONs na pasta data/files/.
"""

import requests
import json
import os
import sys

# Pasta onde guardar os ficheiros JSON
FILES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'files')
os.makedirs(FILES_DIR, exist_ok=True)

schoolYear = '202526'
course = 260  # LEI - Licenciatura em Engenharia Informática

print(f"=== A descarregar dados do curso {course} (ano {schoolYear}) ===\n")

for language in ['PT', 'ENG']:
    print(f"--- Idioma: {language} ---")

    # 1. Obter detalhes do curso
    url_course = 'https://secure.ensinolusofona.pt/dados-publicos-academicos/resources/GetCourseDetail'
    payload = {
        'language': language,
        'courseCode': course,
        'schoolYear': schoolYear
    }
    headers = {'content-type': 'application/json'}

    response = requests.post(url_course, json=payload, headers=headers)
    response_dict = response.json()

    course_file = os.path.join(FILES_DIR, f"ULHT{course}-{language}.json")
    with open(course_file, "w", encoding="utf-8") as f:
        json.dump(response_dict, f, indent=4, ensure_ascii=False)
    print(f"  ✅ Curso guardado: {course_file}")

    # 2. Para cada UC do plano curricular, obter detalhes
    ucs = response_dict.get('courseFlatPlan', [])
    print(f"  Encontradas {len(ucs)} UCs no plano curricular.\n")

    for uc in ucs:
        uc_code = uc['curricularIUnitReadableCode']
        url_uc = 'https://secure.ensinolusofona.pt/dados-publicos-academicos/resources/GetSIGESCurricularUnitDetails'
        payload_uc = {
            'language': language,
            'curricularIUnitReadableCode': uc_code,
        }

        response_uc = requests.post(url_uc, json=payload_uc, headers=headers)
        response_uc_dict = response_uc.json()

        uc_file = os.path.join(FILES_DIR, f"{uc_code}-{language}.json")
        with open(uc_file, "w", encoding="utf-8") as f:
            json.dump(response_uc_dict, f, indent=4, ensure_ascii=False)
        print(f"  ✅ UC guardada: {uc_code} - {uc.get('curricularIUnitName', '')}")

print("\n=== Download concluído! ===")
