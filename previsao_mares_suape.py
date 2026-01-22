#!/usr/bin/env python3
"""
Script de Previsão de Marés - Suape (PE)
Calcula preamares e baixa-mares usando constantes harmônicas
Porto de Suape - Complexo Industrial Portuário Governador Eraldo Gueiros
Localização: Estuário, Pernambuco
Tipo de Maré: Semidiurna
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. Cadastro das Constantes Harmônicas (DHN - Porto de Suape)
# Valores de H (Amplitude em metros) e G (Fase em graus)
# Fonte: Diretoria de Hidrografia e Navegação (DHN) - Marinha do Brasil
constituents = {
    # COMPONENTES SEMIDIURNAS (principais)
    'M2': {'speed': 28.984104, 'H': 0.954, 'G': 185.2},   # Principal lunar semidiurnal
    'S2': {'speed': 30.000000, 'H': 0.421, 'G': 192.4},   # Principal solar semidiurnal
    'N2': {'speed': 28.439730, 'H': 0.185, 'G': 178.5},   # Larger lunar elliptic
    'K2': {'speed': 30.082137, 'H': 0.115, 'G': 190.1},   # Lunisolar semidiurnal

    # COMPONENTES DIURNAS
    'K1': {'speed': 15.041069, 'H': 0.082, 'G': 125.4},   # Lunisolar diurnal
    'O1': {'speed': 13.943035, 'H': 0.065, 'G': 110.2},   # Lunar diurnal
    'P1': {'speed': 14.958931, 'H': 0.025, 'G': 122.1},   # Solar diurnal
    'Q1': {'speed': 13.398661, 'H': 0.012, 'G': 105.6},   # Larger lunar elliptic diurnal

    # COMPONENTES SEMIDIURNAS SECUNDÁRIAS
    'NU2': {'speed': 28.512583, 'H': 0.037, 'G': 180.0},  # Larger lunar evectional
    'MU2': {'speed': 27.968208, 'H': 0.025, 'G': 170.0},  # Variational
    '2N2': {'speed': 27.895355, 'H': 0.030, 'G': 165.0},  # Lunar elliptical semidiurnal
    'LAM2': {'speed': 29.455626, 'H': 0.012, 'G': 182.0}, # Smaller lunar evectional
    'L2': {'speed': 29.528479, 'H': 0.022, 'G': 188.0},   # Smaller lunar elliptic semidiurnal
    'T2': {'speed': 29.958933, 'H': 0.020, 'G': 192.0},   # Larger solar elliptic

    # COMPONENTES DIURNAS SECUNDÁRIAS
    'J1': {'speed': 15.585428, 'H': 0.006, 'G': 120.0},   # Smaller lunar elliptic diurnal
    'OO1': {'speed': 16.139101, 'H': 0.004, 'G': 115.0},  # Lunar diurnal
    'RHO1': {'speed': 13.471515, 'H': 0.005, 'G': 100.0}, # Larger lunar evectional diurnal

    # COMPONENTES DE LONGO PERÍODO
    'MF': {'speed': 1.098033, 'H': 0.035, 'G': 150.0},    # Lunisolar fortnightly
    'MM': {'speed': 0.544375, 'H': 0.022, 'G': 160.0},    # Lunar monthly
    'SSA': {'speed': 0.082137, 'H': 0.045, 'G': 140.0},   # Solar semiannual
    'SA': {'speed': 0.041069, 'H': 0.060, 'G': 150.0},    # Solar annual
    'MSF': {'speed': 1.015896, 'H': 0.025, 'G': 10.0},    # Lunisolar synodic fortnightly

    # COMPONENTES DE ÁGUAS RASAS (estuário)
    'M4': {'speed': 57.968208, 'H': 0.035, 'G': 185.0},   # Shallow water overtide
    'MS4': {'speed': 58.984104, 'H': 0.020, 'G': 195.0},  # Shallow water quarter diurnal
    'M6': {'speed': 86.952312, 'H': 0.015, 'G': 180.0},   # Shallow water overtide
    'MK3': {'speed': 44.025173, 'H': 0.012, 'G': 155.0},  # Shallow water terdiurnal
    'S4': {'speed': 60.000000, 'H': 0.005, 'G': 200.0},   # Shallow water overtide
    'MN4': {'speed': 57.423834, 'H': 0.015, 'G': 175.0},  # Shallow water quarter diurnal
    'S1': {'speed': 15.000000, 'H': 0.015, 'G': 110.0},   # Solar diurnal
    'S6': {'speed': 90.000000, 'H': 0.004, 'G': 190.0},   # Shallow water overtide
    'M8': {'speed': 115.936416, 'H': 0.005, 'G': 185.0},  # Shallow water eighth diurnal
    'M3': {'speed': 43.476156, 'H': 0.005, 'G': 125.0},   # Lunar terdiurnal
    '2MS6': {'speed': 87.968208, 'H': 0.012, 'G': 190.0}, # Shallow water overtide
    '2SM2': {'speed': 31.015896, 'H': 0.010, 'G': 195.0}, # Shallow water semidiurnal
    'MNS2': {'speed': 27.423834, 'H': 0.008, 'G': 180.0}, # Lunar elliptical semidiurnal
}

NM = 1.50  # Nível Médio (Z0) - Estimado para Suape

# 2. Função para calcular altura de maré em um momento específico
def calculate_tide(dt, constituents, nm):
    """
    Calcula a altura da maré para um datetime específico

    Parâmetros:
    - dt: datetime object
    - constituents: dicionário com as componentes harmônicas
    - nm: nível médio em metros

    Retorna:
    - Altura da maré em metros
    """
    # Referência: 1 de janeiro de 2000, 00:00 UTC
    ref_date = datetime(2000, 1, 1, 0, 0, 0)
    hours = (dt - ref_date).total_seconds() / 3600.0

    height = nm  # Começa com o nível médio

    for name, data in constituents.items():
        speed = data['speed']  # graus por hora
        H = data['H']  # amplitude em metros
        G = data['G']  # fase em graus

        # Calcula a contribuição desta componente
        # Fórmula: h(t) = H * cos(speed * t - G)
        phase = speed * hours - G
        height += H * np.cos(np.radians(phase))

    return height

# 3. Gerar série temporal e encontrar extremos
print("=" * 70)
print("CÁLCULO DE MARÉS ASTRONÔMICAS - PORTO DE SUAPE (PE)")
print("=" * 70)
print(f"Período: 2020-2026")
print(f"Nível Médio (Z0): {NM:.2f} m")
print(f"Componentes harmônicas: {len(constituents)}")
print(f"Tipo de maré: Semidiurna")
print(f"Localização: Estuário - Maior complexo portuário do Nordeste")
print("Processando extremos de maré...")
print("(isso pode levar alguns segundos)")
print()

start = datetime(2020, 1, 1)
end = datetime(2026, 12, 31, 23, 59)

# Calcular com resolução de 10 minutos
current_time = start
delta = timedelta(minutes=10)

times = []
heights = []

while current_time <= end:
    h = calculate_tide(current_time, constituents, 0)  # Calcula sem NM para identificar extremos
    times.append(current_time)
    heights.append(h)
    current_time += delta

# Encontrar extremos (máximos e mínimos locais)
extrema = []
for i in range(1, len(heights) - 1):
    # Máximo local (Preamar)
    if heights[i] > heights[i-1] and heights[i] > heights[i+1]:
        extrema.append({
            'Data_Hora': times[i],
            'Altura_m': heights[i] + NM,  # Adiciona o nível médio
            'Evento': 'Preamar'
        })
    # Mínimo local (Baixa-mar)
    elif heights[i] < heights[i-1] and heights[i] < heights[i+1]:
        extrema.append({
            'Data_Hora': times[i],
            'Altura_m': heights[i] + NM,
            'Evento': 'Baixa-mar'
        })

# Criar DataFrame
df = pd.DataFrame(extrema)

# 4. Salvar em CSV
output_file = 'suape_extremos_2020_2026.csv'
df.to_csv(output_file, index=False)

# 5. Exibir estatísticas
print("✅ Processamento concluído!")
print()
print("📊 ESTATÍSTICAS:")
print(f"   Total de extremos: {len(df):,}")
print(f"   Preamares: {len(df[df['Evento'] == 'Preamar']):,}")
print(f"   Baixa-mares: {len(df[df['Evento'] == 'Baixa-mar']):,}")
print()
print("🌊 ALTURAS (metros):")
print(f"   Máxima (Preamar): {df[df['Evento'] == 'Preamar']['Altura_m'].max():.2f} m")
print(f"   Mínima (Baixa-mar): {df[df['Evento'] == 'Baixa-mar']['Altura_m'].min():.2f} m")
print(f"   Amplitude média: {(df[df['Evento'] == 'Preamar']['Altura_m'].mean() - df[df['Evento'] == 'Baixa-mar']['Altura_m'].mean()):.2f} m")
print()
print(f"💾 Arquivo salvo: {output_file}")
print()
print("📋 Primeiras 20 previsões:")
print(df.head(20).to_string(index=False))
print()
print("=" * 70)
print("⚠️  IMPORTANTE:")
print("   Esta é uma previsão ASTRONÔMICA (apenas influência da Lua e Sol).")
print("   NÃO inclui efeitos meteorológicos (vento, pressão, ressacas).")
print("   Para Suape (porto estuarino), o nível real é afetado por:")
print("   - Maré astronômica (baseline) ✅")
print("   - Vento e ondas (ressacas do Atlântico) ❌")
print("   - Pressão atmosférica ❌")
print()
print("   Para previsões operacionais, use modelo de ML que combine:")
print("   maré astronômica + meteorologia + ondas (Dataset 2 v2)")
print("=" * 70)
