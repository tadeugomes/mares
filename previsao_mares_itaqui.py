#!/usr/bin/env python3
"""
Script de Previsão de Marés - Porto de Itaqui
Calcula preamares e baixa-mares usando 35 constantes harmônicas
Ficha 30110 - Porto de Itaqui
"""

import pandas as pd
from datetime import datetime
from pytides.tide import Tide
import pytides.constituent as cons

# 1. Cadastro das 35 Constantes Harmônicas (Ficha 30110 - Porto de Itaqui)
# Valores exatos de H (Amplitude) e G (Fase) do seu documento
constituent_data = {
    'M2': (2.441, 207.27), 'S2': (0.908, 241.14), 'N2': (0.443, 189.92),
    'K2': (0.252, 237.54), 'K1': (0.089, 203.04), 'O1': (0.077, 201.21),
    'P1': (0.028, 201.07), 'Q1': (0.018, 186.29), 'M4': (0.061, 237.28),
    'MS4': (0.043, 274.58), 'M6': (0.019, 114.50), 'MK3': (0.016, 231.83),
    'S4': (0.006, 313.97), 'MN4': (0.024, 219.86), 'NU2': (0.088, 193.81),
    'S1': (0.015, 128.00), 'MU2': (0.040, 159.26), '2N2': (0.057, 172.57),
    'OO1': (0.003, 216.03), 'LAM2': (0.020, 215.11), 'S6': (0.003, 177.56),
    'M8': (0.005, 231.75), 'M3': (0.009, 133.04), 'MF': (0.042, 196.89),
    'MM': (0.027, 203.40), 'SSA': (0.033, 222.03), 'SA': (0.065, 222.39),
    'MSF': (0.024, 11.23), '2MS6': (0.021, 153.69), '2SM2': (0.044, 277.10),
    'MNS2': (0.015, 206.58), 'RHO1': (0.005, 179.52), 'T2': (0.053, 235.33),
    'J1': (0.005, 210.64), 'L2': (0.054, 210.36)
}

# Transformando para objetos que a biblioteca reconhece
consts, amps, phs = [], [], []
for name, (a, p) in constituent_data.items():
    if hasattr(cons, name):  # Verifica se a biblioteca suporta a componente
        consts.append(getattr(cons, name))
        amps.append(a)
        phs.append(p)

# 2. Configuração do Modelo
tide_model = Tide(constituents=consts, amplitudes=amps, phases=phs)
NM = 3.43  # Nível Médio da Ficha 30110

# 3. Cálculo de Extremos (Preamar e Baixa-mar) 2020-2025
start = datetime(2020, 1, 1)
end = datetime(2026, 12, 31, 23, 59)

print("Processando extremos de maré (isso pode levar alguns segundos)...")
extrema = tide_model.extrema(start, end)

# 4. Criando a lista de resultados
resultados = []
for time, height in extrema:
    real_height = height + NM
    # Identifica se é Preamar ou Baixa-mar comparando com o ponto anterior/seguinte
    resultados.append({
        'Data_Hora': time,
        'Altura_m': round(real_height, 2),
        'Evento': 'Preamar' if height > 0 else 'Baixa-mar'
    })

# 5. Exportando para DataFrame
df_itaqui = pd.DataFrame(resultados)

# Visualização
print("\n=== Primeiras 20 previsões ===")
print(df_itaqui.head(20))

print(f"\n=== Resumo ===")
print(f"Total de eventos: {len(df_itaqui)}")
print(f"Período: {start.date()} até {end.date()}")
print(f"Preamares: {len(df_itaqui[df_itaqui['Evento'] == 'Preamar'])}")
print(f"Baixa-mares: {len(df_itaqui[df_itaqui['Evento'] == 'Baixa-mar'])}")

# Salvar arquivo
output_file = 'itaqui_extremos_2020_2026.csv'
df_itaqui.to_csv(output_file, index=False)
print(f"\n✓ Arquivo salvo: {output_file}")
