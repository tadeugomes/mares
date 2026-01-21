#!/usr/bin/env python3
"""
Script de Previsão de Marés - Vila do Conde
Calcula preamares e baixa-mares usando constantes harmônicas
Ficha 10566 - Vila do Conde, Barcarena (PA)
Localização: Baía de Marajó - Foz do Rio Amazonas
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. Cadastro das Constantes Harmônicas (Ficha 10566 - Vila do Conde)
# Valores de H (Amplitude em metros) e G (Fase em graus)
constituents = {
    'M2': {'speed': 28.984104, 'H': 1.144, 'G': 185.73},   # Principal lunar semidiurnal
    'S2': {'speed': 30.000000, 'H': 0.354, 'G': 224.23},   # Principal solar semidiurnal
    'N2': {'speed': 28.439730, 'H': 0.211, 'G': 159.23},   # Larger lunar elliptic
    'K2': {'speed': 30.082137, 'H': 0.098, 'G': 220.13},   # Lunisolar semidiurnal
    'K1': {'speed': 15.041069, 'H': 0.052, 'G': 196.43},   # Lunisolar diurnal
    'O1': {'speed': 13.943035, 'H': 0.047, 'G': 183.13},   # Lunar diurnal
    'P1': {'speed': 14.958931, 'H': 0.017, 'G': 196.43},   # Solar diurnal
    'Q1': {'speed': 13.398661, 'H': 0.012, 'G': 169.83},   # Larger lunar elliptic diurnal
    'M4': {'speed': 57.968208, 'H': 0.054, 'G': 184.81},   # Shallow water overtide (SIGNIFICATIVA!)
    'MS4': {'speed': 58.984104, 'H': 0.033, 'G': 228.31},  # Shallow water quarter diurnal
    'M6': {'speed': 86.952312, 'H': 0.021, 'G': 240.23},   # Shallow water overtide (PRONUNCIADA!)
    'MK3': {'speed': 44.025173, 'H': 0.016, 'G': 172.13},  # Shallow water terdiurnal
    'S4': {'speed': 60.000000, 'H': 0.005, 'G': 301.21},   # Shallow water overtide
    'MN4': {'speed': 57.423834, 'H': 0.020, 'G': 158.33},  # Shallow water quarter diurnal
    'NU2': {'speed': 28.512583, 'H': 0.042, 'G': 163.13},  # Larger lunar evectional
    'S1': {'speed': 15.000000, 'H': 0.021, 'G': 112.00},   # Solar diurnal
    'MU2': {'speed': 27.968208, 'H': 0.019, 'G': 128.43},  # Variational
    '2N2': {'speed': 27.895355, 'H': 0.027, 'G': 132.73},  # Lunar elliptical semidiurnal
    'OO1': {'speed': 16.139101, 'H': 0.002, 'G': 209.73},  # Lunar diurnal
    'LAM2': {'speed': 29.455626, 'H': 0.010, 'G': 193.23}, # Smaller lunar evectional
    'S6': {'speed': 90.000000, 'H': 0.003, 'G': 335.81},   # Shallow water overtide
    'M8': {'speed': 115.936416, 'H': 0.005, 'G': 185.13},  # Shallow water eighth diurnal
    'M3': {'speed': 43.476156, 'H': 0.005, 'G': 120.33},   # Lunar terdiurnal
    'MF': {'speed': 1.098033, 'H': 0.036, 'G': 172.13},    # Lunisolar fortnightly
    'MM': {'speed': 0.544375, 'H': 0.021, 'G': 185.31},    # Lunar monthly
    'SSA': {'speed': 0.082137, 'H': 0.042, 'G': 172.13},   # Solar semiannual
    'SA': {'speed': 0.041069, 'H': 0.058, 'G': 184.13},    # Solar annual
    'MSF': {'speed': 1.015896, 'H': 0.023, 'G': 11.23},    # Lunisolar synodic fortnightly
    'RHO1': {'speed': 13.471515, 'H': 0.004, 'G': 158.43}, # Larger lunar evectional diurnal
    'T2': {'speed': 29.958933, 'H': 0.021, 'G': 224.23},   # Larger solar elliptic
    'J1': {'speed': 15.585428, 'H': 0.003, 'G': 209.73},   # Smaller lunar elliptic diurnal
    'L2': {'speed': 29.528479, 'H': 0.026, 'G': 212.23},   # Smaller lunar elliptic semidiurnal
    '2MS6': {'speed': 87.968208, 'H': 0.023, 'G': 198.81}, # Shallow water overtide
    '2SM2': {'speed': 31.015896, 'H': 0.018, 'G': 301.11}, # Shallow water semidiurnal
    'MNS2': {'speed': 27.423834, 'H': 0.012, 'G': 185.73}, # Lunar elliptical semidiurnal
}

NM = 2.15  # Nível Médio da Ficha 10566 (Vila do Conde)

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
print("Processando extremos de maré para Vila do Conde...")
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
df_viladoconde = pd.DataFrame(extrema)

# Visualização
print("\n=== Primeiras 20 previsões ===")
print(df_viladoconde.head(20))

print(f"\n=== Resumo ===")
print(f"Total de eventos: {len(df_viladoconde)}")
print(f"Período: {start.date()} até {end.date()}")
print(f"Preamares: {len(df_viladoconde[df_viladoconde['Evento'] == 'Preamar'])}")
print(f"Baixa-mares: {len(df_viladoconde[df_viladoconde['Evento'] == 'Baixa-mar'])}")

# Estatísticas de altura
print(f"\n=== Estatísticas de Altura (metros) ===")
print(f"Altura mínima: {df_viladoconde['Altura_m'].min():.2f} m")
print(f"Altura máxima: {df_viladoconde['Altura_m'].max():.2f} m")
print(f"Amplitude média: {df_viladoconde['Altura_m'].max() - df_viladoconde['Altura_m'].min():.2f} m")
print(f"Altura média: {df_viladoconde['Altura_m'].mean():.2f} m")

# Salvar arquivo
output_file = 'viladoconde_extremos_2020_2026.csv'
df_viladoconde.to_csv(output_file, index=False)
print(f"\n✓ Arquivo salvo: {output_file}")

# Informações importantes
print("\n=== Observações Importantes - Vila do Conde ===")
print("Localização: Baía de Marajó - Foz do Rio Amazonas")
print("Segunda maior amplitude de maré do projeto (~3m)")
print("")
print("⚠️  FORTE DISTORÇÃO DE ÁGUAS RASAS:")
print("   - Componentes M4, M6 muito significativas")
print("   - Assimetria: maré sobe mais rápido do que desce")
print("   - Influência do gigantesco volume de água doce do Amazonas/Tocantins")
print("")
print("Para Machine Learning:")
print("   - Feature principal: Previsão astronômica (este script)")
print("   - Feature fluvial: Vazão dos rios Amazonas e Tocantins")
print("   - Desvios sazonais significativos devido à descarga fluvial")
print("   - Distorção de assimetria capturada por M4 e M6")
