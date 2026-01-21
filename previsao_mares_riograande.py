#!/usr/bin/env python3
"""
Script de Previsão de Marés - Porto do Rio Grande
Calcula preamares e baixa-mares usando constantes harmônicas
Carta 2101 - Ficha 60380 (F-41) - PRATICAGEM R.GRANDE
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. Cadastro das Constantes Harmônicas (Ficha 60380 - Porto do Rio Grande)
# Valores de H (Amplitude em metros) e G (Fase em graus)
constituents = {
    'M2': {'speed': 28.984104, 'H': 0.103, 'G': 58.76},    # Principal lunar semidiurnal
    'S2': {'speed': 30.000000, 'H': 0.076, 'G': 52.89},    # Principal solar semidiurnal
    'O1': {'speed': 13.943035, 'H': 0.052, 'G': 28.52},    # Lunar diurnal
    'K1': {'speed': 15.041069, 'H': 0.071, 'G': 38.38},    # Lunisolar diurnal
    'N2': {'speed': 28.439730, 'H': 0.021, 'G': 37.10},    # Larger lunar elliptic
    'K2': {'speed': 30.082137, 'H': 0.021, 'G': 52.48},    # Lunisolar semidiurnal
    'P1': {'speed': 14.958931, 'H': 0.023, 'G': 38.38},    # Solar diurnal
    'Q1': {'speed': 13.398661, 'H': 0.010, 'G': 20.37},    # Larger lunar elliptic diurnal
    'M4': {'speed': 57.968208, 'H': 0.003, 'G': 192.34},   # Shallow water overtide
    'MS4': {'speed': 58.984104, 'H': 0.002, 'G': 117.89},  # Shallow water quarter diurnal
    'M6': {'speed': 86.952312, 'H': 0.002, 'G': 290.34},   # Shallow water overtide
    'MK3': {'speed': 44.025173, 'H': 0.003, 'G': 115.39},  # Shallow water terdiurnal
    'S4': {'speed': 60.000000, 'H': 0.001, 'G': 230.13},   # Shallow water overtide
    'MN4': {'speed': 57.423834, 'H': 0.001, 'G': 169.51},  # Shallow water quarter diurnal
    'NU2': {'speed': 28.512583, 'H': 0.004, 'G': 38.41},   # Larger lunar evectional
    'S1': {'speed': 15.000000, 'H': 0.021, 'G': 313.23},   # Solar diurnal
    'MU2': {'speed': 27.968208, 'H': 0.002, 'G': 20.84},   # Variational
    '2N2': {'speed': 27.895355, 'H': 0.003, 'G': 15.44},   # Lunar elliptical semidiurnal
    'OO1': {'speed': 16.139101, 'H': 0.002, 'G': 48.24},   # Lunar diurnal
    'LAM2': {'speed': 29.455626, 'H': 0.001, 'G': 64.91},  # Smaller lunar evectional
    'S6': {'speed': 90.000000, 'H': 0.001, 'G': 164.21},   # Shallow water overtide
    'M8': {'speed': 115.936416, 'H': 0.001, 'G': 32.55},   # Shallow water eighth diurnal
    'M3': {'speed': 43.476156, 'H': 0.001, 'G': 22.86},    # Lunar terdiurnal
    'MF': {'speed': 1.098033, 'H': 0.038, 'G': 277.10},    # Lunisolar fortnightly
    'MM': {'speed': 0.544375, 'H': 0.023, 'G': 198.66},    # Lunar monthly
    'SSA': {'speed': 0.082137, 'H': 0.046, 'G': 179.91},   # Solar semiannual
    'SA': {'speed': 0.041069, 'H': 0.061, 'G': 185.76},    # Solar annual
    'MSF': {'speed': 1.015896, 'H': 0.036, 'G': 11.83},    # Lunisolar synodic fortnightly
    'RHO1': {'speed': 13.471515, 'H': 0.002, 'G': 19.34},  # Larger lunar evectional diurnal
    'T2': {'speed': 29.958933, 'H': 0.004, 'G': 52.89},    # Larger solar elliptic
    'J1': {'speed': 15.585428, 'H': 0.004, 'G': 48.24},    # Smaller lunar elliptic diurnal
    'L2': {'speed': 29.528479, 'H': 0.003, 'G': 76.57},    # Smaller lunar elliptic semidiurnal
    '2MS6': {'speed': 87.968208, 'H': 0.001, 'G': 224.23}, # Shallow water overtide
    '2SM2': {'speed': 31.015896, 'H': 0.003, 'G': 222.10}, # Shallow water semidiurnal
    'MNS2': {'speed': 27.423834, 'H': 0.001, 'G': 58.07},  # Lunar elliptical semidiurnal
}

NM = 0.858  # Nível Médio da Ficha 60380 (S0 = 85.8 cm)

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
print("Processando extremos de maré para Porto do Rio Grande...")
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
df_riograande = pd.DataFrame(extrema)

# Visualização
print("\n=== Primeiras 20 previsões ===")
print(df_riograande.head(20))

print(f"\n=== Resumo ===")
print(f"Total de eventos: {len(df_riograande)}")
print(f"Período: {start.date()} até {end.date()}")
print(f"Preamares: {len(df_riograande[df_riograande['Evento'] == 'Preamar'])}")
print(f"Baixa-mares: {len(df_riograande[df_riograande['Evento'] == 'Baixa-mar'])}")

# Estatísticas de altura
print(f"\n=== Estatísticas de Altura (metros) ===")
print(f"Altura mínima: {df_riograande['Altura_m'].min():.2f} m")
print(f"Altura máxima: {df_riograande['Altura_m'].max():.2f} m")
print(f"Amplitude média: {df_riograande['Altura_m'].max() - df_riograande['Altura_m'].min():.2f} m")
print(f"Altura média: {df_riograande['Altura_m'].mean():.2f} m")

# Salvar arquivo
output_file = 'riograande_extremos_2020_2026.csv'
df_riograande.to_csv(output_file, index=False)
print(f"\n✓ Arquivo salvo: {output_file}")

# Informação adicional
print("\n=== Observações ===")
print("Porto do Rio Grande apresenta maré mista com micro-amplitude")
print("Classificação: Maré Mista")
print("Estabelecimento de Porto: 7h 28m")
