#!/usr/bin/env python3
"""
Script de Previsão de Marés - Porto de Paranaguá Cais Oeste I
Calcula preamares e baixa-mares usando constantes harmônicas
Ficha 60151 - Paranaguá Cais Oeste I (PR)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. Cadastro das Constantes Harmônicas (Ficha 60151 - Paranaguá Cais Oeste I)
# Valores de H (Amplitude em metros) e G (Fase em graus)
constituents = {
    'M2': {'speed': 28.984104, 'H': 0.470, 'G': 85.50},    # Principal lunar semidiurnal
    'S2': {'speed': 30.000000, 'H': 0.311, 'G': 98.40},    # Principal solar semidiurnal
    'O1': {'speed': 13.943035, 'H': 0.126, 'G': 50.80},    # Lunar diurnal
    'K1': {'speed': 15.041069, 'H': 0.201, 'G': 58.60},    # Lunisolar diurnal
    'N2': {'speed': 28.439730, 'H': 0.093, 'G': 66.80},    # Larger lunar elliptic
    'K2': {'speed': 30.082137, 'H': 0.086, 'G': 92.40},    # Lunisolar semidiurnal
    'P1': {'speed': 14.958931, 'H': 0.066, 'G': 58.60},    # Solar diurnal
    'Q1': {'speed': 13.398661, 'H': 0.025, 'G': 45.20},    # Larger lunar elliptic diurnal
    'M4': {'speed': 57.968208, 'H': 0.020, 'G': 248.80},   # Shallow water overtide
    'MS4': {'speed': 58.984104, 'H': 0.022, 'G': 276.00},  # Shallow water quarter diurnal
    'M6': {'speed': 86.952312, 'H': 0.012, 'G': 270.20},   # Shallow water overtide
    'MK3': {'speed': 44.025173, 'H': 0.009, 'G': 238.60},  # Shallow water terdiurnal
    'S4': {'speed': 60.000000, 'H': 0.004, 'G': 315.60},   # Shallow water overtide
    'MN4': {'speed': 57.423834, 'H': 0.006, 'G': 229.00},  # Shallow water quarter diurnal
    'NU2': {'speed': 28.512583, 'H': 0.021, 'G': 65.60},   # Larger lunar evectional
    'S1': {'speed': 15.000000, 'H': 0.024, 'G': 18.00},    # Solar diurnal
    'MU2': {'speed': 27.968208, 'H': 0.010, 'G': 33.60},   # Variational
    '2N2': {'speed': 27.895355, 'H': 0.012, 'G': 47.60},   # Lunar elliptical semidiurnal
    'OO1': {'speed': 16.139101, 'H': 0.006, 'G': 68.60},   # Lunar diurnal
    'LAM2': {'speed': 29.455626, 'H': 0.005, 'G': 104.00}, # Smaller lunar evectional
    'S6': {'speed': 90.000000, 'H': 0.004, 'G': 350.40},   # Shallow water overtide
    'M8': {'speed': 115.936416, 'H': 0.002, 'G': 34.40},   # Shallow water eighth diurnal
    'M3': {'speed': 43.476156, 'H': 0.004, 'G': 78.00},    # Lunar terdiurnal
    'MF': {'speed': 1.098033, 'H': 0.035, 'G': 301.60},    # Lunisolar fortnightly
    'MM': {'speed': 0.544375, 'H': 0.020, 'G': 237.00},    # Lunar monthly
    'SSA': {'speed': 0.082137, 'H': 0.063, 'G': 180.40},   # Solar semiannual
    'SA': {'speed': 0.041069, 'H': 0.082, 'G': 186.00},    # Solar annual
    'MSF': {'speed': 1.015896, 'H': 0.026, 'G': 56.00},    # Lunisolar synodic fortnightly
    'RHO1': {'speed': 13.471515, 'H': 0.007, 'G': 44.40},  # Larger lunar evectional diurnal
    'T2': {'speed': 29.958933, 'H': 0.018, 'G': 98.40},    # Larger solar elliptic
    'J1': {'speed': 15.585428, 'H': 0.006, 'G': 68.60},    # Smaller lunar elliptic diurnal
    'L2': {'speed': 29.528479, 'H': 0.020, 'G': 105.00},   # Smaller lunar elliptic semidiurnal
    '2MS6': {'speed': 87.968208, 'H': 0.012, 'G': 203.00}, # Shallow water overtide
    '2SM2': {'speed': 31.015896, 'H': 0.014, 'G': 315.60}, # Shallow water semidiurnal
    'MNS2': {'speed': 27.423834, 'H': 0.007, 'G': 86.60},  # Lunar elliptical semidiurnal
}

NM = 0.916  # Nível Médio da Ficha 60151 (Paranaguá Cais Oeste I)

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
print("Processando extremos de maré para Paranaguá Cais Oeste I...")
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
df_cais_oeste = pd.DataFrame(extrema)

# Visualização
print("\n=== Primeiras 20 previsões ===")
print(df_cais_oeste.head(20))

print(f"\n=== Resumo ===")
print(f"Total de eventos: {len(df_cais_oeste)}")
print(f"Período: {start.date()} até {end.date()}")
print(f"Preamares: {len(df_cais_oeste[df_cais_oeste['Evento'] == 'Preamar'])}")
print(f"Baixa-mares: {len(df_cais_oeste[df_cais_oeste['Evento'] == 'Baixa-mar'])}")

# Estatísticas de altura
print(f"\n=== Estatísticas de Altura (metros) ===")
print(f"Altura mínima: {df_cais_oeste['Altura_m'].min():.2f} m")
print(f"Altura máxima: {df_cais_oeste['Altura_m'].max():.2f} m")
print(f"Amplitude média: {df_cais_oeste['Altura_m'].max() - df_cais_oeste['Altura_m'].min():.2f} m")
print(f"Altura média: {df_cais_oeste['Altura_m'].mean():.2f} m")

# Salvar arquivo
output_file = 'paranagua_cais_oeste_extremos_2020_2026.csv'
df_cais_oeste.to_csv(output_file, index=False)
print(f"\n✓ Arquivo salvo: {output_file}")

# Informação adicional
print("\n=== Observações Importantes - Cais Oeste I ===")
print("Localização: Interior da Baía de Paranaguá (mais para oeste)")
print("Esta estação complementa o Cais Leste (TCP) para análise de gradiente")
print("")
print("⚠️  COMPARAÇÃO COM CAIS LESTE:")
print("   - NM Cais Oeste: 0.916 m vs NM Cais Leste: 0.937 m")
print("   - Diferença de fase permite calcular velocidade de propagação da onda de maré")
print("   - Distorção de águas rasas similar (M4, MS4, M6)")
print("")
print("Para Machine Learning:")
print("   - Feature de gradiente: diferença de altura entre Cais Oeste e Cais Leste")
print("   - Feature de lag temporal: tempo entre preamares nas duas estações")
print("   - Permite prever condições no canal de acesso")
print("   - Útil para navegação e operações portuárias")
