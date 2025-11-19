import matplotlib.pyplot as plt
import json
import numpy as np
from datetime import datetime
import os

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

def carregar_dados():
    """Carrega os dados do arquivo JSON"""
    try:
        with open('dados_graficos.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("ERRO: Arquivo de dados não encontrado. Execute primeiro o processamento.")
        return None

def grafico_top_procedimentos(dados):
    """Gráfico dos top 10 procedimentos mais solicitados"""
    totais = dados['totais_globais']
    
    # Ordenar e pegar top 10
    top_10 = sorted(totais.items(), key=lambda x: x[1], reverse=True)[:10]
    procedimentos = [p[:30] + '...' if len(p) > 30 else p for p, _ in top_10]
    quantidades = [q for _, q in top_10]
    
    plt.figure(figsize=(12, 8))
    bars = plt.barh(procedimentos, quantidades, color='skyblue', edgecolor='navy')
    
    # Adicionar valores nas barras
    for bar, valor in zip(bars, quantidades):
        plt.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
                f'{valor}', ha='left', va='center', fontweight='bold')
    
    plt.xlabel('Número de Solicitações')
    plt.title('TOP 10 PROCEDIMENTOS MAIS SOLICITADOS\n(Todos os Bairros)', 
              fontsize=14, fontweight='bold', pad=20)
    plt.gca().invert_yaxis()
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig('grafico_top_procedimentos.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Gráfico 1: Top 10 procedimentos")

def grafico_distribuicao_bairros(dados):
    """Gráfico de distribuição por bairros"""
    bairros = list(dados['resumo_bairros'].keys())
    quantidades = list(dados['resumo_bairros'].values())
    
    # Ordenar por quantidade
    bairros_ordenados, quantidades_ordenadas = zip(*sorted(
        zip(bairros, quantidades), key=lambda x: x[1], reverse=True
    ))
    
    plt.figure(figsize=(14, 8))
    bars = plt.bar(bairros_ordenados, quantidades_ordenadas, 
                   color='lightcoral', edgecolor='darkred')
    
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Número de Solicitações')
    plt.title('DISTRIBUICAO DE SOLICITACOES POR BAIRRO', 
              fontsize=14, fontweight='bold', pad=20)
    
    # Adicionar valores no topo das barras
    for bar, valor in zip(bars, quantidades_ordenadas):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{valor}', ha='center', va='bottom', fontweight='bold')
    
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('grafico_distribuicao_bairros.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Gráfico 2: Distribuição por bairros")

def grafico_tempo_medio_procedimentos(dados):
    """Gráfico de tempo médio por tipo de procedimento"""
    tempos_por_procedimento = {}
    
    for bairro, procedimentos in dados['bairros_detalhados'].items():
        for proc, info in procedimentos.items():
            if proc not in tempos_por_procedimento:
                tempos_por_procedimento[proc] = []
            tempos_por_procedimento[proc].append(info['tempo_medio'])
    
    # Calcular média geral por procedimento
    medias = {proc: sum(tempos)/len(tempos) for proc, tempos in tempos_por_procedimento.items()}
    
    # Top 10 por tempo médio
    top_10_tempo = sorted(medias.items(), key=lambda x: x[1], reverse=True)[:10]
    procedimentos = [p[:25] + '...' if len(p) > 25 else p for p, _ in top_10_tempo]
    tempos = [t for _, t in top_10_tempo]
    
    plt.figure(figsize=(12, 8))
    bars = plt.barh(procedimentos, tempos, color='lightgreen', edgecolor='darkgreen')
    
    for bar, tempo in zip(bars, tempos):
        plt.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
                f'{tempo:.0f} dias', ha='left', va='center', fontweight='bold')
    
    plt.xlabel('Tempo Médio de Espera (dias)')
    plt.title('TOP 10 PROCEDIMENTOS COM MAIOR TEMPO MEDIO DE ESPERA', 
              fontsize=14, fontweight='bold', pad=20)
    plt.gca().invert_yaxis()
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig('grafico_tempo_medio.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Gráfico 3: Tempos médios de espera")

def grafico_pizza_totais(dados):
    """Gráfico de pizza com distribuição geral"""
    totais = dados['totais_globais']
    
    # Agrupar procedimentos menores em "Outros"
    if len(totais) > 8:
        sorted_totais = sorted(totais.items(), key=lambda x: x[1], reverse=True)
        principais = sorted_totais[:7]
        outros = sum(q for _, q in sorted_totais[7:])
        
        labels = [p[0][:15] + '...' if len(p[0]) > 15 else p[0] for p in principais]
        labels.append('Outros')
        sizes = [p[1] for p in principais] + [outros]
    else:
        labels = [p[:15] + '...' if len(p) > 15 else p for p in totais.keys()]
        sizes = list(totais.values())
    
    plt.figure(figsize=(12, 8))
    colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
    
    wedges, texts, autotexts = plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                      startangle=90, textprops={'fontsize': 9})
    
    # Melhorar aparência dos textos
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    plt.title('DISTRIBUICAO GERAL DE SOLICITACOES\n(Percentual por Tipo de Procedimento)', 
              fontsize=14, fontweight='bold', pad=20)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('grafico_pizza_geral.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Gráfico 4: Pizza de distribuição")

def grafico_comparativo_bairros(dados):
    """Gráfico comparativo entre bairros (top 5)"""
    bairros_totais = dados['resumo_bairros']
    top_5_bairros = sorted(bairros_totais.items(), key=lambda x: x[1], reverse=True)[:5]
    
    bairros_nomes = [b[0] for b in top_5_bairros]
    bairros_quantidades = [b[1] for b in top_5_bairros]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(bairros_nomes, bairros_quantidades, 
                   color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57'])
    
    plt.title('TOP 5 BAIRROS COM MAIS SOLICITACOES', 
              fontsize=14, fontweight='bold', pad=20)
    plt.ylabel('Número de Solicitações')
    
    # Adicionar valores nas barras
    for bar, valor in zip(bars, bairros_quantidades):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{valor}', ha='center', va='bottom', fontweight='bold')
    
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('grafico_top_bairros.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Gráfico 5: Top 5 bairros")

def criar_relatorio_visual():
    """Cria um relatório HTML com todos os gráficos"""
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Relatório Visual - Lista de Espera</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ text-align: center; background: #2c3e50; color: white; padding: 20px; }}
            .graph {{ margin: 30px 0; text-align: center; }}
            .graph img {{ max-width: 100%; height: auto; border: 1px solid #ddd; }}
            .info {{ background: #f8f9fa; padding: 15px; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>RELATORIO VISUAL - LISTA DE ESPERA</h1>
            <p>Municipio da Serra/ES - Gerado em {datetime.now().strftime('%d/%m/%Y as %H:%M')}</p>
        </div>
        
        <div class="info">
            <h3>ANALISES GRAFICAS DISPONIVEIS:</h3>
            <p>Este relatorio contem visualizacoes dos dados processados da lista de espera.</p>
        </div>
        
        <div class="graph">
            <h2>Top 10 Procedimentos Mais Solicitados</h2>
            <img src="grafico_top_procedimentos.png" alt="Top Procedimentos">
        </div>
        
        <div class="graph">
            <h2>Distribuicao por Bairros</h2>
            <img src="grafico_distribuicao_bairros.png" alt="Distribuicao Bairros">
        </div>
        
        <div class="graph">
            <h2>Maiores Tempos de Espera</h2>
            <img src="grafico_tempo_medio.png" alt="Tempo Medio">
        </div>
        
        <div class="graph">
            <h2>Distribuicao Geral</h2>
            <img src="grafico_pizza_geral.png" alt="Pizza Geral">
        </div>
        
        <div class="graph">
            <h2>Top 5 Bairros</h2>
            <img src="grafico_top_bairros.png" alt="Top Bairros">
        </div>
        
        <div class="info">
            <p><strong>DICA:</strong> Os graficos tambem foram salvos individualmente em PNG para uso em apresentacoes.</p>
        </div>
    </body>
    </html>
    """
    
    with open('relatorio_visual.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("   ✅ Relatorio HTML gerado")

def main():
    """Função principal"""
    print("GERANDO GRAFICOS COM MATPLOTLIB")
    print("=" * 50)
    
    dados = carregar_dados()
    if not dados:
        return
    
    print("Carregando dados...")
    print(f"   → {len(dados['totais_globais'])} tipos de procedimentos")
    print(f"   → {len(dados['bairros_detalhados'])} bairros analisados")
    print(f"   → {sum(dados['resumo_bairros'].values())} solicitacoes totais")
    
    print("\nCriando graficos...")
    
    grafico_top_procedimentos(dados)
    grafico_distribuicao_bairros(dados)
    grafico_tempo_medio_procedimentos(dados)
    grafico_pizza_totais(dados)
    grafico_comparativo_bairros(dados)
    criar_relatorio_visual()
    
    print("\nGRAFICOS GERADOS COM SUCESSO!")
    print("=" * 50)
    print("Arquivos criados:")
    print("   • grafico_top_procedimentos.png")
    print("   • grafico_distribuicao_bairros.png") 
    print("   • grafico_tempo_medio.png")
    print("   • grafico_pizza_geral.png")
    print("   • grafico_top_bairros.png")
    print("   • relatorio_visual.html")
    print("\nAbra 'relatorio_visual.html' no navegador para ver todos os graficos!")

if __name__ == "__main__":
    main()
