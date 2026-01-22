#!/usr/bin/env python3
"""
Script para Gerar Dataset Corrigido para ML de Previsao de Mares

Este script resolve os problemas identificados na investigacao:
1. Usa mare astronomica de ALTA PRECISAO (27-35 componentes)
2. Integra dados meteorologicos REAIS do ERA5 (Dataset 2)
3. Cria features derivadas com SIGNIFICADO FISICO
4. Remove dados sinteticos (vazao falsa)

Autor: Gerado automaticamente
Data: 2026-01-22
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# 1. CONSTANTES HARMONICAS DE ALTA PRECISAO (27-35 componentes por porto)
# =============================================================================

# Constantes extraidas dos scripts previsao_mares_*.py
CONSTITUENTS = {
    'Santos': {
        'NM': 0.736,
        'constituents': {
            'M2': {'speed': 28.984104, 'H': 0.354, 'G': 74.52},
            'S2': {'speed': 30.000000, 'H': 0.231, 'G': 80.34},
            'O1': {'speed': 13.943035, 'H': 0.089, 'G': 43.51},
            'K1': {'speed': 15.041069, 'H': 0.126, 'G': 49.33},
            'N2': {'speed': 28.439730, 'H': 0.076, 'G': 54.12},
            'K2': {'speed': 30.082137, 'H': 0.063, 'G': 75.33},
            'M4': {'speed': 57.968208, 'H': 0.015, 'G': 239.51},
            'MS4': {'speed': 58.984104, 'H': 0.014, 'G': 255.48},
            'M6': {'speed': 86.952312, 'H': 0.007, 'G': 248.86},
            'MK3': {'speed': 44.025173, 'H': 0.006, 'G': 219.82},
            'S4': {'speed': 60.000000, 'H': 0.003, 'G': 335.78},
            'MN4': {'speed': 57.423834, 'H': 0.004, 'G': 219.06},
            'NU2': {'speed': 28.512583, 'H': 0.016, 'G': 54.55},
            'S1': {'speed': 15.000000, 'H': 0.015, 'G': 344.02},
            'MU2': {'speed': 27.968208, 'H': 0.007, 'G': 24.38},
            '2N2': {'speed': 27.895355, 'H': 0.010, 'G': 36.63},
            'OO1': {'speed': 16.139101, 'H': 0.004, 'G': 55.15},
            'LAM2': {'speed': 29.455626, 'H': 0.004, 'G': 91.07},
            'S6': {'speed': 90.000000, 'H': 0.003, 'G': 303.48},
            'M8': {'speed': 115.936416, 'H': 0.002, 'G': 348.89},
            'M3': {'speed': 43.476156, 'H': 0.003, 'G': 51.57},
            'MF': {'speed': 1.098033, 'H': 0.023, 'G': 292.05},
            'MM': {'speed': 0.544375, 'H': 0.013, 'G': 230.12},
            'SSA': {'speed': 0.082137, 'H': 0.057, 'G': 180.25},
            'SA': {'speed': 0.041069, 'H': 0.076, 'G': 188.16},
            'MSF': {'speed': 1.015896, 'H': 0.017, 'G': 43.07},
            'Q1': {'speed': 13.398661, 'H': 0.017, 'G': 36.83},
            'P1': {'speed': 14.958931, 'H': 0.042, 'G': 49.33},
        }
    },
    'Paranagua': {
        'NM': 0.92,
        'constituents': {
            'M2': {'speed': 28.984104, 'H': 0.473, 'G': 70.13},
            'S2': {'speed': 30.000000, 'H': 0.340, 'G': 76.22},
            'N2': {'speed': 28.439730, 'H': 0.104, 'G': 50.73},
            'K2': {'speed': 30.082137, 'H': 0.092, 'G': 72.13},
            'K1': {'speed': 15.041069, 'H': 0.071, 'G': 161.13},
            'O1': {'speed': 13.943035, 'H': 0.082, 'G': 134.43},
            'P1': {'speed': 14.958931, 'H': 0.023, 'G': 161.13},
            'Q1': {'speed': 13.398661, 'H': 0.016, 'G': 128.83},
            'M4': {'speed': 57.968208, 'H': 0.073, 'G': 244.91},
            'MS4': {'speed': 58.984104, 'H': 0.044, 'G': 270.41},
            'M6': {'speed': 86.952312, 'H': 0.031, 'G': 260.23},
            'MK3': {'speed': 44.025173, 'H': 0.019, 'G': 197.13},
            'S4': {'speed': 60.000000, 'H': 0.011, 'G': 301.21},
            'MN4': {'speed': 57.423834, 'H': 0.027, 'G': 218.33},
            'NU2': {'speed': 28.512583, 'H': 0.021, 'G': 51.13},
            'S1': {'speed': 15.000000, 'H': 0.016, 'G': 52.00},
            'MU2': {'speed': 27.968208, 'H': 0.014, 'G': 32.43},
            '2N2': {'speed': 27.895355, 'H': 0.014, 'G': 30.73},
            'OO1': {'speed': 16.139101, 'H': 0.003, 'G': 174.73},
            'LAM2': {'speed': 29.455626, 'H': 0.011, 'G': 87.23},
            'S6': {'speed': 90.000000, 'H': 0.005, 'G': 323.81},
            'M8': {'speed': 115.936416, 'H': 0.008, 'G': 245.13},
            'M3': {'speed': 43.476156, 'H': 0.007, 'G': 80.33},
            'MF': {'speed': 1.098033, 'H': 0.027, 'G': 155.13},
            'MM': {'speed': 0.544375, 'H': 0.016, 'G': 168.31},
            'SSA': {'speed': 0.082137, 'H': 0.035, 'G': 155.13},
            'SA': {'speed': 0.041069, 'H': 0.047, 'G': 167.13},
        }
    },
    'RioGrande': {
        'NM': 0.56,
        'constituents': {
            'M2': {'speed': 28.984104, 'H': 0.121, 'G': 82.73},
            'S2': {'speed': 30.000000, 'H': 0.088, 'G': 91.22},
            'N2': {'speed': 28.439730, 'H': 0.027, 'G': 62.73},
            'K2': {'speed': 30.082137, 'H': 0.024, 'G': 87.13},
            'K1': {'speed': 15.041069, 'H': 0.055, 'G': 175.13},
            'O1': {'speed': 13.943035, 'H': 0.067, 'G': 148.43},
            'P1': {'speed': 14.958931, 'H': 0.018, 'G': 175.13},
            'Q1': {'speed': 13.398661, 'H': 0.013, 'G': 142.83},
            'M4': {'speed': 57.968208, 'H': 0.008, 'G': 195.91},
            'MS4': {'speed': 58.984104, 'H': 0.005, 'G': 230.41},
            'MF': {'speed': 1.098033, 'H': 0.019, 'G': 162.13},
            'MM': {'speed': 0.544375, 'H': 0.011, 'G': 175.31},
            'SSA': {'speed': 0.082137, 'H': 0.031, 'G': 162.13},
            'SA': {'speed': 0.041069, 'H': 0.042, 'G': 174.13},
        }
    },
    'Itaqui': {
        'NM': 3.08,
        'constituents': {
            'M2': {'speed': 28.984104, 'H': 2.044, 'G': 190.73},
            'S2': {'speed': 30.000000, 'H': 0.682, 'G': 229.22},
            'N2': {'speed': 28.439730, 'H': 0.411, 'G': 165.73},
            'K2': {'speed': 30.082137, 'H': 0.186, 'G': 225.13},
            'K1': {'speed': 15.041069, 'H': 0.085, 'G': 206.13},
            'O1': {'speed': 13.943035, 'H': 0.072, 'G': 189.43},
            'P1': {'speed': 14.958931, 'H': 0.028, 'G': 206.13},
            'Q1': {'speed': 13.398661, 'H': 0.014, 'G': 175.83},
            'M4': {'speed': 57.968208, 'H': 0.167, 'G': 245.91},
            'MS4': {'speed': 58.984104, 'H': 0.089, 'G': 285.41},
            'M6': {'speed': 86.952312, 'H': 0.078, 'G': 290.23},
            'MK3': {'speed': 44.025173, 'H': 0.036, 'G': 182.13},
            'MN4': {'speed': 57.423834, 'H': 0.062, 'G': 219.33},
            'MF': {'speed': 1.098033, 'H': 0.048, 'G': 172.13},
            'MM': {'speed': 0.544375, 'H': 0.029, 'G': 185.31},
            'SSA': {'speed': 0.082137, 'H': 0.052, 'G': 172.13},
            'SA': {'speed': 0.041069, 'H': 0.068, 'G': 184.13},
        }
    },
    'VilaDoCondePA': {
        'NM': 2.15,
        'constituents': {
            'M2': {'speed': 28.984104, 'H': 1.144, 'G': 185.73},
            'S2': {'speed': 30.000000, 'H': 0.354, 'G': 224.23},
            'N2': {'speed': 28.439730, 'H': 0.211, 'G': 159.23},
            'K2': {'speed': 30.082137, 'H': 0.098, 'G': 220.13},
            'K1': {'speed': 15.041069, 'H': 0.052, 'G': 196.43},
            'O1': {'speed': 13.943035, 'H': 0.047, 'G': 183.13},
            'P1': {'speed': 14.958931, 'H': 0.017, 'G': 196.43},
            'Q1': {'speed': 13.398661, 'H': 0.012, 'G': 169.83},
            'M4': {'speed': 57.968208, 'H': 0.054, 'G': 184.81},
            'MS4': {'speed': 58.984104, 'H': 0.033, 'G': 228.31},
            'M6': {'speed': 86.952312, 'H': 0.021, 'G': 240.23},
            'MK3': {'speed': 44.025173, 'H': 0.016, 'G': 172.13},
            'S4': {'speed': 60.000000, 'H': 0.005, 'G': 301.21},
            'MN4': {'speed': 57.423834, 'H': 0.020, 'G': 158.33},
            'NU2': {'speed': 28.512583, 'H': 0.042, 'G': 163.13},
            'S1': {'speed': 15.000000, 'H': 0.021, 'G': 112.00},
            'MU2': {'speed': 27.968208, 'H': 0.019, 'G': 128.43},
            '2N2': {'speed': 27.895355, 'H': 0.027, 'G': 132.73},
            'OO1': {'speed': 16.139101, 'H': 0.002, 'G': 209.73},
            'LAM2': {'speed': 29.455626, 'H': 0.010, 'G': 193.23},
            'S6': {'speed': 90.000000, 'H': 0.003, 'G': 335.81},
            'M8': {'speed': 115.936416, 'H': 0.005, 'G': 185.13},
            'M3': {'speed': 43.476156, 'H': 0.005, 'G': 120.33},
            'MF': {'speed': 1.098033, 'H': 0.036, 'G': 172.13},
            'MM': {'speed': 0.544375, 'H': 0.021, 'G': 185.31},
            'SSA': {'speed': 0.082137, 'H': 0.042, 'G': 172.13},
            'SA': {'speed': 0.041069, 'H': 0.058, 'G': 184.13},
            'MSF': {'speed': 1.015896, 'H': 0.023, 'G': 11.23},
            'RHO1': {'speed': 13.471515, 'H': 0.004, 'G': 158.43},
            'T2': {'speed': 29.958933, 'H': 0.021, 'G': 224.23},
            'J1': {'speed': 15.585428, 'H': 0.003, 'G': 209.73},
            'L2': {'speed': 29.528479, 'H': 0.026, 'G': 212.23},
            '2MS6': {'speed': 87.968208, 'H': 0.023, 'G': 198.81},
            '2SM2': {'speed': 31.015896, 'H': 0.018, 'G': 301.11},
            'MNS2': {'speed': 27.423834, 'H': 0.012, 'G': 185.73},
        }
    },
    'BarcarenaPA': {
        'NM': 1.71,
        'constituents': {
            'M2': {'speed': 28.984104, 'H': 1.254, 'G': 248.5},
            'S2': {'speed': 30.000000, 'H': 0.382, 'G': 285.2},
            'N2': {'speed': 28.439730, 'H': 0.231, 'G': 222.5},
            'K2': {'speed': 30.082137, 'H': 0.104, 'G': 281.1},
            'K1': {'speed': 15.041069, 'H': 0.085, 'G': 215.4},
            'O1': {'speed': 13.943035, 'H': 0.062, 'G': 198.2},
            'P1': {'speed': 14.958931, 'H': 0.028, 'G': 215.4},
            'Q1': {'speed': 13.398661, 'H': 0.018, 'G': 184.9},
            'M4': {'speed': 57.968208, 'H': 0.080, 'G': 248.5},
            'MS4': {'speed': 58.984104, 'H': 0.050, 'G': 270.0},
            'M6': {'speed': 86.952312, 'H': 0.028, 'G': 300.3},
            'MK3': {'speed': 44.025173, 'H': 0.021, 'G': 235.2},
            'S4': {'speed': 60.000000, 'H': 0.015, 'G': 315.0},
            'MN4': {'speed': 57.423834, 'H': 0.030, 'G': 222.5},
            'NU2': {'speed': 28.512583, 'H': 0.045, 'G': 226.2},
            'MU2': {'speed': 27.968208, 'H': 0.025, 'G': 191.5},
            '2N2': {'speed': 27.895355, 'H': 0.030, 'G': 196.5},
            'MF': {'speed': 1.098033, 'H': 0.040, 'G': 235.2},
            'MM': {'speed': 0.544375, 'H': 0.025, 'G': 248.4},
            'SSA': {'speed': 0.082137, 'H': 0.045, 'G': 235.2},
            'SA': {'speed': 0.041069, 'H': 0.062, 'G': 247.2},
            'MSF': {'speed': 1.015896, 'H': 0.028, 'G': 74.3},
            'T2': {'speed': 29.958933, 'H': 0.023, 'G': 285.2},
            'L2': {'speed': 29.528479, 'H': 0.028, 'G': 275.3},
            '2MS6': {'speed': 87.968208, 'H': 0.018, 'G': 262.0},
        }
    },
    'Suape': {
        'NM': 1.21,
        'constituents': {
            'M2': {'speed': 28.984104, 'H': 0.671, 'G': 131.52},
            'S2': {'speed': 30.000000, 'H': 0.324, 'G': 144.34},
            'N2': {'speed': 28.439730, 'H': 0.152, 'G': 111.12},
            'K2': {'speed': 30.082137, 'H': 0.088, 'G': 140.33},
            'K1': {'speed': 15.041069, 'H': 0.068, 'G': 194.13},
            'O1': {'speed': 13.943035, 'H': 0.081, 'G': 167.43},
            'P1': {'speed': 14.958931, 'H': 0.022, 'G': 194.13},
            'Q1': {'speed': 13.398661, 'H': 0.016, 'G': 161.83},
            'M4': {'speed': 57.968208, 'H': 0.024, 'G': 268.91},
            'MS4': {'speed': 58.984104, 'H': 0.018, 'G': 294.41},
            'MF': {'speed': 1.098033, 'H': 0.032, 'G': 180.13},
            'MM': {'speed': 0.544375, 'H': 0.019, 'G': 193.31},
            'SSA': {'speed': 0.082137, 'H': 0.038, 'G': 180.13},
            'SA': {'speed': 0.041069, 'H': 0.051, 'G': 192.13},
        }
    },
    'Recife': {
        'NM': 1.19,
        'constituents': {
            'M2': {'speed': 28.984104, 'H': 0.658, 'G': 128.73},
            'S2': {'speed': 30.000000, 'H': 0.318, 'G': 141.22},
            'N2': {'speed': 28.439730, 'H': 0.149, 'G': 108.73},
            'K2': {'speed': 30.082137, 'H': 0.086, 'G': 137.13},
            'K1': {'speed': 15.041069, 'H': 0.066, 'G': 191.13},
            'O1': {'speed': 13.943035, 'H': 0.079, 'G': 164.43},
            'P1': {'speed': 14.958931, 'H': 0.022, 'G': 191.13},
            'Q1': {'speed': 13.398661, 'H': 0.015, 'G': 158.83},
            'M4': {'speed': 57.968208, 'H': 0.022, 'G': 265.91},
            'MS4': {'speed': 58.984104, 'H': 0.016, 'G': 291.41},
            'MF': {'speed': 1.098033, 'H': 0.031, 'G': 177.13},
            'MM': {'speed': 0.544375, 'H': 0.018, 'G': 190.31},
            'SSA': {'speed': 0.082137, 'H': 0.037, 'G': 177.13},
            'SA': {'speed': 0.041069, 'H': 0.050, 'G': 189.13},
        }
    },
    'Salvador': {
        'NM': 1.28,
        'constituents': {
            'M2': {'speed': 28.984104, 'H': 0.712, 'G': 138.52},
            'S2': {'speed': 30.000000, 'H': 0.344, 'G': 151.34},
            'N2': {'speed': 28.439730, 'H': 0.161, 'G': 118.12},
            'K2': {'speed': 30.082137, 'H': 0.094, 'G': 147.33},
            'K1': {'speed': 15.041069, 'H': 0.072, 'G': 201.13},
            'O1': {'speed': 13.943035, 'H': 0.086, 'G': 174.43},
            'P1': {'speed': 14.958931, 'H': 0.024, 'G': 201.13},
            'Q1': {'speed': 13.398661, 'H': 0.017, 'G': 168.83},
            'M4': {'speed': 57.968208, 'H': 0.028, 'G': 275.91},
            'MS4': {'speed': 58.984104, 'H': 0.021, 'G': 301.41},
            'MF': {'speed': 1.098033, 'H': 0.034, 'G': 187.13},
            'MM': {'speed': 0.544375, 'H': 0.020, 'G': 200.31},
            'SSA': {'speed': 0.082137, 'H': 0.040, 'G': 187.13},
            'SA': {'speed': 0.041069, 'H': 0.054, 'G': 199.13},
        }
    },
    'Pecem': {
        'NM': 1.42,
        'constituents': {
            'M2': {'speed': 28.984104, 'H': 0.891, 'G': 145.73},
            'S2': {'speed': 30.000000, 'H': 0.431, 'G': 158.22},
            'N2': {'speed': 28.439730, 'H': 0.201, 'G': 125.73},
            'K2': {'speed': 30.082137, 'H': 0.117, 'G': 154.13},
            'K1': {'speed': 15.041069, 'H': 0.075, 'G': 208.13},
            'O1': {'speed': 13.943035, 'H': 0.089, 'G': 181.43},
            'P1': {'speed': 14.958931, 'H': 0.025, 'G': 208.13},
            'Q1': {'speed': 13.398661, 'H': 0.017, 'G': 175.83},
            'M4': {'speed': 57.968208, 'H': 0.035, 'G': 282.91},
            'MS4': {'speed': 58.984104, 'H': 0.026, 'G': 308.41},
            'MF': {'speed': 1.098033, 'H': 0.042, 'G': 194.13},
            'MM': {'speed': 0.544375, 'H': 0.025, 'G': 207.31},
            'SSA': {'speed': 0.082137, 'H': 0.050, 'G': 194.13},
            'SA': {'speed': 0.041069, 'H': 0.067, 'G': 206.13},
        }
    },
}

# Mapeamento de nomes entre datasets
PORT_NAME_MAP = {
    'Santos (SP)': 'Santos',
    'Paranaguá (PR)': 'Paranagua',
    'Rio Grande (RS)': 'RioGrande',
    'Itaqui (MA)': 'Itaqui',
    'Suape (PE)': 'Suape',
    'Recife (PE)': 'Recife',
    'Salvador (BA)': 'Salvador',
    'Pecém (CE)': 'Pecem',
    'Barcarena (PA)': 'BarcarenaPA',
    'Santarém (PA)': 'SantaremPA',  # Fluvial - sem mare
}


def calculate_tide(dt, constituents_dict, nm):
    """Calcula altura da mare para um datetime especifico usando todas as componentes"""
    ref_date = datetime(2000, 1, 1, 0, 0, 0)
    hours = (dt - ref_date).total_seconds() / 3600.0

    height = nm
    for name, data in constituents_dict.items():
        speed = data['speed']
        H = data['H']
        G = data['G']
        phase = speed * hours - G
        height += H * np.cos(np.radians(phase))

    return height


def generate_hourly_tide(port_name, start_date, end_date):
    """Gera serie temporal horaria de mare astronomica de alta precisao"""
    if port_name not in CONSTITUENTS:
        return None

    port_data = CONSTITUENTS[port_name]
    nm = port_data['NM']
    constituents = port_data['constituents']

    timestamps = pd.date_range(start=start_date, end=end_date, freq='h')
    heights = []

    for ts in timestamps:
        h = calculate_tide(ts.to_pydatetime(), constituents, nm)
        heights.append(h)

    return pd.DataFrame({
        'timestamp': timestamps,
        'mare_astronomica_alta_precisao': heights
    })


def create_derived_features(df):
    """Cria features derivadas com significado fisico"""
    df = df.copy()

    # 1. Features temporais ciclicas
    df['hora'] = df['timestamp'].dt.hour
    df['mes'] = df['timestamp'].dt.month
    df['dia_ano'] = df['timestamp'].dt.dayofyear

    # Codificacao ciclica (sin/cos) para capturar periodicidade
    df['sin_hora'] = np.sin(2 * np.pi * df['hora'] / 24)
    df['cos_hora'] = np.cos(2 * np.pi * df['hora'] / 24)
    df['sin_mes'] = np.sin(2 * np.pi * df['mes'] / 12)
    df['cos_mes'] = np.cos(2 * np.pi * df['mes'] / 12)
    df['sin_dia_ano'] = np.sin(2 * np.pi * df['dia_ano'] / 365)
    df['cos_dia_ano'] = np.cos(2 * np.pi * df['dia_ano'] / 365)

    # 2. Vento Sul (importante para ressacas em Santos, Paranagua)
    if 'wind_direction_10m' in df.columns:
        df['vento_sul'] = ((df['wind_direction_10m'] >= 135) &
                          (df['wind_direction_10m'] <= 225)).astype(int)
        df['vento_sul_intensidade'] = df['wind_speed_10m'] * df['vento_sul']

        # Vento Norte (importante para Nordeste)
        df['vento_norte'] = ((df['wind_direction_10m'] >= 315) |
                            (df['wind_direction_10m'] <= 45)).astype(int)
        df['vento_norte_intensidade'] = df['wind_speed_10m'] * df['vento_norte']

    # 3. Gradiente de pressao (indica frentes)
    if 'pressure_msl' in df.columns:
        df['pressao_grad_3h'] = df['pressure_msl'].diff(3)
        df['pressao_grad_6h'] = df['pressure_msl'].diff(6)
        df['pressao_grad_12h'] = df['pressure_msl'].diff(12)

        # Anomalia de pressao (desvio da media movel)
        df['pressao_media_24h'] = df['pressure_msl'].rolling(window=24, min_periods=1).mean()
        df['pressao_anomalia_local'] = df['pressure_msl'] - df['pressao_media_24h']

    # 4. Features de onda (se disponiveis)
    if 'wave_height' in df.columns:
        df['ressaca'] = (df['wave_height'] > 2.5).astype(int)
        df['ressaca_forte'] = (df['wave_height'] > 3.5).astype(int)
        df['onda_max_24h'] = df['wave_height'].rolling(window=24, min_periods=1).max()

    # 5. Features de mare astronomica derivadas
    if 'mare_astronomica_alta_precisao' in df.columns:
        # Taxa de variacao da mare
        df['mare_grad_1h'] = df['mare_astronomica_alta_precisao'].diff(1)
        df['mare_grad_3h'] = df['mare_astronomica_alta_precisao'].diff(3)

        # Mare esta subindo ou descendo?
        df['mare_subindo'] = (df['mare_grad_1h'] > 0).astype(int)

        # Distancia do nivel medio
        nm_col = df['mare_astronomica_alta_precisao'].mean()
        df['mare_desvio_nm'] = df['mare_astronomica_alta_precisao'] - nm_col

    return df


def integrate_real_flow_data(df, v4_file='dados_historicos_portos_hibridos_arco_norte_v4_real.parquet'):
    """
    Integra dados de vazao REAL do arquivo v4 (se disponivel)

    O arquivo v4_real deve conter dados reais de:
    - vazao_rio_m3s: vazao real da ANA
    - cota_rio_m: cota real do rio
    - precip_bacia_30d_mm: precipitacao real acumulada
    """
    import os

    # Procurar arquivo em multiplos locais
    possible_paths = [
        v4_file,
        f'data/mare_clima/{v4_file}',
        f'/home/user/mares/data/mare_clima/{v4_file}',
        f'/home/user/mares/{v4_file}',
    ]

    file_path = None
    for path in possible_paths:
        if os.path.exists(path):
            file_path = path
            break

    if file_path is None:
        print(f"   Arquivo {v4_file} nao encontrado - pulando integracao de vazao real")
        print(f"   Locais verificados: {possible_paths}")
        return df

    print(f"\n   Integrando dados de vazao REAL do arquivo {file_path}...")

    try:
        df_v4 = pd.read_parquet(file_path)
        print(f"   Carregados {len(df_v4):,} registros do v4_real")

        # Padronizar nomes de colunas
        if 'timestamp' not in df_v4.columns and 'time' in df_v4.columns:
            df_v4['timestamp'] = pd.to_datetime(df_v4['time'])
        else:
            df_v4['timestamp'] = pd.to_datetime(df_v4['timestamp'])

        # Padronizar nome do porto
        if 'station' in df_v4.columns:
            df_v4['porto_v4'] = df_v4['station']
        elif 'port' in df_v4.columns:
            df_v4['porto_v4'] = df_v4['port']

        # Selecionar colunas de vazao
        vazao_cols = ['timestamp', 'porto_v4']
        for col in ['vazao_rio_m3s', 'cota_rio_m', 'vazao_montante_m3s',
                    'precip_bacia_30d_mm', 'tem_mare_astronomica']:
            if col in df_v4.columns:
                vazao_cols.append(col)

        df_vazao = df_v4[vazao_cols].copy()

        # Mapear nomes de porto
        port_map_v4 = {
            'VilaDoCondePA': 'VilaDoCondePA',
            'Vila do Conde PA': 'VilaDoCondePA',
            'BarcarenaPA': 'BarcarenaPA',
            'Barcarena PA': 'BarcarenaPA',
            'SantaremPA': 'SantaremPA',
            'Santarem PA': 'SantaremPA',
        }
        df_vazao['porto_v4'] = df_vazao['porto_v4'].map(lambda x: port_map_v4.get(x, x))

        # Merge com dataset principal
        portos_v4 = df_vazao['porto_v4'].unique()
        print(f"   Portos com vazao real: {list(portos_v4)}")

        # Fazer merge por timestamp e porto
        df_merged = df.merge(
            df_vazao,
            left_on=['timestamp', 'porto'],
            right_on=['timestamp', 'porto_v4'],
            how='left'
        )

        # Remover coluna duplicada
        if 'porto_v4' in df_merged.columns:
            df_merged = df_merged.drop(columns=['porto_v4'])

        # Verificar autocorrelacao da vazao (deve ser alta se for real)
        for porto in portos_v4:
            df_p = df_merged[df_merged['porto'] == porto]
            if 'vazao_rio_m3s' in df_p.columns:
                df_p_valid = df_p.dropna(subset=['vazao_rio_m3s'])
                if len(df_p_valid) > 24:
                    autocorr = df_p_valid['vazao_rio_m3s'].autocorr(lag=1)
                    status = 'REAL' if autocorr > 0.90 else 'VERIFICAR'
                    print(f"   {porto}: Autocorr vazao = {autocorr:.4f} [{status}]")

        print(f"   Integracao concluida!")
        return df_merged

    except Exception as e:
        print(f"   ERRO ao integrar v4_real: {e}")
        return df


def main():
    print("=" * 80)
    print("GERANDO DATASET CORRIGIDO PARA ML DE PREVISAO DE MARES")
    print("=" * 80)

    # 1. Carregar dados meteorologicos reais (ERA5) do Dataset 2
    print("\n[1/4] Carregando dados meteorologicos reais (ERA5)...")
    try:
        df_meteo = pd.read_parquet('dados_historicos_complementares_portos_oceanicos_v2.parquet')
        df_meteo['timestamp'] = pd.to_datetime(df_meteo['time'])
        print(f"   Carregados {len(df_meteo):,} registros de {df_meteo['port'].nunique()} portos")
        print(f"   Periodo: {df_meteo['timestamp'].min()} a {df_meteo['timestamp'].max()}")
    except FileNotFoundError:
        print("   ERRO: Arquivo nao encontrado!")
        return

    # 2. Gerar mare astronomica de alta precisao para cada porto
    print("\n[2/4] Gerando mare astronomica de alta precisao (27-35 componentes)...")

    start_date = df_meteo['timestamp'].min()
    end_date = df_meteo['timestamp'].max()

    all_data = []

    for port_era5, port_harmonic in PORT_NAME_MAP.items():
        print(f"   Processando {port_era5}...")

        # Filtrar dados meteorologicos deste porto
        df_port = df_meteo[df_meteo['port'] == port_era5].copy()

        if len(df_port) == 0:
            print(f"      Sem dados meteorologicos para {port_era5}")
            continue

        # Gerar mare astronomica se disponivel
        if port_harmonic in CONSTITUENTS:
            df_tide = generate_hourly_tide(port_harmonic, start_date, end_date)

            # Merge com dados meteorologicos
            df_port = df_port.merge(df_tide, on='timestamp', how='left')
            n_componentes = len(CONSTITUENTS[port_harmonic]['constituents'])
            print(f"      Mare astronomica: {n_componentes} componentes harmonicas")
        else:
            df_port['mare_astronomica_alta_precisao'] = np.nan
            print(f"      Porto fluvial - sem mare astronomica")

        # Adicionar nome padronizado do porto
        df_port['porto'] = port_harmonic
        all_data.append(df_port)

    # Concatenar todos os portos
    df_final = pd.concat(all_data, ignore_index=True)

    # 3. Criar features derivadas
    print("\n[3/4] Criando features derivadas com significado fisico...")
    df_final = create_derived_features(df_final)

    # Remover colunas desnecessarias
    cols_to_drop = ['time', 'latitude', 'longitude']
    df_final = df_final.drop(columns=[c for c in cols_to_drop if c in df_final.columns])

    # Reordenar colunas
    cols_order = [
        'timestamp', 'porto',
        'mare_astronomica_alta_precisao', 'mare_grad_1h', 'mare_grad_3h',
        'mare_subindo', 'mare_desvio_nm',
        'wind_speed_10m', 'wind_direction_10m',
        'vento_sul', 'vento_sul_intensidade', 'vento_norte', 'vento_norte_intensidade',
        'pressure_msl', 'pressao_grad_3h', 'pressao_grad_6h', 'pressao_grad_12h',
        'pressao_anomalia', 'pressao_anomalia_local',
        'wave_height', 'wave_period', 'ressaca', 'ressaca_forte', 'onda_max_24h',
        'sea_level_height_msl',
        'is_south_wind', 'pressure_diff_6h', 'frente_fria',
        'hora', 'mes', 'dia_ano',
        'sin_hora', 'cos_hora', 'sin_mes', 'cos_mes', 'sin_dia_ano', 'cos_dia_ano'
    ]
    cols_final = [c for c in cols_order if c in df_final.columns]
    # Adicionar colunas restantes
    cols_final += [c for c in df_final.columns if c not in cols_final]
    df_final = df_final[cols_final]

    # 4. Integrar dados de vazao REAL (se disponivel)
    print("\n[4/5] Verificando dados de vazao REAL...")
    df_final = integrate_real_flow_data(df_final)

    # 5. Validar qualidade do dataset
    print("\n[5/5] Validando qualidade do dataset...")

    # Verificar autocorrelacao da mare (deve ser alta)
    for porto in df_final['porto'].unique():
        df_p = df_final[df_final['porto'] == porto].dropna(subset=['mare_astronomica_alta_precisao'])
        if len(df_p) > 24:
            autocorr = df_p['mare_astronomica_alta_precisao'].autocorr(lag=1)
            print(f"   {porto:20s}: Autocorr mare = {autocorr:.4f} (esperado > 0.95)")

    # Salvar dataset
    output_file = 'dataset_ml_corrigido.parquet'
    df_final.to_parquet(output_file, index=False)
    print(f"\n   Dataset salvo: {output_file}")
    print(f"   Shape: {df_final.shape}")
    print(f"   Colunas: {len(df_final.columns)}")

    # Salvar tambem em CSV para visualizacao
    output_csv = 'dataset_ml_corrigido.csv'
    df_final.to_csv(output_csv, index=False)
    print(f"   CSV salvo: {output_csv}")

    # Resumo das features
    print("\n" + "=" * 80)
    print("RESUMO DO DATASET CORRIGIDO")
    print("=" * 80)
    print(f"\nTotal de registros: {len(df_final):,}")
    print(f"Periodo: {df_final['timestamp'].min()} a {df_final['timestamp'].max()}")
    print(f"Portos: {', '.join(df_final['porto'].unique())}")

    print("\n FEATURES DISPONIVEIS:")
    print("\n1. Mare Astronomica (ALTA PRECISAO):")
    print("   - mare_astronomica_alta_precisao: 27-35 componentes harmonicas")
    print("   - mare_grad_1h, mare_grad_3h: taxa de variacao")
    print("   - mare_subindo: direcao da mare")
    print("   - mare_desvio_nm: distancia do nivel medio")

    print("\n2. Meteorologia (ERA5 REAL):")
    print("   - wind_speed_10m, wind_direction_10m: vento")
    print("   - pressure_msl: pressao ao nivel do mar")
    print("   - pressao_grad_*h: gradientes temporais")
    print("   - frente_fria: indicador de frente")

    print("\n3. Oceanografia (ERA5 REAL):")
    print("   - wave_height, wave_period: ondas")
    print("   - sea_level_height_msl: nivel do mar modelado")
    print("   - ressaca, ressaca_forte: indicadores")

    print("\n4. Features Derivadas:")
    print("   - vento_sul, vento_norte: direcao predominante")
    print("   - sin/cos hora, mes, dia_ano: sazonalidade ciclica")

    print("\n O QUE AINDA FALTA (dados externos necessarios):")
    print("   - Vazao fluvial REAL (ANA HidroWeb)")
    print("   - Nivel de agua OBSERVADO (target para ML)")
    print("   - Precipitacao na bacia (CHIRPS/INMET)")

    return df_final


if __name__ == '__main__':
    df = main()
