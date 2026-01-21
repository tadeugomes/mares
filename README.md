# Previsão de Marés - Brasil

Scripts para cálculo de preamares e baixa-mares de portos brasileiros utilizando constantes harmônicas oficiais da Marinha do Brasil (DHN - Diretoria de Hidrografia e Navegação).

## Portos Disponíveis

### 1. Porto de Itaqui (MA)
- **Ficha:** 30110
- **Tipo de Maré:** Macromaré (amplitude > 4m)
- **Nível Médio (NM):** 3.43 m
- **Constantes:** 35 componentes harmônicas
- **Script:** `previsao_mares_itaqui.py`
- **Saída:** `itaqui_extremos_2020_2026.csv`

### 2. Terminal Gás Sul - São Francisco do Sul (SC)
- **Ficha:** 60266 (F-41)
- **Tipo de Maré:** Micro-maré (amplitude < 2m)
- **Nível Médio (NM):** 1.11 m
- **Constantes:** 27 componentes harmônicas
- **Script:** `previsao_mares_tgs.py`
- **Saída:** `tgs_extremos_2020_2026.csv`

### 3. Porto de Santos (SP)
- **Carta:** 1712 - Ficha 50231 (TIPLAM)
- **Tipo de Maré:** Micro-maré (amplitude < 2m)
- **Nível Médio (NM):** 0.736 m
- **Constantes:** 28 componentes harmônicas
- **Script:** `previsao_mares_santos.py`
- **Saída:** `santos_extremos_2020_2026.csv`
- **⚠️ Observação:** Efeitos meteorológicos (ressacas) podem elevar o nível em +1m

### 4. Porto do Rio Grande (RS)
- **Carta:** 2101 - Ficha 60380 (F-41)
- **Tipo de Maré:** Maré Mista (micro-amplitude < 0.5m)
- **Nível Médio (NM):** 0.858 m
- **Constantes:** 35 componentes harmônicas
- **Script:** `previsao_mares_riograande.py`
- **Saída:** `riograande_extremos_2020_2026.csv`
- **Estabelecimento de Porto:** 7h 28m

### 5. Porto de Paranaguá (PR)
- **Ficha:** 60141
- **Tipo de Maré:** Micro-maré com distorção (amplitude < 2m)
- **Nível Médio (NM):** 0.937 m
- **Constantes:** 35 componentes harmônicas
- **Script:** `previsao_mares_paranagua.py`
- **Saída:** `paranagua_extremos_2020_2026.csv`
- **⚠️ Observação:** Distorção por águas rasas (M4, MS4) e influência meteorológica

## Descrição

Este projeto calcula os extremos de maré (preamares e baixa-mares) para diferentes portos brasileiros no período de 2020 a 2026, utilizando análise harmônica de componentes de maré.

### Constantes Harmônicas

Os modelos utilizam constantes harmônicas incluindo:
- **Principais semidiurnas:** M2, S2, N2, K2
- **Principais diurnas:** K1, O1, P1, Q1
- **Componentes de águas rasas:** M4, MS4, M6, MK3, S4, MN4
- **Componentes de longo período:** MF, MM, SSA, SA, MSF

### Diferenças Regionais

**Porto de Itaqui (MA):**
- Macromaré equatorial com grandes amplitudes (até 7 metros)
- Fortemente influenciado pela proximidade do equador
- Variação significativa entre marés de sizígia e quadratura

**Terminal Gás Sul (SC):**
- Micro-maré com amplitudes pequenas (geralmente 0.4m a 1.8m)
- Influência meteorológica proporcionalmente maior
- Variações mais sutis e regulares

**Porto de Santos (SP):**
- Micro-maré com amplitudes pequenas (geralmente 0.2m a 1.5m)
- **Forte influência meteorológica:** ressacas podem adicionar +1m ou mais
- Frentes frias e ventos sul causam sobre-elevação significativa
- Previsões astronômicas devem ser combinadas com previsões meteorológicas

**Porto do Rio Grande (RS):**
- Maré mista com amplitudes muito pequenas (< 0.5m)
- Menor amplitude de maré entre todos os portos do projeto
- Localizado em estuário, sofre influência de vazão fluvial
- Estabelecimento de porto de 7h 28m

**Porto de Paranaguá (PR):**
- Micro-maré com distorção significativa (amplitude ~2m)
- **Forte distorção de águas rasas:** constantes M4, MS4, M6 significativas
- A forma da onda de maré se deforma ao entrar na Baía de Paranaguá
- **Influência meteorológica:** ventos sul causam sobre-elevação
- Ideal para estudos de ML: maré astronômica + vento como features

## Instalação

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

Ou instalar manualmente:

```bash
pip install pandas numpy
```

## Uso

### Opção 1: Executar scripts diretamente

**Porto de Itaqui:**
```bash
python previsao_mares_itaqui.py
```

**Terminal Gás Sul:**
```bash
python previsao_mares_tgs.py
```

**Porto de Santos:**
```bash
python previsao_mares_santos.py
```

**Porto do Rio Grande:**
```bash
python previsao_mares_riograande.py
```

**Porto de Paranaguá:**
```bash
python previsao_mares_paranagua.py
```

### Opção 2: Usar script auxiliar interativo

```bash
chmod +x run.sh
./run.sh
```

O script auxiliar permite escolher qual porto você deseja calcular.

## Saída

Cada script gera:

1. **Console:** Exibe as primeiras 20 previsões e resumo estatístico
2. **Arquivo CSV:** Com todas as previsões de extremos de maré

### Formato do CSV

| Data_Hora | Altura_m | Evento |
|-----------|----------|--------|
| 2020-01-01 00:15:00 | 5.87 | Preamar |
| 2020-01-01 06:30:00 | 0.99 | Baixa-mar |

### Estrutura dos Dados

- **Data_Hora:** Timestamp do evento de maré (fuso horário UTC)
- **Altura_m:** Altura da maré em metros (já inclui o nível médio)
- **Evento:** Tipo do evento ("Preamar" ou "Baixa-mar")

## Arquivos do Projeto

```
mares/
├── previsao_mares_itaqui.py     # Script Porto de Itaqui
├── previsao_mares_tgs.py        # Script Terminal Gás Sul
├── previsao_mares_santos.py     # Script Porto de Santos
├── previsao_mares_riograande.py # Script Porto do Rio Grande
├── previsao_mares_paranagua.py  # Script Porto de Paranaguá
├── requirements.txt              # Dependências Python
├── run.sh                        # Script auxiliar de execução
└── README.md                     # Esta documentação
```

## Requisitos

- Python 3.7+
- pandas >= 1.3.0
- numpy >= 1.20.0

## Observações Técnicas

### Precisão
- As previsões são baseadas exclusivamente em componentes astronômicas
- Não incluem efeitos meteorológicos (vento, pressão atmosférica)
- Para navegação oficial, sempre consulte as Tábuas de Marés da DHN

### Fuso Horário
- Os horários são calculados em UTC
- Porto de Itaqui: UTC-3
- Terminal Gás Sul: UTC-3
- Porto de Santos: UTC-3
- Porto do Rio Grande: UTC-3
- Porto de Paranaguá: UTC-3

### Período de Validade
- Previsões calculadas para 2020-2026
- As constantes harmônicas são atualizadas periodicamente pela DHN

## Referências

- Marinha do Brasil - Centro de Hidrografia da Marinha (CHM)
- Diretoria de Hidrografia e Navegação (DHN)
- Fichas de Marés: https://www.marinha.mil.br/chm/

## Autor

Scripts baseados nas constantes harmônicas oficiais das fichas de maré da Marinha do Brasil.
