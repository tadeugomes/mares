#!/usr/bin/env python3
"""
Script de Previsão de Marés - Porto de Paranaguá
Calcula preamares e baixa-mares usando constantes harmônicas
Ficha 60141 - Porto de Paranaguá (PR)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. Cadastro das Constantes Harmônicas (Ficha 60141 - Porto de Paranaguá)
# Valores de H (Amplitude em metros) e G (Fase em graus)
constituents = {
    'M2': {'speed': 28.984104, 'H': 0.468, 'G': 84.11},    # Principal lunar semidiurnal
    'S2': {'speed': 30.000000, 'H': 0.316, 'G': 97.56},    # Principal solar semidiurnal
    'O1': {'speed': 13.943035, 'H': 0.126, 'G': 50.81},    # Lunar diurnal
    'K1': {'speed': 15.041069, 'H': 0.198, 'G': 59.96},    # Lunisolar diurnal
    'N2': {'speed': 28.439730, 'H': 0.093, 'G': 64.91},    # Larger lunar elliptic
    'K2': {'speed': 30.082137, 'H': 0.086, 'G': 91.56},    # Lunisolar semidiurnal
    'P1': {'speed': 14.958931, 'H': 0.065, 'G': 59.96},    # Solar diurnal
    'Q1': {'speed': 13.398661, 'H': 0.025, 'G': 45.31},    # Larger lunar elliptic diurnal
    'M4': {'speed': 57.968208, 'H': 0.021, 'G': 246.33},   # Shallow water overtide
    'MS4': {'speed': 58.984104, 'H': 0.023, 'G': 273.81},  # Shallow water quarter diurnal
    'M6': {'speed': 86.952312, 'H': 0.013, 'G': 266.36},   # Shallow water overtide
    'MK3': {'speed': 44.025173, 'H': 0.009, 'G': 237.98},  # Shallow water terdiurnal
    'S4': {'speed': 60.000000, 'H': 0.004, 'G': 313.38},   # Shallow water overtide
    'MN4': {'speed': 57.423834, 'H': 0.006, 'G': 227.11},  # Shallow water quarter diurnal
    'NU2': {'speed': 28.512583, 'H': 0.021, 'G': 63.81},   # Larger lunar evectional
    'S1': {'speed': 15.000000, 'H': 0.024, 'G': 18.00},    # Solar diurnal
    'MU2': {'speed': 27.968208, 'H': 0.010, 'G': 31.83},   # Variational
    '2N2': {'speed': 27.895355, 'H': 0.012, 'G': 45.81},   # Lunar elliptical semidiurnal
    'OO1': {'speed': 16.139101, 'H': 0.006, 'G': 69.11},   # Lunar diurnal
    'LAM2': {'speed': 29.455626, 'H': 0.005, 'G': 102.31}, # Smaller lunar evectional
    'S6': {'speed': 90.000000, 'H': 0.004, 'G': 345.51},   # Shallow water overtide
    'M8': {'speed': 115.936416, 'H': 0.002, 'G': 30.56},   # Shallow water eighth diurnal
    'M3': {'speed': 43.476156, 'H': 0.004, 'G': 76.81},    # Lunar terdiurnal
    'MF': {'speed': 1.098033, 'H': 0.035, 'G': 301.11},    # Lunisolar fortnightly
    'MM': {'speed': 0.544375, 'H': 0.020, 'G': 235.81},    # Lunar monthly
    'SSA': {'speed': 0.082137, 'H': 0.063, 'G': 178.51},   # Solar semiannual
    'SA': {'speed': 0.041069, 'H': 0.082, 'G': 184.81},    # Solar annual
    'MSF': {'speed': 1.015896, 'H': 0.026, 'G': 54.31},    # Lunisolar synodic fortnightly
    'RHO1': {'speed': 13.471515, 'H': 0.007, 'G': 44.56},  # Larger lunar evectional diurnal
    'T2': {'speed': 29.958933, 'H': 0.018, 'G': 97.56},    # Larger solar elliptic
    'J1': {'speed': 15.585428, 'H': 0.006, 'G': 69.11},    # Smaller lunar elliptic diurnal
    'L2': {'speed': 29.528479, 'H': 0.020, 'G': 103.31},   # Smaller lunar elliptic semidiurnal
    '2MS6': {'speed': 87.968208, 'H': 0.012, 'G': 198.81}, # Shallow water overtide
    '2SM2': {'speed': 31.015896, 'H': 0.014, 'G': 313.11}, # Shallow water semidiurnal
    'MNS2': {'speed': 27.423834, 'H': 0.007, 'G': 85.31},  # Lunar elliptical semidiurnal
}

NM = 0.937  # Nível Médio da Ficha 60141 (Porto de Paranaguá)

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
print("Processando extremos de maré para Porto de Paranaguá...")
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
df_paranagua = pd.DataFrame(extrema)

# Visualização
print("\n=== Primeiras 20 previsões ===")
print(df_paranagua.head(20))

print(f"\n=== Resumo ===")
print(f"Total de eventos: {len(df_paranagua)}")
print(f"Período: {start.date()} até {end.date()}")
print(f"Preamares: {len(df_paranagua[df_paranagua['Evento'] == 'Preamar'])}")
print(f"Baixa-mares: {len(df_paranagua[df_paranagua['Evento'] == 'Baixa-mar'])}")

# Estatísticas de altura
print(f"\n=== Estatísticas de Altura (metros) ===")
print(f"Altura mínima: {df_paranagua['Altura_m'].min():.2f} m")
print(f"Altura máxima: {df_paranagua['Altura_m'].max():.2f} m")
print(f"Amplitude média: {df_paranagua['Altura_m'].max() - df_paranagua['Altura_m'].min():.2f} m")
print(f"Altura média: {df_paranagua['Altura_m'].mean():.2f} m")

# Salvar arquivo
output_file = 'paranagua_extremos_2020_2026.csv'
df_paranagua.to_csv(output_file, index=False)
print(f"\n✓ Arquivo salvo: {output_file}")

# Informação adicional
print("\n=== Observações Importantes ===")
print("Porto de Paranaguá apresenta distorção de maré (águas rasas)")
print("Constantes significativas: M4, MS4, M6 indicam deformação da onda de maré")
print("⚠️  Influência meteorológica: ventos sul causam sobre-elevação na Baía")
print("Para ML: maré astronômica é feature principal, vento é feature de erro")
