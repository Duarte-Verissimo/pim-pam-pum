import os
import sys
import django
import json

# Adicionar a pasta raiz ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from portfolio.models import TFC, Tecnologia, TipoTecnologia, Docente, Licenciatura

print("=== A iniciar importação dos TFCs a partir do JSON ===\n")

# Limpar TFCs existentes (opcional — descomenta se quiseres resetar)
# TFC.objects.all().delete()

with open('data/tfcs_2025.json', encoding='utf-8') as f:
    tfcs = json.load(f)

    # tfcs é uma lista de dicionários,
    # cada dicionário tendo informação de um TFC

    print(f"Encontrados {len(tfcs)} TFCs no ficheiro JSON.\n")

    for tfc_data in tfcs:
        # ---- Resolver FK: Licenciatura ----
        licenciatura_nome = tfc_data.get('licenciatura', '')
        licenciatura = None
        if licenciatura_nome:
            licenciatura, _ = Licenciatura.objects.get_or_create(
                nome=licenciatura_nome,
                defaults={
                    'sigla': '',
                    'departamento': 'DEISI',
                }
            )

        # ---- Resolver palavras_chave (lista → string separada por vírgulas) ----
        palavras_chave_list = tfc_data.get('palavras_chave', [])
        # Limpar pontos finais dos valores
        palavras_chave = ', '.join([p.rstrip('.') for p in palavras_chave_list])

        # ---- Resolver areas (lista → string separada por vírgulas) ----
        areas_list = tfc_data.get('areas', [])
        areas = ', '.join([a.rstrip('.') for a in areas_list])

        # ---- Criar o TFC ----
        tfc, created = TFC.objects.get_or_create(
            titulo=tfc_data['titulo'],
            defaults={
                'resumo': tfc_data.get('resumo', ''),
                'imagem_url': tfc_data.get('imagem', ''),
                'pdf_url': tfc_data.get('pdf_url', ''),
                'nivel_interesse': tfc_data.get('rating', 3),
                'parceiro': tfc_data.get('parceiro', '') or '',
                'palavras_chave': palavras_chave,
                'areas': areas,
                'licenciatura': licenciatura,
            }
        )

        # ---- Resolver M:N: Tecnologias ----
        tecnologias_list = tfc_data.get('tecnologias', [])
        tipo_outros, _ = TipoTecnologia.objects.get_or_create(nome='Outros')
        for tec_nome in tecnologias_list:
            tec_nome_limpo = tec_nome.rstrip('.')  # Remove pontos finais
            tec, _ = Tecnologia.objects.get_or_create(
                nome=tec_nome_limpo,
                defaults={
                    'tipo': tipo_outros,
                    'nivel_interesse': 3,
                }
            )
            tfc.tecnologias.add(tec)

        # ---- Resolver M:N: Orientadores (Docentes) ----
        orientadores_str = tfc_data.get('orientador', '')
        if orientadores_str:
            # O campo pode ter múltiplos orientadores separados por vírgula
            orientadores_nomes = [nome.strip() for nome in orientadores_str.split(',')]
            for nome_orientador in orientadores_nomes:
                docente, _ = Docente.objects.get_or_create(
                    nome=nome_orientador,
                    defaults={}
                )
                tfc.orientadores.add(docente)

        status = '✅ Criado' if created else 'ℹ️ Já existia'
        print(f"   {status}: {tfc.titulo[:80]}...")

print(f"\n=== Importação concluída! Total: {len(tfcs)} TFCs processados ===")
