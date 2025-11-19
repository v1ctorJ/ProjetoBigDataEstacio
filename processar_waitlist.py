import subprocess
import os
import pandas as pd
from datetime import datetime

def extrair_dados_pdf():
    """Extrai dados do PDF para formato processável"""
    print("📄 Extraindo dados do PDF...")
    
    cmd = "pdftotext -layout 'Lista de espera julho 2025.pdf' - | grep -E '^[0-9]' > dados_extraidos.txt"
    result = os.system(cmd)
    
    if result == 0:
        with open('dados_extraidos.txt', 'r') as f:
            lines = f.readlines()
        print(f"✅ Dados extraídos: {len(lines)} registros")
    else:
        print("❌ Erro na extração do PDF")

def processar_hadoop():
    """Executa o processamento Hadoop"""
    print("\n🔄 Iniciando processamento Hadoop...")
    
    try:
        subprocess.run(["hadoop", "version"], check=True, capture_output=True)
    except:
        print("❌ Hadoop não está configurado, usando processamento local...")
        processar_local()
        return
    
    commands = [
        "hdfs dfs -rm -r /user/waitlist 2>/dev/null || true",
        "hdfs dfs -mkdir -p /user/waitlist",
        "hdfs dfs -put dados_extraidos.txt /user/waitlist/",
        "hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar " +
        "-files mapper.py,reducer.py " +
        "-mapper mapper.py " +
        "-reducer reducer.py " +
        "-input /user/waitlist/dados_extraidos.txt " +
        "-output /user/waitlist/resultado"
    ]
    
    for cmd in commands:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0 and "rm" not in cmd:
                print(f"❌ Erro no Hadoop, usando processamento local...")
                processar_local()
                return
        except Exception as e:
            print(f"❌ Erro no Hadoop: {e}")
            processar_local()
            return
    
    gerar_relatorio_hadoop()

def processar_local():
    """Processamento local sem Hadoop"""
    print("🖥️  Executando processamento local...")
    
    cmd = "cat dados_extraidos.txt | python3 mapper.py | sort | python3 reducer.py"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        filename = f"relatorio_completo_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        with open(filename, "w") as f:
            f.write("RELATÓRIO COMPLETO - SOLICITAÇÕES POR BAIRRO\n")
            f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
            f.write("="*80 + "\n")
            f.write(result.stdout)
        
        print(f"✅ Relatório salvo: {filename}")
        print("\n" + "="*80)
        print("📊 RESUMO DO RELATÓRIO:")
        print("="*80)
        print(result.stdout)
    else:
        print("❌ Erro no processamento local")

def gerar_relatorio_hadoop():
    """Gera relatório a partir do Hadoop"""
    print("\n📋 Gerando relatório final...")
    
    cmd = "hdfs dfs -cat /user/waitlist/resultado/part-00000"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        filename = f"relatorio_completo_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        with open(filename, "w") as f:
            f.write("RELATÓRIO COMPLETO - SOLICITAÇÕES POR BAIRRO\n")
            f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
            f.write("="*80 + "\n")
            f.write(result.stdout)
        
        print(f"✅ Relatório salvo: {filename}")
        print("\n" + "="*80)
        print("📊 RESUMO DO RELATÓRIO:")
        print("="*80)
        print(result.stdout)
    else:
        print("❌ Erro ao recuperar resultados do Hadoop")

def gerar_graficos():
    """Gera gráficos com matplotlib"""
    print("\n🎨 Gerando gráficos...")
    
    try:
        # Verificar se matplotlib está instalado
        subprocess.run(["python3", "-c", "import matplotlib"], 
                      check=True, capture_output=True)
    except:
        print("❌ matplotlib não instalado. Instalando...")
        subprocess.run(["pip3", "install", "matplotlib"], check=True)
    
    # Executar gerador de gráficos
    result = subprocess.run(["python3", "gerar_graficos.py"], 
                           capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Gráficos gerados com sucesso!")
        print("📊 Ver arquivos .png e relatorio_visual.html")
    else:
        print("❌ Erro ao gerar gráficos:")
        print(result.stderr)


def gerar_graficos():
    """Gera gráficos com matplotlib"""
    print("\n🎨 Gerando gráficos...")

    try:
        # Verificar se matplotlib está instalado
        subprocess.run(["python3", "-c", "import matplotlib"],
                       check=True, capture_output=True)
    except:
        print("❌ matplotlib não instalado. Instalando...")
        subprocess.run(["pip3", "install", "matplotlib"], check=True)

    # Executar gerador de gráficos
    result = subprocess.run(["python3", "gerar_graficos.py"],
                            capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ Gráficos gerados com sucesso!")
        print("📊 Ver arquivos .png e relatorio_visual.html")
    else:
        print("❌ Erro ao gerar gráficos:")
        print(result.stderr)

if __name__ == "__main__":
    print("🚀 PROCESSANDO LISTA DE ESPERA - SERRA/ES")
    print("📊 Agora com Grupos de Procedimento e Totais Globais")
    
    extrair_dados_pdf()
    processar_hadoop()
    gerar_graficos()
