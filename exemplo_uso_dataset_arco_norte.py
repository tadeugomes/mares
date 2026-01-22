#!/usr/bin/env python3
"""
Exemplo de Uso do Dataset de Portos Híbridos do Arco Norte

Dataset: dados_historicos_portos_hibridos_arco_norte_v2.parquet

Este script demonstra como usar o dataset do Arco Norte que contém:
- Maré astronômica (Vila do Conde e Barcarena)
- Dados fluviais ANA (vazão e cota)
- Meteorologia INMET
- Precipitação na bacia
- Sazonalidade

Portos incluídos:
  1. Vila do Conde (PA) - Híbrido (maré + vazão)
  2. Barcarena (PA) - Híbrido (maré + vazão)
  3. Santarém (PA) - Fluvial puro (apenas vazão)
"""

import pandas as pd
import numpy as np
from datetime import datetime

def explorar_dataset_arco_norte():
    """Carrega e explora o dataset do Arco Norte"""

    print("=" * 80)
    print("EXPLORANDO DATASET - PORTOS HÍBRIDOS DO ARCO NORTE")
    print("=" * 80)

    # 1. Carregar dataset
    print("\n📂 Carregando dataset...")
    try:
        df = pd.read_parquet('dados_historicos_portos_hibridos_arco_norte_v2.parquet')
        print("✅ Dataset carregado com sucesso!")
    except FileNotFoundError:
        print("❌ Arquivo não encontrado!")
        print("   Certifique-se de que 'dados_historicos_portos_hibridos_arco_norte_v2.parquet'")
        print("   está no diretório atual.")
        return

    # 2. Informações gerais
    print("\n📊 INFORMAÇÕES GERAIS:")
    print(f"   Total de registros: {len(df):,}")
    print(f"   Período: {df['timestamp'].min()} até {df['timestamp'].max()}")
    print(f"   Colunas disponíveis ({len(df.columns)}):")
    for col in df.columns:
        print(f"     - {col}")

    # 3. Registros por porto
    print("\n🏢 REGISTROS POR PORTO:")
    contagem = df['station'].value_counts()
    for porto, count in contagem.items():
        tem_mare = df[df['station'] == porto]['tem_mare_astronomica'].iloc[0]
        tipo = "Híbrido (maré+vazão)" if tem_mare else "Fluvial puro (vazão)"
        print(f"   {porto}: {count:,} registros - {tipo}")

    # 4. Separar portos híbridos vs fluviais
    df_hibridos = df[df['tem_mare_astronomica'] == True].copy()
    df_fluviais = df[df['tem_mare_astronomica'] == False].copy()

    print(f"\n📌 Portos híbridos (com maré): {df_hibridos['station'].nunique()}")
    print(f"   {df_hibridos['station'].unique()}")
    print(f"\n📌 Portos fluviais puros (sem maré): {df_fluviais['station'].nunique()}")
    print(f"   {df_fluviais['station'].unique()}")

    # 5. Estatísticas de maré astronômica (apenas híbridos)
    if len(df_hibridos) > 0:
        print("\n🌊 ESTATÍSTICAS DE MARÉ ASTRONÔMICA (portos híbridos):")
        mare_stats = df_hibridos.groupby('station')['mare_astronomica_m'].describe()[['mean', 'min', 'max', 'std']]
        print(mare_stats)

    # 6. Estatísticas de vazão (todos os portos)
    print("\n🌊 ESTATÍSTICAS DE VAZÃO ANA (m³/s):")
    vazao_stats = df.groupby('station')['vazao_rio_m3s'].describe()[['mean', 'min', 'max', 'std']]
    print(vazao_stats)

    # 7. Estatísticas de cota (nível do rio)
    print("\n📏 ESTATÍSTICAS DE COTA DO RIO (m):")
    cota_stats = df.groupby('station')['cota_rio_m'].describe()[['mean', 'min', 'max', 'std']]
    print(cota_stats)

    # 8. Estatísticas meteorológicas
    print("\n🌬️  ESTATÍSTICAS METEOROLÓGICAS:")
    print("\nVelocidade do Vento (km/h):")
    print(df.groupby('station')['wind_speed_10m'].describe()[['mean', 'min', 'max', 'std']])

    print("\nPressão Atmosférica (hPa):")
    print(df.groupby('station')['pressure_msl'].describe()[['mean', 'min', 'max', 'std']])

    # 9. Estatísticas de precipitação
    print("\n🌧️  PRECIPITAÇÃO ACUMULADA 30 DIAS (mm):")
    precip_stats = df.groupby('station')['precip_bacia_30d_mm'].describe()[['mean', 'min', 'max', 'std']]
    print(precip_stats)

    # 10. Verificar dados faltantes
    print("\n⚠️  VERIFICAÇÃO DE DADOS FALTANTES:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    has_missing = False
    for col, pct in missing_pct.items():
        if pct > 0:
            has_missing = True
            print(f"   {col}: {pct:.2f}% ({missing[col]:,} registros)")

    if not has_missing:
        print("   ✅ Nenhum dado faltante!")

    return df


def analisar_porto_hibrido(df, porto='VilaDoCondePA'):
    """Análise detalhada de um porto híbrido (maré + vazão)"""

    print("\n" + "=" * 80)
    print(f"ANÁLISE DETALHADA: {porto} (Porto Híbrido)")
    print("=" * 80)

    df_porto = df[df['station'] == porto].copy()

    if len(df_porto) == 0:
        print(f"❌ Porto {porto} não encontrado no dataset!")
        return

    print(f"\n📊 Total de registros: {len(df_porto):,}")
    print(f"   Período: {df_porto['timestamp'].min()} até {df_porto['timestamp'].max()}")

    # 1. Maré astronômica
    print("\n🌊 MARÉ ASTRONÔMICA:")
    amplitude_mare = df_porto['mare_astronomica_m'].max() - df_porto['mare_astronomica_m'].min()
    print(f"   Mínima: {df_porto['mare_astronomica_m'].min():.3f} m")
    print(f"   Máxima: {df_porto['mare_astronomica_m'].max():.3f} m")
    print(f"   Amplitude: {amplitude_mare:.3f} m")
    print(f"   Média: {df_porto['mare_astronomica_m'].mean():.3f} m")

    # 2. Vazão do rio
    print("\n🌊 VAZÃO DO RIO (ANA):")
    print(f"   Mínima: {df_porto['vazao_rio_m3s'].min():,.0f} m³/s")
    print(f"   Máxima: {df_porto['vazao_rio_m3s'].max():,.0f} m³/s")
    print(f"   Média: {df_porto['vazao_rio_m3s'].mean():,.0f} m³/s")
    print(f"   Variação: {df_porto['vazao_rio_m3s'].max() - df_porto['vazao_rio_m3s'].min():,.0f} m³/s")

    # 3. Sazonalidade da vazão
    print("\n📅 SAZONALIDADE DA VAZÃO (média por mês):")
    vazao_mes = df_porto.groupby('mes')['vazao_rio_m3s'].mean()
    meses_nome = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                  'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

    for mes in range(1, 13):
        if mes in vazao_mes.index:
            nome_mes = meses_nome[mes-1]
            vazao = vazao_mes[mes]
            print(f"   {nome_mes}: {vazao:>10,.0f} m³/s")

    mes_max = vazao_mes.idxmax()
    mes_min = vazao_mes.idxmin()
    print(f"\n   🔼 Cheia (máx): {meses_nome[mes_max-1]} ({vazao_mes[mes_max]:,.0f} m³/s)")
    print(f"   🔽 Vazante (mín): {meses_nome[mes_min-1]} ({vazao_mes[mes_min]:,.0f} m³/s)")

    # 4. Comparação: magnitude maré vs vazão
    print("\n⚖️  IMPORTÂNCIA RELATIVA: MARÉ vs VAZÃO")
    print(f"   Amplitude maré: {amplitude_mare:.2f} m")
    variacao_vazao = df_porto['vazao_rio_m3s'].max() - df_porto['vazao_rio_m3s'].min()
    print(f"   Variação vazão: {variacao_vazao:,.0f} m³/s")
    print("\n   💡 Interpretação:")
    print("      Este é um porto HÍBRIDO: ambos os efeitos (maré E vazão)")
    print("      são importantes para prever o nível de água.")

    # 5. Vazão montante (propagação)
    print("\n🔄 PROPAGAÇÃO DE VAZÃO (estação montante):")
    print(f"   Vazão montante média: {df_porto['vazao_montante_m3s'].mean():,.0f} m³/s")

    # Calcular correlação com lag
    df_porto_sorted = df_porto.sort_values('timestamp').copy()
    correlacoes_lag = {}

    for lag_days in [1, 2, 3, 7, 14]:
        lag_hours = lag_days * 24
        df_porto_sorted[f'vazao_local_lag_{lag_days}d'] = df_porto_sorted['vazao_rio_m3s'].shift(lag_hours)
        corr = df_porto_sorted['vazao_montante_m3s'].corr(df_porto_sorted[f'vazao_local_lag_{lag_days}d'])
        correlacoes_lag[lag_days] = corr

    print("\n   Correlação vazão_montante → vazão_local (com lag):")
    for lag_days, corr in correlacoes_lag.items():
        if not np.isnan(corr):
            print(f"      Lag {lag_days:2d} dias: {corr:.3f}")

    best_lag = max(correlacoes_lag, key=lambda k: correlacoes_lag[k] if not np.isnan(correlacoes_lag[k]) else -1)
    print(f"\n   🎯 Melhor lag: {best_lag} dias (correlação {correlacoes_lag[best_lag]:.3f})")
    print(f"      Significado: Vazão em estação montante hoje → nível local em +{best_lag} dias")

    # 6. Precipitação
    print("\n🌧️  PRECIPITAÇÃO NA BACIA (acumulado 30 dias):")
    print(f"   Mínima: {df_porto['precip_bacia_30d_mm'].min():.1f} mm")
    print(f"   Máxima: {df_porto['precip_bacia_30d_mm'].max():.1f} mm")
    print(f"   Média: {df_porto['precip_bacia_30d_mm'].mean():.1f} mm")

    # 7. Recomendações para ML
    print("\n🎓 RECOMENDAÇÕES PARA MACHINE LEARNING:")
    print("   Features recomendadas (ordem de importância esperada):")
    print("   1. mare_astronomica_m (baseline - componente previsível)")
    print("   2. vazao_rio_m3s (componente fluvial local)")
    print(f"   3. vazao_montante_lag_{best_lag}d (propagação rio acima)")
    print("   4. precip_bacia_30d_mm (precipitação recente)")
    print("   5. sin_mes, cos_mes (sazonalidade)")
    print("   6. wind_speed_10m, pressure_msl (efeitos meteorológicos)")
    print("\n   💡 Este porto requer modelo HÍBRIDO que combine:")
    print("      - Maré astronômica (baseline)")
    print("      - Correção fluvial (vazão + precipitação)")
    print("      - Correção meteorológica (vento + pressão)")


def analisar_porto_fluvial(df, porto='SantaremPA'):
    """Análise detalhada de um porto fluvial puro (apenas vazão)"""

    print("\n" + "=" * 80)
    print(f"ANÁLISE DETALHADA: {porto} (Porto Fluvial Puro)")
    print("=" * 80)

    df_porto = df[df['station'] == porto].copy()

    if len(df_porto) == 0:
        print(f"❌ Porto {porto} não encontrado no dataset!")
        return

    print(f"\n📊 Total de registros: {len(df_porto):,}")
    print(f"   Período: {df_porto['timestamp'].min()} até {df_porto['timestamp'].max()}")

    # 1. Confirmação: sem maré astronômica
    tem_mare = df_porto['tem_mare_astronomica'].iloc[0]
    print(f"\n🌊 MARÉ ASTRONÔMICA: {'SIM' if tem_mare else 'NÃO'}")
    if not tem_mare:
        print("   ✅ Confirmado: Porto fluvial puro (maré desprezível < 5cm)")
        print("   💡 Modelo ML deve usar APENAS vazão/precipitação (NÃO incluir maré)")

    # 2. Vazão do rio
    print("\n🌊 VAZÃO DO RIO (ANA) - DOMINANTE:")
    print(f"   Mínima: {df_porto['vazao_rio_m3s'].min():,.0f} m³/s")
    print(f"   Máxima: {df_porto['vazao_rio_m3s'].max():,.0f} m³/s")
    print(f"   Média: {df_porto['vazao_rio_m3s'].mean():,.0f} m³/s")
    variacao = df_porto['vazao_rio_m3s'].max() - df_porto['vazao_rio_m3s'].min()
    print(f"   Variação: {variacao:,.0f} m³/s ({(variacao/df_porto['vazao_rio_m3s'].mean())*100:.0f}% da média)")

    # 3. Cota do rio
    print("\n📏 COTA DO RIO (nível medido - m):")
    print(f"   Mínima: {df_porto['cota_rio_m'].min():.2f} m")
    print(f"   Máxima: {df_porto['cota_rio_m'].max():.2f} m")
    print(f"   Amplitude: {df_porto['cota_rio_m'].max() - df_porto['cota_rio_m'].min():.2f} m")
    print(f"   Média: {df_porto['cota_rio_m'].mean():.2f} m")

    # 4. Sazonalidade da vazão
    print("\n📅 SAZONALIDADE DA VAZÃO (média por mês):")
    vazao_mes = df_porto.groupby('mes')['vazao_rio_m3s'].mean()
    cota_mes = df_porto.groupby('mes')['cota_rio_m'].mean()
    meses_nome = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                  'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

    print("\n   Mês    Vazão (m³/s)    Cota (m)")
    print("   " + "-" * 38)
    for mes in range(1, 13):
        if mes in vazao_mes.index:
            nome_mes = meses_nome[mes-1]
            vazao = vazao_mes[mes]
            cota = cota_mes[mes]
            print(f"   {nome_mes}   {vazao:>10,.0f}    {cota:>6.2f}")

    mes_max = vazao_mes.idxmax()
    mes_min = vazao_mes.idxmin()
    print(f"\n   🔼 CHEIA (máx): {meses_nome[mes_max-1]}")
    print(f"      Vazão: {vazao_mes[mes_max]:,.0f} m³/s | Cota: {cota_mes[mes_max]:.2f} m")
    print(f"   🔽 VAZANTE (mín): {meses_nome[mes_min-1]}")
    print(f"      Vazão: {vazao_mes[mes_min]:,.0f} m³/s | Cota: {cota_mes[mes_min]:.2f} m")

    # 5. Vazão montante (propagação)
    print("\n🔄 PROPAGAÇÃO DE VAZÃO (estação montante → local):")
    print(f"   Vazão montante média: {df_porto['vazao_montante_m3s'].mean():,.0f} m³/s")

    # Calcular correlação com lag
    df_porto_sorted = df_porto.sort_values('timestamp').copy()
    correlacoes_lag = {}

    for lag_days in [1, 2, 3, 4, 5, 7]:
        lag_hours = lag_days * 24
        df_porto_sorted[f'vazao_local_lag_{lag_days}d'] = df_porto_sorted['vazao_rio_m3s'].shift(lag_hours)
        corr = df_porto_sorted['vazao_montante_m3s'].corr(df_porto_sorted[f'vazao_local_lag_{lag_days}d'])
        correlacoes_lag[lag_days] = corr

    print("\n   Correlação vazão_montante → vazão_local (com lag):")
    for lag_days, corr in correlacoes_lag.items():
        if not np.isnan(corr):
            print(f"      Lag {lag_days} dias: {corr:.3f}")

    best_lag = max(correlacoes_lag, key=lambda k: correlacoes_lag[k] if not np.isnan(correlacoes_lag[k]) else -1)
    print(f"\n   🎯 Melhor lag: {best_lag} dias (correlação {correlacoes_lag[best_lag]:.3f})")
    print(f"      Significado: Onda de cheia propaga em ~{best_lag} dias")
    print(f"      Uso para previsão: Vazão montante hoje → nível local em +{best_lag} dias")

    # 6. Precipitação
    print("\n🌧️  PRECIPITAÇÃO NA BACIA (acumulado 30 dias):")
    print(f"   Mínima: {df_porto['precip_bacia_30d_mm'].min():.1f} mm")
    print(f"   Máxima: {df_porto['precip_bacia_30d_mm'].max():.1f} mm")
    print(f"   Média: {df_porto['precip_bacia_30d_mm'].mean():.1f} mm")

    # Correlação precipitação → vazão (com lags maiores: 15-30 dias)
    print("\n   Correlação precip_30d → vazão_rio (lag em dias):")
    for lag_days in [0, 7, 14, 21, 30]:
        lag_hours = lag_days * 24
        df_porto_sorted[f'vazao_lag_{lag_days}d'] = df_porto_sorted['vazao_rio_m3s'].shift(lag_hours)
        corr = df_porto_sorted['precip_bacia_30d_mm'].corr(df_porto_sorted[f'vazao_lag_{lag_days}d'])
        if not np.isnan(corr):
            print(f"      Lag {lag_days:2d} dias: {corr:.3f}")

    # 7. Recomendações para ML
    print("\n🎓 RECOMENDAÇÕES PARA MACHINE LEARNING:")
    print("   Features recomendadas (ordem de importância esperada):")
    print("   1. vazao_rio_m3s (dominante em rios)")
    print(f"   2. vazao_montante_lag_{best_lag}d (propagação de onda)")
    print("   3. precip_bacia_30d_mm (chuva recente)")
    print("   4. sin_mes, cos_mes (sazonalidade cheia/vazante)")
    print("   5. cota_rio_m (pode usar como target ou feature)")
    print("\n   ⚠️  NÃO incluir:")
    print("      ❌ mare_astronomica_m (seria apenas ruído)")
    print("      ❌ wave_height, wave_period (não existe em rio)")
    print("\n   💡 Este porto requer modelo HIDROLÓGICO PURO:")
    print("      - Vazão local + montante")
    print("      - Precipitação na bacia")
    print("      - Sazonalidade (ciclo anual Amazônia)")


def comparar_portos(df):
    """Comparação entre os 3 portos do Arco Norte"""

    print("\n" + "=" * 80)
    print("COMPARAÇÃO: PORTOS DO ARCO NORTE")
    print("=" * 80)

    # Criar resumo comparativo
    resumo = []

    for porto in df['station'].unique():
        df_porto = df[df['station'] == porto]

        info = {
            'Porto': porto,
            'Tipo': 'Híbrido' if df_porto['tem_mare_astronomica'].iloc[0] else 'Fluvial',
            'Vazão Média (m³/s)': f"{df_porto['vazao_rio_m3s'].mean():,.0f}",
            'Vazão Mín (m³/s)': f"{df_porto['vazao_rio_m3s'].min():,.0f}",
            'Vazão Máx (m³/s)': f"{df_porto['vazao_rio_m3s'].max():,.0f}",
            'Cota Amplitude (m)': f"{df_porto['cota_rio_m'].max() - df_porto['cota_rio_m'].min():.2f}",
        }

        if df_porto['tem_mare_astronomica'].iloc[0]:
            info['Maré Amplitude (m)'] = f"{df_porto['mare_astronomica_m'].max() - df_porto['mare_astronomica_m'].min():.3f}"
        else:
            info['Maré Amplitude (m)'] = 'N/A (< 0.05m)'

        resumo.append(info)

    df_resumo = pd.DataFrame(resumo)
    print("\n📊 RESUMO COMPARATIVO:")
    print(df_resumo.to_string(index=False))

    print("\n💡 INTERPRETAÇÃO:")
    print("   - Vila do Conde e Barcarena: HÍBRIDOS (maré + vazão)")
    print("   - Santarém: FLUVIAL PURO (apenas vazão)")
    print("\n   Todos têm vazão do Amazonas, mas importância da maré difere:")
    print("   - Híbridos: Modelo ML deve combinar maré astronômica + vazão")
    print("   - Fluvial: Modelo ML deve usar APENAS vazão + precipitação")


if __name__ == '__main__':
    # 1. Explorar dataset completo
    df = explorar_dataset_arco_norte()

    if df is not None:
        # 2. Analisar porto híbrido (Vila do Conde)
        analisar_porto_hibrido(df, porto='VilaDoCondePA')

        # 3. Analisar porto fluvial puro (Santarém)
        analisar_porto_fluvial(df, porto='SantaremPA')

        # 4. Comparação entre portos
        comparar_portos(df)

        print("\n" + "=" * 80)
        print("✅ ANÁLISE CONCLUÍDA!")
        print("=" * 80)
        print("\n💡 Próximos passos:")
        print("   1. Obter observações reais do nível de água (target para ML)")
        print("   2. Criar features adicionais (lags, sin/cos mês, etc.)")
        print("   3. Treinar modelos separados:")
        print("      - Modelo híbrido: Vila do Conde, Barcarena")
        print("      - Modelo fluvial: Santarém")
        print("   4. Validar modelos com dados holdout (últimos 6-12 meses)")
        print("\n📚 Para mais informações, consulte:")
        print("   - RECOMENDACOES_PORTOS_ARCO_NORTE.md")
        print("   - README.md (seção Dataset 3)")
