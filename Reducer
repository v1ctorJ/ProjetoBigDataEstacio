import sys
import json
from collections import defaultdict
import os

current_bairro = None
procedimentos_data = defaultdict(list)
total_global = defaultdict(int)
todos_bairros = []

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    try:
        bairro, grupo_procedimento, tempo_espera = line.split('\t')
        tempo_espera = int(tempo_espera)
        
        if current_bairro != bairro:
            if current_bairro:
                sorted_procedimentos = sorted(
                    [(proc, sum(tempos)//len(tempos), len(tempos)) 
                     for proc, tempos in procedimentos_data.items()],
                    key=lambda x: x[2],
                    reverse=True
                )
                todos_bairros.append((current_bairro, sorted_procedimentos))
                for proc, avg_time, count in sorted_procedimentos:
                    total_global[proc] += count
            
            current_bairro = bairro
            procedimentos_data = defaultdict(list)
        
        procedimentos_data[grupo_procedimento].append(tempo_espera)
    except ValueError:
        continue

if current_bairro:
    sorted_procedimentos = sorted(
        [(proc, sum(tempos)//len(tempos), len(tempos)) 
         for proc, tempos in procedimentos_data.items()],
        key=lambda x: x[2],
        reverse=True
    )
    todos_bairros.append((current_bairro, sorted_procedimentos))
    for proc, avg_time, count in sorted_procedimentos:
        total_global[proc] += count

# SALVAR DADOS PARA GRÁFICOS
dados_graficos = {
    'totais_globais': dict(total_global),
    'bairros_detalhados': {},
    'resumo_bairros': {}
}

for bairro, procedimentos in todos_bairros:
    dados_graficos['bairros_detalhados'][bairro] = {
        proc: {'quantidade': count, 'tempo_medio': avg} 
        for proc, avg, count in procedimentos
    }
    dados_graficos['resumo_bairros'][bairro] = sum(count for _, _, count in procedimentos)

# Salvar em arquivo JSON
with open('dados_graficos.json', 'w', encoding='utf-8') as f:
    json.dump(dados_graficos, f, ensure_ascii=False, indent=2)

# RELATÓRIO (código anterior mantido)
print("=" * 80)
print("RELATÓRIO POR BAIRRO - ORDEM DECRESCENTE DE SOLICITAÇÕES")
print("=" * 80)

for bairro, procedimentos in todos_bairros:
    total_bairro = sum(count for _, _, count in procedimentos)
    
    print(f"\n📊 BAIRRO: {bairro} (Total: {total_bairro} solicitações)")
    print("-" * 60)
    
    for i, (proc, avg_time, count) in enumerate(procedimentos, 1):
        print(f"  {i:2d}. {proc}")
        print(f"      📋 {count} solicitações | ⏳ Tempo médio: {avg_time} dias")

# ... (restante do código do relatório mantido)
