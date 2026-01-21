# Previsão de Marés - Porto de Itaqui

Script para cálculo de preamares e baixa-mares do Porto de Itaqui utilizando 35 constantes harmônicas da Ficha 30110.

## Descrição

Este projeto calcula os extremos de maré (preamares e baixa-mares) para o Porto de Itaqui no período de 2020 a 2026, utilizando análise harmônica com 35 componentes de maré.

### Constantes Harmônicas (Ficha 30110)

O modelo utiliza 35 constantes harmônicas incluindo:
- Principais semidiurnas: M2, S2, N2, K2
- Principais diurnas: K1, O1, P1, Q1
- Componentes de águas rasas: M4, MS4, M6, MK3, S4, MN4
- E outras 21 componentes adicionais

**Nível Médio (NM):** 3.43 m

## Instalação

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

Ou instalar manualmente:

```bash
pip install pandas pytides numpy
```

### 2. Executar o script

#### Opção 1: Diretamente com Python

```bash
python previsao_mares_itaqui.py
```

#### Opção 2: Usando o script auxiliar

```bash
chmod +x run.sh
./run.sh
```

## Saída

O script gera:

1. **Console:** Exibe as primeiras 20 previsões e um resumo estatístico
2. **Arquivo CSV:** `itaqui_extremos_2020_2026.csv` com todas as previsões

### Formato do CSV

| Data_Hora | Altura_m | Evento |
|-----------|----------|--------|
| 2020-01-01 00:15:00 | 5.87 | Preamar |
| 2020-01-01 06:30:00 | 0.99 | Baixa-mar |

## Estrutura dos Dados

- **Data_Hora:** Timestamp do evento de maré
- **Altura_m:** Altura da maré em metros (já inclui o nível médio)
- **Evento:** Tipo do evento ("Preamar" ou "Baixa-mar")

## Requisitos

- Python 3.7+
- pandas >= 1.3.0
- pytides >= 0.0.6
- numpy >= 1.20.0

## Autor

Script baseado nas constantes harmônicas da Ficha 30110 - Porto de Itaqui.
