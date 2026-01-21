#!/usr/bin/env python3
"""
Script de Previsão de Marés - Porto de Santos
Calcula preamares e baixa-mares usando constantes harmônicas
Carta 1712 - Ficha 50231 (TIPLAM / Porto de Santos)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. Cadastro das Constantes Harmônicas (Ficha 50231 - TIPLAM / Porto de Santos)
# Valores de H (Amplitude em metros) e G (Fase em graus)
constituents = {
    'M2': {'speed': 28.984104, 'H': 0.354, 'G': 74.52},    # Principal lunar semidiurnal
    'S2': {'speed': 30.000000, 'H': 0.231, 'G': 80.34},    # Principal solar semidiurnal
    'O1': {'speed': 13.943035, 'H': 0.089, 'G': 43.51},    # Lunar diurnal
    'K1': {'speed': 15.041069, 'H': 0.126, 'G': 49.33},    # Lunisolar diurnal
    'N2': {'speed': 28.439730, 'H': 0.076, 'G': 54.12},    # Larger lunar elliptic
    'K2': {'speed': 30.082137, 'H': 0.063, 'G': 75.33},    # Lunisolar semidiurnal
    'M4': {'speed': 57.968208, 'H': 0.015, 'G': 239.51},   # Shallow water overtide
    'MS4': {'speed': 58.984104, 'H': 0.014, 'G': 255.48},  # Shallow water quarter diurnal
    'M6': {'speed': 86.952312, 'H': 0.007, 'G': 248.86},   # Shallow water overtide
    'MK3': {'speed': 44.025173, 'H': 0.006, 'G': 219.82},  # Shallow water terdiurnal
    'S4': {'speed': 60.000000, 'H': 0.003, 'G': 335.78},   # Shallow water overtide
    'MN4': {'speed': 57.423834, 'H': 0.004, 'G': 219.06},  # Shallow water quarter diurnal
    'NU2': {'speed': 28.512583, 'H': 0.016, 'G': 54.55},   # Larger lunar evectional
    'S1': {'speed': 15.000000, 'H': 0.015, 'G': 344.02},   # Solar diurnal
    'MU2': {'speed': 27.968208, 'H': 0.007, 'G': 24.38},   # Variational
    '2N2': {'speed': 27.895355, 'H': 0.010, 'G': 36.63},   # Lunar elliptical semidiurnal
    'OO1': {'speed': 16.139101, 'H': 0.004, 'G': 55.15},   # Lunar diurnal
    'LAM2': {'speed': 29.455626, 'H': 0.004, 'G': 91.07},  # Smaller lunar evectional
    'S6': {'speed': 90.000000, 'H': 0.003, 'G': 303.48},   # Shallow water overtide
    'M8': {'speed': 115.936416, 'H': 0.002, 'G': 348.89},  # Shallow water eighth diurnal
    'M3': {'speed': 43.476156, 'H': 0.003, 'G': 51.57},    # Lunar terdiurnal
    'MF': {'speed': 1.098033, 'H': 0.023, 'G': 292.05},    # Lunisolar fortnightly
    'MM': {'speed': 0.544375, 'H': 0.013, 'G': 230.12},    # Lunar monthly
    'SSA': {'speed': 0.082137, 'H': 0.057, 'G': 180.25},   # Solar semiannual
    'SA': {'speed': 0.041069, 'H': 0.076, 'G': 188.16},    # Solar annual
    'MSF': {'speed': 1.015896, 'H': 0.017, 'G': 43.07},    # Lunisolar synodic fortnightly
    'Q1': {'speed': 13.398661, 'H': 0.017, 'G': 36.83},    # Larger lunar elliptic diurnal
    'P1': {'speed': 14.958931, 'H': 0.042, 'G': 49.33},    # Solar diurnal
}

NM = 0.736  # Nível Médio do Porto de Santos (TIPLAM)

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
print("Processando extremos de maré para Porto de Santos...")
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
df_santos = pd.DataFrame(extrema)

# Visualização
print("\n=== Primeiras 20 previsões ===")
print(df_santos.head(20))

print(f"\n=== Resumo ===")
print(f"Total de eventos: {len(df_santos)}")
print(f"Período: {start.date()} até {end.date()}")
print(f"Preamares: {len(df_santos[df_santos['Evento'] == 'Preamar'])}")
print(f"Baixa-mares: {len(df_santos[df_santos['Evento'] == 'Baixa-mar'])}")

# Estatísticas de altura
print(f"\n=== Estatísticas de Altura (metros) ===")
print(f"Altura mínima: {df_santos['Altura_m'].min():.2f} m")
print(f"Altura máxima: {df_santos['Altura_m'].max():.2f} m")
print(f"Amplitude média: {df_santos['Altura_m'].max() - df_santos['Altura_m'].min():.2f} m")
print(f"Altura média: {df_santos['Altura_m'].mean():.2f} m")

# Salvar arquivo
output_file = 'santos_extremos_2020_2026.csv'
df_santos.to_csv(output_file, index=False)
print(f"\n✓ Arquivo salvo: {output_file}")

# Informação adicional
print("\n=== AVISO IMPORTANTE ===")
print("Estas previsões são baseadas APENAS em componentes astronômicas.")
print("No Porto de Santos, efeitos meteorológicos (ressacas, frentes frias)")
print("podem elevar o nível do mar em mais de 1 metro acima do previsto.")
print("Para operações críticas, consulte também previsões meteorológicas.")
