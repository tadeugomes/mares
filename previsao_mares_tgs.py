#!/usr/bin/env python3
"""
Script de Previsão de Marés - Terminal Gás Sul
Calcula preamares e baixa-mares usando constantes harmônicas
Ficha 60266 - Terminal Gás Sul, São Francisco do Sul (SC)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. Cadastro das Constantes Harmônicas (Ficha 60266 - Terminal Gás Sul)
# Valores de H (Amplitude em metros) e G (Fase em graus)
constituents = {
    'M2': {'speed': 28.984104, 'H': 0.286, 'G': 77.26},    # Principal lunar semidiurnal
    'S2': {'speed': 30.000000, 'H': 0.245, 'G': 78.33},    # Principal solar semidiurnal
    'O1': {'speed': 13.943035, 'H': 0.117, 'G': 45.42},    # Lunar diurnal
    'K1': {'speed': 15.041069, 'H': 0.180, 'G': 54.76},    # Lunisolar diurnal
    'N2': {'speed': 28.439730, 'H': 0.052, 'G': 57.08},    # Larger lunar elliptic
    'M4': {'speed': 57.968208, 'H': 0.016, 'G': 215.11},   # Shallow water overtide
    'MS4': {'speed': 58.984104, 'H': 0.017, 'G': 237.95},  # Shallow water quarter diurnal
    'M6': {'speed': 86.952312, 'H': 0.012, 'G': 194.57},   # Shallow water overtide
    'MK3': {'speed': 44.025173, 'H': 0.007, 'G': 185.73},  # Shallow water terdiurnal
    'S4': {'speed': 60.000000, 'H': 0.005, 'G': 305.86},   # Shallow water overtide
    'MN4': {'speed': 57.423834, 'H': 0.005, 'G': 172.50},  # Shallow water quarter diurnal
    'NU2': {'speed': 28.512583, 'H': 0.011, 'G': 51.52},   # Larger lunar evectional
    'S1': {'speed': 15.000000, 'H': 0.027, 'G': 26.27},    # Solar diurnal
    'MU2': {'speed': 27.968208, 'H': 0.010, 'G': 24.38},   # Variational
    '2N2': {'speed': 27.895355, 'H': 0.007, 'G': 36.89},   # Lunar elliptical semidiurnal
    'OO1': {'speed': 16.139101, 'H': 0.006, 'G': 64.09},   # Lunar diurnal
    'LAM2': {'speed': 29.455626, 'H': 0.002, 'G': 116.82}, # Smaller lunar evectional
    'S6': {'speed': 90.000000, 'H': 0.005, 'G': 306.96},   # Shallow water overtide
    'M8': {'speed': 115.936416, 'H': 0.004, 'G': 273.66},  # Shallow water eighth diurnal
    'M3': {'speed': 43.476156, 'H': 0.004, 'G': 335.70},   # Lunar terdiurnal
    'MF': {'speed': 1.098033, 'H': 0.038, 'G': 301.99},    # Lunisolar fortnightly
    'MM': {'speed': 0.544375, 'H': 0.024, 'G': 226.54},    # Lunar monthly
    'SSA': {'speed': 0.082137, 'H': 0.063, 'G': 172.90},   # Solar semiannual
    'SA': {'speed': 0.041069, 'H': 0.084, 'G': 184.81},    # Solar annual
    'MSF': {'speed': 1.015896, 'H': 0.033, 'G': 49.33},    # Lunisolar synodic fortnightly
    'Q1': {'speed': 13.398661, 'H': 0.023, 'G': 38.08},    # Larger lunar elliptic diurnal
    'P1': {'speed': 14.958931, 'H': 0.060, 'G': 54.76},    # Solar diurnal
}

NM = 1.11  # Nível Médio da Ficha 60266 (Terminal Gás Sul)

# 2. Função para calcular altura de maré em um momento específico
def calculate_tide(dt, constituents, nm):
    """Calcula a altura da maré para um datetime específico"""
    # Referência: 1 de janeiro de 2000, 00:00 UTC
    ref_date = datetime(2000, 1, 1, 0, 0, 0)
    hours = (dt - ref_date).total_seconds() / 3600.0

    height = nm  # Começa com o nível médio

    for name, data in constituents.items():
        speed = data['speed']  # graus por hora
        H = data['H']  # amplitude em metros
        G = data['G']  # fase em graus

        # Calcula a contribuição desta componente
        phase = speed * hours - G
        height += H * np.cos(np.radians(phase))

    return height

# 3. Gerar série temporal e encontrar extremos
print("Processando extremos de maré para Terminal Gás Sul...")
print("(isso pode levar alguns segundos)")

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
            'Altura_m': round(heights[i] + NM, 2),
            'Evento': 'Preamar'
        })
    # Mínimo local (Baixa-mar)
    elif heights[i] < heights[i-1] and heights[i] < heights[i+1]:
        extrema.append({
            'Data_Hora': times[i],
            'Altura_m': round(heights[i] + NM, 2),
            'Evento': 'Baixa-mar'
        })

# 4. Criar DataFrame
df_tgs = pd.DataFrame(extrema)

# Visualização
print("\n=== Primeiras 20 previsões ===")
print(df_tgs.head(20))

print(f"\n=== Resumo ===")
print(f"Total de eventos: {len(df_tgs)}")
print(f"Período: {start.date()} até {end.date()}")
print(f"Preamares: {len(df_tgs[df_tgs['Evento'] == 'Preamar'])}")
print(f"Baixa-mares: {len(df_tgs[df_tgs['Evento'] == 'Baixa-mar'])}")

# Estatísticas de altura
print(f"\n=== Estatísticas de Altura (metros) ===")
print(f"Altura mínima: {df_tgs['Altura_m'].min():.2f} m")
print(f"Altura máxima: {df_tgs['Altura_m'].max():.2f} m")
print(f"Amplitude média: {df_tgs['Altura_m'].max() - df_tgs['Altura_m'].min():.2f} m")
print(f"Altura média: {df_tgs['Altura_m'].mean():.2f} m")

# Salvar arquivo
output_file = 'tgs_extremos_2020_2026.csv'
df_tgs.to_csv(output_file, index=False)
print(f"\n✓ Arquivo salvo: {output_file}")

# Informação adicional
print("\n=== Observações ===")
print("Terminal Gás Sul apresenta micro-maré (amplitude < 2m)")
print("A influência meteorológica pode ser significativa nesta região")
