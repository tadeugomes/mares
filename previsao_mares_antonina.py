#!/usr/bin/env python3
"""
Script de Previsão de Marés - Porto de Antonina
Calcula preamares e baixa-mares usando constantes harmônicas
Ficha 60110 - Antonina (PR)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. Cadastro das Constantes Harmônicas (Ficha 60110 - Antonina)
# Valores de H (Amplitude em metros) e G (Fase em graus)
constituents = {
    'M2': {'speed': 28.984104, 'H': 0.536, 'G': 100.2},    # Principal lunar semidiurnal
    'S2': {'speed': 30.000000, 'H': 0.354, 'G': 114.3},    # Principal solar semidiurnal
    'O1': {'speed': 13.943035, 'H': 0.126, 'G': 55.4},     # Lunar diurnal
    'K1': {'speed': 15.041069, 'H': 0.201, 'G': 63.8},     # Lunisolar diurnal
    'N2': {'speed': 28.439730, 'H': 0.106, 'G': 82.1},     # Larger lunar elliptic
    'K2': {'speed': 30.082137, 'H': 0.096, 'G': 114.3},    # Lunisolar semidiurnal
    'P1': {'speed': 14.958931, 'H': 0.066, 'G': 63.8},     # Solar diurnal
    'Q1': {'speed': 13.398661, 'H': 0.025, 'G': 48.1},     # Larger lunar elliptic diurnal
    'M4': {'speed': 57.968208, 'H': 0.027, 'G': 273.4},    # Shallow water overtide
    'MS4': {'speed': 58.984104, 'H': 0.030, 'G': 310.2},   # Shallow water quarter diurnal
    'M6': {'speed': 86.952312, 'H': 0.016, 'G': 298.5},    # Shallow water overtide
    'MK3': {'speed': 44.025173, 'H': 0.012, 'G': 264.3},   # Shallow water terdiurnal
    'S4': {'speed': 60.000000, 'H': 0.005, 'G': 345.2},    # Shallow water overtide
    'MN4': {'speed': 57.423834, 'H': 0.008, 'G': 255.4},   # Shallow water quarter diurnal
    'NU2': {'speed': 28.512583, 'H': 0.021, 'G': 80.2},    # Larger lunar evectional
    'S1': {'speed': 15.000000, 'H': 0.024, 'G': 18.0},     # Solar diurnal
    'MU2': {'speed': 27.968208, 'H': 0.010, 'G': 42.4},    # Variational
    '2N2': {'speed': 27.895355, 'H': 0.015, 'G': 64.2},    # Lunar elliptical semidiurnal
    'OO1': {'speed': 16.139101, 'H': 0.006, 'G': 75.4},    # Lunar diurnal
    'LAM2': {'speed': 29.455626, 'H': 0.006, 'G': 115.3},  # Smaller lunar evectional
    'S6': {'speed': 90.000000, 'H': 0.004, 'G': 12.1},     # Shallow water overtide
    'M8': {'speed': 115.936416, 'H': 0.003, 'G': 45.2},    # Shallow water eighth diurnal
    'M3': {'speed': 43.476156, 'H': 0.005, 'G': 92.4},     # Lunar terdiurnal
    'MF': {'speed': 1.098033, 'H': 0.035, 'G': 301.1},     # Lunisolar fortnightly
    'MM': {'speed': 0.544375, 'H': 0.020, 'G': 235.8},     # Lunar monthly
    'SSA': {'speed': 0.082137, 'H': 0.063, 'G': 178.5},    # Solar semiannual
    'SA': {'speed': 0.041069, 'H': 0.082, 'G': 184.8},     # Solar annual
    'MSF': {'speed': 1.015896, 'H': 0.026, 'G': 54.3},     # Lunisolar synodic fortnightly
    'RHO1': {'speed': 13.471515, 'H': 0.007, 'G': 48.2},   # Larger lunar evectional diurnal
    'T2': {'speed': 29.958933, 'H': 0.018, 'G': 114.3},    # Larger solar elliptic
    'J1': {'speed': 15.585428, 'H': 0.006, 'G': 75.4},     # Smaller lunar elliptic diurnal
    'L2': {'speed': 29.528479, 'H': 0.022, 'G': 118.4},    # Smaller lunar elliptic semidiurnal
    '2MS6': {'speed': 87.968208, 'H': 0.015, 'G': 224.2},  # Shallow water overtide
    '2SM2': {'speed': 31.015896, 'H': 0.016, 'G': 335.4},  # Shallow water semidiurnal
    'MNS2': {'speed': 27.423834, 'H': 0.008, 'G': 100.2},  # Lunar elliptical semidiurnal
}

NM = 1.11  # Nível Médio da Ficha 60110 (Antonina)

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
print("Processando extremos de maré para Antonina...")
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
df_antonina = pd.DataFrame(extrema)

# Visualização
print("\n=== Primeiras 20 previsões ===")
print(df_antonina.head(20))

print(f"\n=== Resumo ===")
print(f"Total de eventos: {len(df_antonina)}")
print(f"Período: {start.date()} até {end.date()}")
print(f"Preamares: {len(df_antonina[df_antonina['Evento'] == 'Preamar'])}")
print(f"Baixa-mares: {len(df_antonina[df_antonina['Evento'] == 'Baixa-mar'])}")

# Estatísticas de altura
print(f"\n=== Estatísticas de Altura (metros) ===")
print(f"Altura mínima: {df_antonina['Altura_m'].min():.2f} m")
print(f"Altura máxima: {df_antonina['Altura_m'].max():.2f} m")
print(f"Amplitude média: {df_antonina['Altura_m'].max() - df_antonina['Altura_m'].min():.2f} m")
print(f"Altura média: {df_antonina['Altura_m'].mean():.2f} m")

# Salvar arquivo
output_file = 'antonina_extremos_2020_2026.csv'
df_antonina.to_csv(output_file, index=False)
print(f"\n✓ Arquivo salvo: {output_file}")

# Informação adicional
print("\n=== Observações Importantes - Antonina ===")
print("Localização: Fundo da Baía de Paranaguá")
print("Esta estação é a mais interior das três estações de Paranaguá")
print("")
print("⚠️  EFEITO FUNIL - AMPLIFICAÇÃO DA MARÉ:")
print("   - M2 Antonina: 0.536 m (MAIOR que Cais Leste: 0.470 m)")
print("   - A baía estreita à medida que avança para o interior")
print("   - Isso 'comprime' a água, aumentando a amplitude")
print("")
print("⚠️  ATRASO DA ONDA DE MARÉ (PHASE LAG):")
print("   - Fase M2 Antonina: 100.2° vs Cais Leste: 85.5°")
print("   - Diferença de ~14.7° representa o tempo de propagação")
print("   - A maré 'demora' para chegar ao fundo da baía")
print("")
print("Para Machine Learning:")
print("   - Feature de amplificação: razão entre amplitudes Antonina/Cais Leste")
print("   - Feature de lag temporal: diferença de fase convertida em tempo")
print("   - Permite prever quanto tempo após a preamar em Paranaguá ocorrerá em Antonina")
print("   - Útil para modelar inundações e operações portuárias no fundo da baía")
print("")
print("Conjunto completo da Baía de Paranaguá:")
print("   1. Cais Leste (TCP) - Entrada da baía")
print("   2. Cais Oeste I - Meio da baía")
print("   3. Antonina - Fundo da baía")
