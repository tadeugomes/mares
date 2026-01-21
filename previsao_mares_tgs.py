#!/usr/bin/env python3
"""
Script de Previsão de Marés - Terminal Gás Sul
Calcula preamares e baixa-mares usando constantes harmônicas
Ficha 60266 - Terminal Gás Sul, São Francisco do Sul (SC)
"""

import pandas as pd
from datetime import datetime
from pytides.tide import Tide
import pytides.constituent as cons

# 1. Cadastro das Constantes Harmônicas (Ficha 60266 - Terminal Gás Sul)
# Valores de H (Amplitude) e G (Fase) específicos de São Francisco do Sul
constituent_data = {
    'M2': (0.286, 77.26), 'S2': (0.245, 78.33), 'O1': (0.117, 45.42),
    'K1': (0.180, 54.76), 'N2': (0.052, 57.08), 'M4': (0.016, 215.11),
    'MS4': (0.017, 237.95), 'M6': (0.012, 194.57), 'MK3': (0.007, 185.73),
    'S4': (0.005, 305.86), 'MN4': (0.005, 172.50), 'NU2': (0.011, 51.52),
    'S1': (0.027, 26.27), 'MU2': (0.010, 24.38), '2N2': (0.007, 36.89),
    'OO1': (0.006, 64.09), 'LAM2': (0.002, 116.82), 'S6': (0.005, 306.96),
    'M8': (0.004, 273.66), 'M3': (0.004, 335.70), 'MF': (0.038, 301.99),
    'MM': (0.024, 226.54), 'SSA': (0.063, 172.90), 'SA': (0.084, 184.81),
    'MSF': (0.033, 49.33), 'Q1': (0.023, 38.08), 'P1': (0.060, 54.76)
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
NM = 1.11  # Nível Médio da Ficha 60266 (Terminal Gás Sul)

# 3. Cálculo de Extremos (Preamar e Baixa-mar) 2020-2026
start = datetime(2020, 1, 1)
end = datetime(2026, 12, 31, 23, 59)

print("Processando extremos de maré para Terminal Gás Sul...")
print("(isso pode levar alguns segundos)")
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
df_tgs = pd.DataFrame(resultados)

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
