#!/usr/bin/env python3
"""
Script de Previsão de Marés - Ilha da Paz
Calcula preamares e baixa-mares usando constantes harmônicas
Ficha 60208 - Ilha da Paz, São Francisco do Sul (SC)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. Cadastro das Constantes Harmônicas (Ficha 60208 - Ilha da Paz)
# Valores de H (Amplitude em metros) e G (Fase em graus)
constituents = {
    'M2': {'speed': 28.984104, 'H': 0.266, 'G': 69.11},    # Principal lunar semidiurnal
    'S2': {'speed': 30.000000, 'H': 0.222, 'G': 70.31},    # Principal solar semidiurnal
    'O1': {'speed': 13.943035, 'H': 0.106, 'G': 41.21},    # Lunar diurnal
    'K1': {'speed': 15.041069, 'H': 0.162, 'G': 51.51},    # Lunisolar diurnal
    'N2': {'speed': 28.439730, 'H': 0.051, 'G': 48.31},    # Larger lunar elliptic
    'K2': {'speed': 30.082137, 'H': 0.060, 'G': 64.11},    # Lunisolar semidiurnal
    'P1': {'speed': 14.958931, 'H': 0.053, 'G': 51.51},    # Solar diurnal
    'Q1': {'speed': 13.398661, 'H': 0.021, 'G': 35.51},    # Larger lunar elliptic diurnal
    'M4': {'speed': 57.968208, 'H': 0.005, 'G': 172.11},   # Shallow water overtide
    'MS4': {'speed': 58.984104, 'H': 0.005, 'G': 237.11},  # Shallow water quarter diurnal
    'M6': {'speed': 86.952312, 'H': 0.004, 'G': 185.11},   # Shallow water overtide
    'MK3': {'speed': 44.025173, 'H': 0.003, 'G': 164.11},  # Shallow water terdiurnal
    'S4': {'speed': 60.000000, 'H': 0.001, 'G': 335.31},   # Shallow water overtide
    'MN4': {'speed': 57.423834, 'H': 0.002, 'G': 169.11},  # Shallow water quarter diurnal
    'NU2': {'speed': 28.512583, 'H': 0.011, 'G': 51.31},   # Larger lunar evectional
    'S1': {'speed': 15.000000, 'H': 0.016, 'G': 26.00},    # Solar diurnal
    'MU2': {'speed': 27.968208, 'H': 0.006, 'G': 24.31},   # Variational
    '2N2': {'speed': 27.895355, 'H': 0.006, 'G': 36.31},   # Lunar elliptical semidiurnal
    'OO1': {'speed': 16.139101, 'H': 0.005, 'G': 64.11},   # Lunar diurnal
    'LAM2': {'speed': 29.455626, 'H': 0.002, 'G': 91.31},  # Smaller lunar evectional
    'S6': {'speed': 90.000000, 'H': 0.002, 'G': 306.31},   # Shallow water overtide
    'M8': {'speed': 115.936416, 'H': 0.002, 'G': 273.11},  # Shallow water eighth diurnal
    'M3': {'speed': 43.476156, 'H': 0.002, 'G': 335.31},   # Lunar terdiurnal
    'MF': {'speed': 1.098033, 'H': 0.038, 'G': 301.31},    # Lunisolar fortnightly
    'MM': {'speed': 0.544375, 'H': 0.024, 'G': 226.31},    # Lunar monthly
    'SSA': {'speed': 0.082137, 'H': 0.063, 'G': 172.11},   # Solar semiannual
    'SA': {'speed': 0.041069, 'H': 0.084, 'G': 184.11},    # Solar annual
    'MSF': {'speed': 1.015896, 'H': 0.033, 'G': 49.31},    # Lunisolar synodic fortnightly
    'RHO1': {'speed': 13.471515, 'H': 0.006, 'G': 38.31},  # Larger lunar evectional diurnal
    'T2': {'speed': 29.958933, 'H': 0.013, 'G': 70.31},    # Larger solar elliptic
    'J1': {'speed': 15.585428, 'H': 0.008, 'G': 64.11},    # Smaller lunar elliptic diurnal
    'L2': {'speed': 29.528479, 'H': 0.008, 'G': 103.31},   # Smaller lunar elliptic semidiurnal
    '2MS6': {'speed': 87.968208, 'H': 0.004, 'G': 153.31}, # Shallow water overtide
    '2SM2': {'speed': 31.015896, 'H': 0.006, 'G': 277.31}, # Shallow water semidiurnal
    'MNS2': {'speed': 27.423834, 'H': 0.003, 'G': 58.31},  # Lunar elliptical semidiurnal
}

NM = 0.781  # Nível Médio da Ficha 60208 (Ilha da Paz)

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
print("Processando extremos de maré para Ilha da Paz...")
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
df_ilhadapaz = pd.DataFrame(extrema)

# Visualização
print("\n=== Primeiras 20 previsões ===")
print(df_ilhadapaz.head(20))

print(f"\n=== Resumo ===")
print(f"Total de eventos: {len(df_ilhadapaz)}")
print(f"Período: {start.date()} até {end.date()}")
print(f"Preamares: {len(df_ilhadapaz[df_ilhadapaz['Evento'] == 'Preamar'])}")
print(f"Baixa-mares: {len(df_ilhadapaz[df_ilhadapaz['Evento'] == 'Baixa-mar'])}")

# Estatísticas de altura
print(f"\n=== Estatísticas de Altura (metros) ===")
print(f"Altura mínima: {df_ilhadapaz['Altura_m'].min():.2f} m")
print(f"Altura máxima: {df_ilhadapaz['Altura_m'].max():.2f} m")
print(f"Amplitude média: {df_ilhadapaz['Altura_m'].max() - df_ilhadapaz['Altura_m'].min():.2f} m")
print(f"Altura média: {df_ilhadapaz['Altura_m'].mean():.2f} m")

# Salvar arquivo
output_file = 'ilhadapaz_extremos_2020_2026.csv'
df_ilhadapaz.to_csv(output_file, index=False)
print(f"\n✓ Arquivo salvo: {output_file}")

# Informação adicional
print("\n=== Observações ===")
print("Ilha da Paz (São Francisco do Sul) apresenta micro-maré")
print("Localização: Baía da Babitonga, Santa Catarina")
print("Classificação: Micro-maré oceânica")
