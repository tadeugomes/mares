#!/usr/bin/env python3
"""
Exemplo de Uso do Dataset Histórico Pronto
Dataset: portos_brasil_historico_portos_hibridos.parquet

Este script demonstra como usar o dataset histórico pré-processado
que contém dados meteorológicos e maré astronômica para Rio Grande,
Paranaguá e Antonina (2020-2024).
"""

import pandas as pd
import matplotlib.pyplot as plt

def explorar_dataset():
    """Carrega e explora o dataset histórico"""

    print("=" * 60)
    print("EXPLORANDO DATASET HISTÓRICO - PORTOS HÍBRIDOS")
    print("=" * 60)

    # 1. Carregar dataset
    print("\n📂 Carregando dataset...")
    try:
        df = pd.read_parquet('portos_brasil_historico_portos_hibridos.parquet')
        print("✅ Dataset carregado com sucesso!")
    except FileNotFoundError:
        print("❌ Arquivo não encontrado!")
        print("   Certifique-se de que 'portos_brasil_historico_portos_hibridos.parquet'")
        print("   está no diretório atual.")
        return

    # 2. Informações gerais
    print("\n📊 INFORMAÇÕES GERAIS:")
    print(f"   Total de registros: {len(df):,}")
    print(f"   Período: {df['timestamp'].min()} até {df['timestamp'].max()}")
    print(f"   Colunas: {', '.join(df.columns)}")

    # 3. Registros por porto
    print("\n🏢 REGISTROS POR PORTO:")
    contagem = df['station'].value_counts()
    for porto, count in contagem.items():
        print(f"   {porto}: {count:,} registros")

    # 4. Estatísticas por variável
    print("\n📈 ESTATÍSTICAS POR VARIÁVEL:")
    print("\nMaré Astronômica (m):")
    print(df.groupby('station')['mare_astronomica'].describe()[['mean', 'min', 'max', 'std']])

    print("\nVelocidade do Vento (m/s):")
    print(df.groupby('station')['wind_speed'].describe()[['mean', 'min', 'max', 'std']])

    print("\nPressão Atmosférica (mB):")
    print(df.groupby('station')['press'].describe()[['mean', 'min', 'max', 'std']])

    # 5. Verificar dados faltantes
    print("\n⚠️  DADOS FALTANTES:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    for col, pct in missing_pct.items():
        if pct > 0:
            print(f"   {col}: {pct:.2f}% ({missing[col]:,} registros)")

    if missing.sum() == 0:
        print("   ✅ Nenhum dado faltante!")

    # 6. Exemplo de uso para um porto específico
    print("\n" + "=" * 60)
    print("EXEMPLO: ANÁLISE DO PORTO DE PARANAGUÁ")
    print("=" * 60)

    df_paranagua = df[df['station'] == 'Paranagua'].copy()

    print(f"\n📊 Total de registros: {len(df_paranagua):,}")

    # Calcular features de vento sul
    df_paranagua['vento_sul'] = (
        (df_paranagua['wind_dir'] >= 135) &
        (df_paranagua['wind_dir'] <= 225)
    ).astype(int)

    vento_sul_count = df_paranagua['vento_sul'].sum()
    vento_sul_pct = (vento_sul_count / len(df_paranagua)) * 100

    print(f"🌬️  Vento sul: {vento_sul_count:,} horas ({vento_sul_pct:.1f}% do tempo)")
    print(f"   Velocidade média vento sul: {df_paranagua[df_paranagua['vento_sul']==1]['wind_speed'].mean():.2f} m/s")

    # Amplitude de maré
    amplitude = df_paranagua['mare_astronomica'].max() - df_paranagua['mare_astronomica'].min()
    print(f"\n🌊 Maré astronômica:")
    print(f"   Mínima: {df_paranagua['mare_astronomica'].min():.2f} m")
    print(f"   Máxima: {df_paranagua['mare_astronomica'].max():.2f} m")
    print(f"   Amplitude: {amplitude:.2f} m")

    # Sazonalidade da precipitação
    df_paranagua['mes'] = pd.to_datetime(df_paranagua['timestamp']).dt.month
    precip_mes = df_paranagua.groupby('mes')['precip'].sum()
    mes_mais_chuvoso = precip_mes.idxmax()
    print(f"\n🌧️  Precipitação:")
    print(f"   Total acumulado: {df_paranagua['precip'].sum():.1f} mm")
    print(f"   Mês mais chuvoso: {mes_mais_chuvoso} ({precip_mes[mes_mais_chuvoso]:.1f} mm)")

    # 7. Dicas de uso
    print("\n" + "=" * 60)
    print("💡 DICAS DE USO PARA MACHINE LEARNING")
    print("=" * 60)

    print("""
    ✅ O que ESTÁ incluído neste dataset:
       - Maré astronômica (simplificada com 4 componentes)
       - Dados meteorológicos completos (vento, pressão, precipitação)
       - Vazão fluvial estimada
       - Período: 2020-2024 (5 anos)

    ❌ O que NÃO está incluído (você precisa obter):
       - Nível de água OBSERVADO (target para treinar o modelo)
       - Para produção: vazão fluvial real (ANA telemetria)

    📝 Próximos passos:
       1. Obter observações reais do nível de água (porto/ANA/Marinha)
       2. Fazer merge com este dataset por timestamp
       3. Treinar modelo de ML
       4. Para maior precisão: substituir 'mare_astronomica' pelos CSVs
          de alta precisão gerados pelos scripts Python deste projeto

    🔗 Código exemplo:
       df_obs = pd.read_csv('observacoes_paranagua.csv')
       df_completo = pd.merge(df_paranagua, df_obs, on='timestamp')

       features = ['mare_astronomica', 'wind_speed', 'press', 'vazao_fluvial']
       X = df_completo[features]
       y = df_completo['nivel_observado']

       # Treinar modelo...
    """)

def comparar_portos():
    """Compara características entre os três portos"""

    print("\n" + "=" * 60)
    print("COMPARAÇÃO ENTRE PORTOS")
    print("=" * 60)

    try:
        df = pd.read_parquet('portos_brasil_historico_portos_hibridos.parquet')
    except FileNotFoundError:
        print("❌ Arquivo não encontrado!")
        return

    # Comparação de amplitudes de maré
    print("\n🌊 AMPLITUDE DE MARÉ:")
    for porto in df['station'].unique():
        df_porto = df[df['station'] == porto]
        amplitude = df_porto['mare_astronomica'].max() - df_porto['mare_astronomica'].min()
        print(f"   {porto:15s}: {amplitude:.2f} m")

    # Comparação de vento médio
    print("\n🌬️  VELOCIDADE MÉDIA DO VENTO:")
    vento_medio = df.groupby('station')['wind_speed'].mean()
    for porto, vel in vento_medio.items():
        print(f"   {porto:15s}: {vel:.2f} m/s")

    # Comparação de rajadas máximas
    print("\n💨 RAJADA MÁXIMA REGISTRADA:")
    rajada_max = df.groupby('station')['wind_gust'].max()
    for porto, rajada in rajada_max.items():
        print(f"   {porto:15s}: {rajada:.1f} m/s")

    # Comparação de precipitação total
    print("\n🌧️  PRECIPITAÇÃO ACUMULADA (2020-2024):")
    precip_total = df.groupby('station')['precip'].sum()
    for porto, precip in precip_total.items():
        print(f"   {porto:15s}: {precip:.0f} mm")

def exemplo_preparacao_ml():
    """Mostra como preparar dados para ML"""

    print("\n" + "=" * 60)
    print("EXEMPLO: PREPARAÇÃO PARA MACHINE LEARNING")
    print("=" * 60)

    try:
        df = pd.read_parquet('portos_brasil_historico_portos_hibridos.parquet')
    except FileNotFoundError:
        print("❌ Arquivo não encontrado!")
        return

    # Filtrar porto
    df_porto = df[df['station'] == 'Paranagua'].copy()

    print(f"\n1️⃣  Filtrado porto: Paranaguá ({len(df_porto):,} registros)")

    # Criar features adicionais
    df_porto['hora'] = pd.to_datetime(df_porto['timestamp']).dt.hour
    df_porto['mes'] = pd.to_datetime(df_porto['timestamp']).dt.month
    df_porto['dia_semana'] = pd.to_datetime(df_porto['timestamp']).dt.dayofweek

    # Vento sul
    df_porto['vento_sul'] = (
        (df_porto['wind_dir'] >= 135) &
        (df_porto['wind_dir'] <= 225)
    ).astype(int)
    df_porto['vento_sul_vel'] = df_porto['wind_speed'] * df_porto['vento_sul']

    # Rolling features
    df_porto['wind_speed_max_24h'] = df_porto['wind_speed'].rolling(window=24, min_periods=1).max()
    df_porto['precip_acum_24h'] = df_porto['precip'].rolling(window=24, min_periods=1).sum()

    print("2️⃣  Features criadas:")
    print("   - Temporais: hora, mes, dia_semana")
    print("   - Vento sul: vento_sul, vento_sul_vel")
    print("   - Rolling: wind_speed_max_24h, precip_acum_24h")

    # Lista de features para ML
    features_ml = [
        'mare_astronomica',
        'wind_speed',
        'wind_dir',
        'wind_gust',
        'press',
        'precip',
        'vazao_fluvial',
        'hora',
        'mes',
        'vento_sul',
        'vento_sul_vel',
        'wind_speed_max_24h',
        'precip_acum_24h'
    ]

    print(f"\n3️⃣  Total de features preparadas: {len(features_ml)}")
    print(f"   Features: {', '.join(features_ml)}")

    # Verificar correlações
    print("\n4️⃣  Correlações com maré astronômica:")
    correlacoes = df_porto[features_ml].corr()['mare_astronomica'].sort_values(ascending=False)
    print(correlacoes.head(10))

    print("\n⚠️  PRÓXIMO PASSO CRÍTICO:")
    print("   Você precisa obter observações REAIS do nível de água!")
    print("   Fontes: Porto de Paranaguá, Marinha do Brasil, ou ANA")
    print("   Arquivo exemplo: observacoes_paranagua_2020_2024.csv")
    print("\n   Depois:")
    print("   df_obs = pd.read_csv('observacoes_paranagua_2020_2024.csv')")
    print("   df_final = pd.merge(df_porto, df_obs, on='timestamp', how='inner')")
    print("   X = df_final[features_ml]")
    print("   y = df_final['nivel_observado']")

if __name__ == '__main__':
    # Executar todas as análises
    explorar_dataset()
    comparar_portos()
    exemplo_preparacao_ml()

    print("\n" + "=" * 60)
    print("✅ Análise concluída!")
    print("=" * 60)
