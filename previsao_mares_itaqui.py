#!/usr/bin/env python3
"""
Script de Previsão de Marés - Porto de Itaqui
Calcula preamares e baixa-mares usando 35 constantes harmônicas
Ficha 30110 - Porto de Itaqui
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. Cadastro das 35 Constantes Harmônicas (Ficha 30110 - Porto de Itaqui)
# Valores exatos de H (Amplitude em metros) e G (Fase em graus)
constituents = {
    'M2': {'speed': 28.984104, 'H': 2.441, 'G': 207.27},   # Principal lunar semidiurnal
    'S2': {'speed': 30.000000, 'H': 0.908, 'G': 241.14},   # Principal solar semidiurnal
    'N2': {'speed': 28.439730, 'H': 0.443, 'G': 189.92},   # Larger lunar elliptic
    'K2': {'speed': 30.082137, 'H': 0.252, 'G': 237.54},   # Lunisolar semidiurnal
    'K1': {'speed': 15.041069, 'H': 0.089, 'G': 203.04},   # Lunisolar diurnal
    'O1': {'speed': 13.943035, 'H': 0.077, 'G': 201.21},   # Lunar diurnal
    'P1': {'speed': 14.958931, 'H': 0.028, 'G': 201.07},   # Solar diurnal
    'Q1': {'speed': 13.398661, 'H': 0.018, 'G': 186.29},   # Larger lunar elliptic diurnal
    'M4': {'speed': 57.968208, 'H': 0.061, 'G': 237.28},   # Shallow water overtide
    'MS4': {'speed': 58.984104, 'H': 0.043, 'G': 274.58},  # Shallow water quarter diurnal
    'M6': {'speed': 86.952312, 'H': 0.019, 'G': 114.50},   # Shallow water overtide
    'MK3': {'speed': 44.025173, 'H': 0.016, 'G': 231.83},  # Shallow water terdiurnal
    'S4': {'speed': 60.000000, 'H': 0.006, 'G': 313.97},   # Shallow water overtide
    'MN4': {'speed': 57.423834, 'H': 0.024, 'G': 219.86},  # Shallow water quarter diurnal
    'NU2': {'speed': 28.512583, 'H': 0.088, 'G': 193.81},  # Larger lunar evectional
    'S1': {'speed': 15.000000, 'H': 0.015, 'G': 128.00},   # Solar diurnal
    'MU2': {'speed': 27.968208, 'H': 0.040, 'G': 159.26},  # Variational
    '2N2': {'speed': 27.895355, 'H': 0.057, 'G': 172.57},  # Lunar elliptical semidiurnal
    'OO1': {'speed': 16.139101, 'H': 0.003, 'G': 216.03},  # Lunar diurnal
    'LAM2': {'speed': 29.455626, 'H': 0.020, 'G': 215.11}, # Smaller lunar evectional
    'S6': {'speed': 90.000000, 'H': 0.003, 'G': 177.56},   # Shallow water overtide
    'M8': {'speed': 115.936416, 'H': 0.005, 'G': 231.75},  # Shallow water eighth diurnal
    'M3': {'speed': 43.476156, 'H': 0.009, 'G': 133.04},   # Lunar terdiurnal
    'MF': {'speed': 1.098033, 'H': 0.042, 'G': 196.89},    # Lunisolar fortnightly
    'MM': {'speed': 0.544375, 'H': 0.027, 'G': 203.40},    # Lunar monthly
    'SSA': {'speed': 0.082137, 'H': 0.033, 'G': 222.03},   # Solar semiannual
    'SA': {'speed': 0.041069, 'H': 0.065, 'G': 222.39},    # Solar annual
    'MSF': {'speed': 1.015896, 'H': 0.024, 'G': 11.23},    # Lunisolar synodic fortnightly
    '2MS6': {'speed': 87.968208, 'H': 0.021, 'G': 153.69}, # Shallow water overtide
    '2SM2': {'speed': 31.015896, 'H': 0.044, 'G': 277.10}, # Shallow water semidiurnal
    'MNS2': {'speed': 27.423834, 'H': 0.015, 'G': 206.58}, # Lunar elliptical semidiurnal
    'RHO1': {'speed': 13.471515, 'H': 0.005, 'G': 179.52}, # Larger lunar evectional diurnal
    'T2': {'speed': 29.958933, 'H': 0.053, 'G': 235.33},   # Larger solar elliptic
    'J1': {'speed': 15.585428, 'H': 0.005, 'G': 210.64},   # Smaller lunar elliptic diurnal
    'L2': {'speed': 29.528479, 'H': 0.054, 'G': 210.36},   # Smaller lunar elliptic semidiurnal
}

NM = 3.43  # Nível Médio da Ficha 30110

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
print("Processando extremos de maré (isso pode levar alguns segundos)...")

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
df_itaqui = pd.DataFrame(extrema)

# Visualização
print("\n=== Primeiras 20 previsões ===")
print(df_itaqui.head(20))

print(f"\n=== Resumo ===")
print(f"Total de eventos: {len(df_itaqui)}")
print(f"Período: {start.date()} até {end.date()}")
print(f"Preamares: {len(df_itaqui[df_itaqui['Evento'] == 'Preamar'])}")
print(f"Baixa-mares: {len(df_itaqui[df_itaqui['Evento'] == 'Baixa-mar'])}")

# Estatísticas
print(f"\n=== Estatísticas de Altura (metros) ===")
print(f"Altura mínima: {df_itaqui['Altura_m'].min():.2f} m")
print(f"Altura máxima: {df_itaqui['Altura_m'].max():.2f} m")
print(f"Amplitude média: {df_itaqui['Altura_m'].max() - df_itaqui['Altura_m'].min():.2f} m")

# Salvar arquivo
output_file = 'itaqui_extremos_2020_2026.csv'
df_itaqui.to_csv(output_file, index=False)
print(f"\n✓ Arquivo salvo: {output_file}")
