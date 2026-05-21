"""
Script para carregar dados do curso e UCs a partir dos JSONs
descarregados da API da Lusófona (pasta data/files/).
"""

import os
import sys
import django
import json

# Configuração Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from portfolio.models import Licenciatura, Docente, UnidadeCurricular

FILES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'files')

print("=== A carregar dados do curso e UCs da API Lusófona ===\n")

# ============================================================
# 1. CARREGAR DADOS DO CURSO (Licenciatura)
# ============================================================
course_file = os.path.join(FILES_DIR, 'ULHT260-PT.json')

with open(course_file, encoding='utf-8') as f:
    course_data = json.load(f)

course_detail = course_data['courseDetail']

lic, created = Licenciatura.objects.update_or_create(
    nome=course_detail['courseName'],
    defaults={
        'sigla': 'LEI',
        'descricao': course_detail.get('presentation', ''),
        'objetivos': course_detail.get('objectives', ''),
        'ects_total': course_detail.get('courseECTS'),
        'duracao_anos': course_detail.get('semesters', 6) // 2,
        'url_oficial': course_detail.get('courseUrl', ''),
        'departamento': course_detail.get('departement', ''),
    }
)
print(f"{'✅ Criada' if created else 'ℹ️ Atualizada'} Licenciatura: {lic}")

# ============================================================
# 2. CARREGAR DOCENTES do corpo docente do curso
# ============================================================
print("\n--- Docentes do curso ---")
teachers = course_data.get('teachers', [])
docentes_map = {}  # fullName -> objeto Docente

for teacher in teachers:
    nome = teacher.get('academicName', teacher.get('fullName', '')).strip()
    if not nome:
        continue

    docente, created = Docente.objects.update_or_create(
        nome=nome,
        defaults={
            'url_pagina_lusofona': '',
        }
    )
    docentes_map[nome.upper()] = docente
    if created:
        print(f"  ✅ Criado: {docente}")

print(f"  Total docentes processados: {len(docentes_map)}")

# ============================================================
# 3. CARREGAR UNIDADES CURRICULARES
# ============================================================
print("\n--- Unidades Curriculares ---")

# courseFlatPlan tem info básica de cada UC (nome, ects, ano, semestre)
flat_plan = course_data.get('courseFlatPlan', [])

for uc_plan in flat_plan:
    uc_code = uc_plan['curricularIUnitReadableCode']
    uc_name = uc_plan['curricularUnitName']

    # Tentar ler o JSON detalhado da UC
    uc_detail_file = os.path.join(FILES_DIR, f"{uc_code}-PT.json")
    uc_detail = {}
    if os.path.exists(uc_detail_file):
        with open(uc_detail_file, encoding='utf-8') as f:
            uc_detail = json.load(f)

    # Criar ou atualizar a UC
    uc, created = UnidadeCurricular.objects.update_or_create(
        nome=uc_name,
        defaults={
            'ects': uc_plan.get('ects'),
            'ano_curricular': uc_plan.get('curricularYear'),
            'semestre': uc_plan.get('semester', ''),
            'objetivos': uc_detail.get('objectives', ''),
            'conteudos': uc_detail.get('programme', ''),
            'bibliografia': uc_detail.get('bibliography', ''),
            'apresentacao': uc_detail.get('presentation', ''),
            'licenciatura': lic,
        }
    )

    status = '✅ Criada' if created else 'ℹ️ Atualizada'
    print(f"  {status}: {uc.nome} ({uc.ects} ECTS, {uc.ano_curricular}º ano, {uc.semestre})")

print(f"\n=== Carregamento concluído! ===")
print(f"    Licenciatura: {lic.nome}")
print(f"    Docentes: {len(docentes_map)}")
print(f"    UCs: {len(flat_plan)}")
