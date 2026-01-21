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

### 6. Ilha da Paz - São Francisco do Sul (SC)
- **Ficha:** 60208
- **Tipo de Maré:** Micro-maré (amplitude < 2m)
- **Nível Médio (NM):** 0.781 m
- **Constantes:** 35 componentes harmônicas
- **Script:** `previsao_mares_ilhadapaz.py`
- **Saída:** `ilhadapaz_extremos_2020_2026.csv`
- **Localização:** Baía da Babitonga, Santa Catarina
- **Estação Sentinela:** Referência para Itapoá e São Francisco do Sul
- **Nota:** Serve como previsão para ambos os portos da região

### 7. Vila do Conde - Barcarena (PA)
- **Ficha:** 10566
- **Tipo de Maré:** Grande amplitude com forte distorção fluvial (~3m)
- **Nível Médio (NM):** 2.15 m
- **Constantes:** 35 componentes harmônicas
- **Script:** `previsao_mares_viladoconde.py`
- **Saída:** `viladoconde_extremos_2020_2026.csv`
- **Localização:** Baía de Marajó - Foz do Rio Amazonas
- **⚠️ Observação:** Forte influência fluvial (Amazonas/Tocantins) e distorção de águas rasas
- **Nota:** Segunda maior amplitude do projeto, assimetria pronunciada (sobe mais rápido que desce)

### 8. Paranaguá Cais Oeste I (PR)
- **Ficha:** 60151
- **Tipo de Maré:** Micro-maré com distorção (amplitude < 2m)
- **Nível Médio (NM):** 0.916 m
- **Constantes:** 35 componentes harmônicas
- **Script:** `previsao_mares_paranagua_cais_oeste.py`
- **Saída:** `paranagua_cais_oeste_extremos_2020_2026.csv`
- **Localização:** Interior da Baía de Paranaguá (mais para oeste)
- **Par com:** Paranaguá Cais Leste/TCP (Ficha 60141)
- **⚠️ Observação:** Complementa Cais Leste para modelagem de gradiente e propagação no canal
- **Para ML:** Lag temporal entre Cais Oeste e Cais Leste permite prever velocidade de propagação da onda de maré

### 9. Porto de Antonina (PR)
- **Ficha:** 60110
- **Tipo de Maré:** Micro-maré com amplificação por efeito funil
- **Nível Médio (NM):** 1.11 m
- **Constantes:** 35 componentes harmônicas
- **Script:** `previsao_mares_antonina.py`
- **Saída:** `antonina_extremos_2020_2026.csv`
- **Localização:** Fundo da Baía de Paranaguá (mais interior)
- **Conjunto completo:** Cais Leste → Cais Oeste I → Antonina
- **⚠️ Observação:** Efeito funil amplifica a maré (M2: 0.536m > Cais Leste: 0.470m)
- **⚠️ Atraso da onda:** Fase M2: 100.2° (vs Cais Leste: 85.5°) = ~14.7° de diferença
- **Para ML:** Amplificação + lag temporal permitem modelar como a maré se propaga e intensifica ao longo da baía

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

**Sistema Completo da Baía de Paranaguá (PR):**
- Micro-maré com distorção significativa (amplitude ~2m)
- **Forte distorção de águas rasas:** constantes M4, MS4, M6 significativas
- A forma da onda de maré se deforma ao entrar na Baía de Paranaguá
- **Influência meteorológica:** ventos sul causam sobre-elevação
- **Três estações disponíveis formando gradiente espacial:**
  - **Cais Leste/TCP (Ficha 60141):** NM = 0.937m, entrada da baía, M2 = 0.470m, Fase = 85.5°
  - **Cais Oeste I (Ficha 60151):** NM = 0.916m, meio da baía, M2 = 0.470m, Fase = 85.5°
  - **Antonina (Ficha 60110):** NM = 1.11m, fundo da baía, M2 = 0.536m, Fase = 100.2°
- **Efeito funil:** A baía estreita em direção a Antonina, amplificando a maré (M2 aumenta 14% de Cais Leste para Antonina)
- **Gradiente de fase:** ~14.7° de diferença entre Cais Leste e Antonina representa o tempo de propagação da onda ao longo da baía
- **Para ML:** Conjunto único permitindo modelar amplificação, atenuação, atraso e distorção da onda de maré em um estuário

**Ilha da Paz - São Francisco do Sul (SC):**
- Micro-maré oceânica (amplitude ~1.5m)
- Localizada na Baía da Babitonga
- Comportamento similar ao Terminal Gás Sul (mesma região)
- Menor influência de águas rasas comparado a Paranaguá
- **Estação sentinela:** Serve de referência para portos próximos (Itapoá, São Francisco do Sul)
- **Para ML:** O lag temporal entre Ilha da Paz e portos internos da baía é feature forte para prever propagação da onda de maré

**Vila do Conde - Barcarena (PA):**
- Grande amplitude com forte distorção (~3m - segunda maior do projeto)
- **Localização fascinante:** Foz do Rio Amazonas (Baía de Marajó)
- **Influência fluvial extrema:** Gigantesco volume de água doce do Amazonas/Tocantins
- **Distorção de águas rasas pronunciada:** M4 (0.054m) e M6 (0.021m) muito significativas
- **Assimetria:** Maré sobe mais rápido do que desce
- **Para ML:** Vazão fluvial (Amazonas/Tocantins) é feature crítica para desvios sazonais

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

**Porto de Paranaguá - Cais Oeste I:**
```bash
python previsao_mares_paranagua_cais_oeste.py
```

**Porto de Antonina:**
```bash
python previsao_mares_antonina.py
```

**Ilha da Paz:**
```bash
python previsao_mares_ilhadapaz.py
```

**Vila do Conde:**
```bash
python previsao_mares_viladoconde.py
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
├── previsao_mares_itaqui.py              # Script Porto de Itaqui
├── previsao_mares_tgs.py                 # Script Terminal Gás Sul
├── previsao_mares_santos.py              # Script Porto de Santos
├── previsao_mares_riograande.py          # Script Porto do Rio Grande
├── previsao_mares_paranagua.py           # Script Porto de Paranaguá (Cais Leste/TCP)
├── previsao_mares_paranagua_cais_oeste.py # Script Paranaguá Cais Oeste I
├── previsao_mares_antonina.py            # Script Porto de Antonina
├── previsao_mares_ilhadapaz.py           # Script Ilha da Paz
├── previsao_mares_viladoconde.py         # Script Vila do Conde
├── requirements.txt                       # Dependências Python
├── run.sh                                 # Script auxiliar de execução
└── README.md                              # Esta documentação
```

## Requisitos

- Python 3.7+
- pandas >= 1.3.0
- numpy >= 1.20.0

## Observações Técnicas

### Precisão e Limitações

**Previsões Astronômicas (este projeto):**
- ✅ Baseadas exclusivamente em componentes astronômicas (Lua, Sol)
- ❌ **NÃO incluem** efeitos meteorológicos (vento, pressão atmosférica)
- ❌ **NÃO incluem** efeitos fluviais (vazão de rios)
- ❌ **NÃO incluem** efeitos de ondas (ressacas)

**Quando usar este projeto:**
- ✅ Portos oceânicos e costeiros (baseline confiável)
- ✅ Portos estuarinos como **baseline** + correções de ML
- ✅ Estudo de propagação de marés em baías
- ✅ Feature engineering para modelos de ML

**Quando NÃO usar (ou usar com muito cuidado):**
- ⚠️ Portos puramente fluviais (ex: Manaus) - maré astronômica é insignificante
- ⚠️ Períodos de ressaca (Santos, Rio de Janeiro) - erro pode ser >1m
- ⚠️ Períodos de cheia na Amazônia (Vila do Conde) - vazão domina
- ⚠️ Vento sul forte (Rio Grande, Santos) - sobre-elevação significativa

**Para navegação oficial:** Sempre consulte as Tábuas de Marés da DHN

### Fuso Horário
- Os horários são calculados em UTC
- Porto de Itaqui: UTC-3
- Terminal Gás Sul: UTC-3
- Porto de Santos: UTC-3
- Porto do Rio Grande: UTC-3
- Porto de Paranaguá (todos): UTC-3
- Porto de Antonina: UTC-3
- Ilha da Paz: UTC-3
- Vila do Conde: UTC-3

### Período de Validade
- Previsões calculadas para 2020-2026
- As constantes harmônicas são atualizadas periodicamente pela DHN

### Como Identificar se um Porto tem Maré Astronômica Significativa

**Indicadores de que o porto TEM maré astronômica (análise harmônica é válida):**
- ✅ Amplitude M2 > 0.05m (quanto maior, mais confiável)
- ✅ Componentes semidiurnas (M2, S2) são as maiores do espectro
- ✅ Localizado < 100km da costa (varia por estuário)
- ✅ DHN publica Tábua de Marés para o local
- ✅ Variação de nível tem período dominante de ~12.4h

**Indicadores de porto PURAMENTE fluvial (análise harmônica NÃO funciona):**
- ❌ Amplitude M2 < 0.01m (praticamente zero)
- ❌ Localizado muito longe da costa (>200km rio acima)
- ❌ Variação dominante é sazonal (meses, não horas)
- ❌ DHN não publica tábuas de marés para o local
- ❌ Variação de nível correlaciona com precipitação/vazão, não com fase da Lua

**Exemplos de portos puramente fluviais no Brasil:**
- Manaus (AM) - Variação ~10-15m anual, 100% fluvial
- Porto Velho (RO) - Variação fluvial
- Corumbá (MS) - Variação fluvial (Pantanal)

Para esses portos, você precisa de um **modelo hidrológico**, não harmônico.

## Aplicações em Machine Learning

### Ilha da Paz como Estação Sentinela

A Ilha da Paz funciona como uma **estação sentinela** para a região da Baía da Babitonga:

**Portos de referência:**
- Itapoá (SC)
- São Francisco do Sul (SC)
- Outros portos internos da Baía da Babitonga

**Feature de lag temporal:**
A diferença de tempo entre o pico da maré na Ilha da Paz (oceânica) e o pico dentro da baía é uma característica muito forte para prever a propagação da onda de maré. Em modelos de ML, use:

```python
# Exemplo de feature engineering
lag_ilha_porto = tempo_preamar_porto_interno - tempo_preamar_ilha_da_paz
```

### Outras Aplicações de ML

**Sistema Completo da Baía de Paranaguá - Modelagem de Propagação e Amplificação:**

Ter três estações em Paranaguá (Cais Leste, Cais Oeste I, e Antonina) permite modelar o gradiente completo de pressão, amplificação por efeito funil, e o tempo de deslocamento da massa de água ao longo de toda a baía:

```python
# Features de lag temporal entre estações (propagação da onda)
lag_leste_oeste = tempo_preamar_oeste - tempo_preamar_leste
lag_oeste_antonina = tempo_preamar_antonina - tempo_preamar_oeste
lag_total = tempo_preamar_antonina - tempo_preamar_leste

# Features de gradiente de altura
gradiente_leste_oeste = altura_leste - altura_oeste
gradiente_oeste_antonina = altura_oeste - altura_antonina

# Feature de amplificação (efeito funil)
# M2 aumenta de 0.470m (Cais Leste) para 0.536m (Antonina) = 14% de amplificação
fator_amplificacao = amplitude_antonina / amplitude_cais_leste

# Feature de diferença de fase (usando M2)
# Fase Antonina: 100.2° vs Fase Cais Leste: 85.5° = 14.7° de atraso
diferenca_fase_M2 = fase_M2_antonina - fase_M2_cais_leste
# Converter para tempo: 14.7° / (360°/12.42h) ≈ 30 minutos de atraso

# Velocidade de propagação da onda de maré na baía
velocidade_propagacao = distancia_total_baia / lag_total
```

**Aplicações práticas:**
- Prever condições de corrente em qualquer ponto da baía
- Otimizar janelas de manobra para navios de grande porte em diferentes portos
- Estimar tempo de chegada da maré em diferentes pontos (Paranaguá → Antonina)
- Corrigir efeitos de atrito, distorção e amplificação ao longo da baía
- Modelar efeito funil: como o estreitamento da baía amplifica a maré
- Prever inundações no fundo da baía (Antonina) com base em observações na entrada (Cais Leste)

---

## Variáveis Complementares para Machine Learning

As previsões astronômicas (fornecidas por este projeto) são apenas o **baseline**. Para portos estuarinos e costeiros, você precisa de variáveis adicionais para capturar desvios causados por rios, vento, pressão e ondas.

### 📊 Classificação dos Portos e Variáveis Necessárias

#### **Tipo 1: Portos Oceânicos/Costeiros**
**Exemplos:** Itaqui (MA), Santos (SP), Ilha da Paz (SC)

**Variáveis necessárias:**

| Variável | Importância | Fonte de Dados (Brasil) | Detalhes |
|----------|-------------|-------------------------|----------|
| **Maré astronômica** | ⭐⭐⭐⭐⭐ | Este projeto | Baseline principal |
| **Vento (vel. e dir.)** | ⭐⭐⭐⭐ | INMET, Copernicus Marine | Ventos sul causam sobre-elevação |
| **Pressão atmosférica** | ⭐⭐⭐ | INMET | Efeito de barômetro invertido (~1cm/hPa) |
| **Altura de onda** | ⭐⭐⭐ | Copernicus Marine, SMC-Brasil | Ressacas podem adicionar +1m |
| **Período de onda** | ⭐⭐ | Copernicus Marine | Ondas longas penetram mais no porto |

**Exemplo: Porto de Santos**
```python
features = {
    'mare_astronomica': altura_prevista_harmonica,      # Este projeto
    'vento_sul_intensidade': max(vel_vento_sul_48h),   # INMET
    'vento_sul_persistencia': horas_vento_sul,         # INMET
    'pressao_atm': pressao_atual - pressao_media,      # INMET (anomalia)
    'altura_onda_significativa': Hs,                    # Copernicus/SMC
    'periodo_onda': Tp,                                 # Copernicus
    'frente_fria': booleano_frente_proximas_48h,      # CPTEC/INPE
}
```

---

#### **Tipo 2: Portos Estuarinos com Influência Fluvial Moderada**
**Exemplos:** Rio Grande (RS), Paranaguá (PR), Antonina (PR)

**Variáveis necessárias:**

| Variável | Importância | Fonte de Dados (Brasil) | Detalhes |
|----------|-------------|-------------------------|----------|
| **Maré astronômica** | ⭐⭐⭐⭐ | Este projeto | Ainda dominante |
| **Vazão fluvial** | ⭐⭐⭐⭐ | ANA (HidroWeb) | Pode adicionar +0.2 a +0.5m ao NM |
| **Vento (vel. e dir.)** | ⭐⭐⭐⭐ | INMET | Vento sul "empurra" água para dentro |
| **Precipitação (bacia)** | ⭐⭐⭐ | ANA, INMET | Indica vazão futura |
| **Pressão atmosférica** | ⭐⭐ | INMET | Menos relevante que vento |

**Exemplo: Porto do Rio Grande (RS)**
```python
features = {
    'mare_astronomica': altura_prevista_harmonica,         # Este projeto (pequena)
    'vazao_lagoa_dos_patos': vazao_m3_s,                  # ANA (estações próximas)
    'vento_sul_vel': velocidade_vento_sul,                # INMET Rio Grande
    'vento_sul_duracao': horas_consecutivas_vento_sul,    # INMET
    'chuva_bacia_30d': precipitacao_acumulada_30dias,     # ANA/INMET (bacia)
    'nivel_lagoa_guaiba': nivel_agua_guaiba,              # ANA (montante)
    'mare_meteorologica': desvio_observado - astronomico, # Calcular com dados históricos
}
```

**Exemplo: Antonina (PR)**
```python
features = {
    'mare_astronomica_antonina': altura_prevista_harmonica,     # Este projeto
    'mare_astronomica_cais_leste': altura_cais_leste,          # Sentinel (propagação)
    'lag_temporal': tempo_preamar_leste - tempo_preamar_antonina, # Feature chave
    'vazao_rios_locais': vazao_rios_pequenos_bacia,            # ANA (se disponível)
    'vento_sul_vel': velocidade_vento_sul,                     # INMET Paranaguá
    'chuva_local_7d': precipitacao_acumulada_7dias,            # INMET
}
```

---

#### **Tipo 3: Portos em Foz de Grandes Rios (Híbrido Complexo)**
**Exemplos:** Vila do Conde (PA)

**Variáveis necessárias:**

| Variável | Importância | Fonte de Dados (Brasil) | Detalhes |
|----------|-------------|-------------------------|----------|
| **Maré astronômica** | ⭐⭐⭐⭐ | Este projeto | Base, mas vazão pode dominar |
| **Vazão Rio Amazonas** | ⭐⭐⭐⭐⭐ | ANA (Óbidos) | CRÍTICO - pode adicionar +2m na cheia |
| **Vazão Rio Tocantins** | ⭐⭐⭐⭐ | ANA (Tucuruí) | Contribui significativamente |
| **Precipitação Amazônia** | ⭐⭐⭐ | ANA, INMET, CHIRPS | Indica vazão futura (lag ~30-60 dias) |
| **Sazonalidade** | ⭐⭐⭐⭐ | Mês do ano | Cheia (mar-mai) vs Seca (set-nov) |
| **Vento local** | ⭐⭐ | INMET Belém/Barcarena | Menos relevante que vazão |

**Exemplo: Vila do Conde (PA)**
```python
features = {
    # Astronômica (baseline)
    'mare_astronomica': altura_prevista_harmonica,           # Este projeto

    # Fluvial (DOMINANTE em alguns períodos)
    'vazao_amazonas_obidos': vazao_m3_s,                    # ANA (Óbidos - estação 15400000)
    'vazao_tocantins_tucurui': vazao_m3_s,                  # ANA (Tucuruí)
    'vazao_total': vazao_amazonas + vazao_tocantins,

    # Sazonalidade
    'mes': mes_do_ano,                                       # 1-12
    'estacao_hidrologica': 'cheia' | 'vazante' | 'seca',    # Classificação

    # Precipitação (feature antecedente)
    'chuva_amazonia_30d': precip_acumulada_bacia_30d,       # CHIRPS/ANA
    'chuva_amazonia_60d': precip_acumulada_bacia_60d,       # Lag maior

    # Meteorológico
    'vento_vel': velocidade_vento,                           # INMET
    'pressao': pressao_atm,                                  # INMET

    # Target
    'nivel_observado': altura_real_medida,                   # Régua/Sensor local
}

# Modelo de correção
desvio_fluvial = modelo_ML.predict(features) - mare_astronomica
nivel_final = mare_astronomica + desvio_fluvial
```

---

### 🌐 Fontes de Dados Brasileiras

#### **1. Dados Fluviais (Vazão e Nível)**

**ANA - Agência Nacional de Águas**
- **Site:** https://www.snirh.gov.br/hidroweb/
- **Dados:** Vazão (m³/s), Nível (cm), Precipitação
- **Formato:** CSV, API REST
- **Cobertura:** ~4.500 estações fluviométricas no Brasil

**Principais estações para o projeto:**

| Porto | Rio/Bacia | Estação ANA | Código |
|-------|-----------|-------------|--------|
| Vila do Conde | Amazonas | Óbidos | 15400000 |
| Vila do Conde | Tocantins | Tucuruí | 29280000 |
| Rio Grande | Lagoa dos Patos | São Gonçalo | 87560000 |
| Antonina | Rios locais PR | Antonina (se existir) | Consultar HidroWeb |

**Como acessar:**
```python
# Exemplo com API HidroWeb
import requests

url = "http://telemetriaws1.ana.gov.br/ServiceANA.asmx/DadosHidrometeorologicos"
params = {
    'codEstacao': '15400000',  # Óbidos
    'dataInicio': '01/01/2020',
    'dataFim': '31/12/2026'
}
response = requests.get(url, params=params)
```

---

#### **2. Dados Meteorológicos**

**INMET - Instituto Nacional de Meteorologia**
- **Site:** https://portal.inmet.gov.br/
- **API:** https://apitempo.inmet.gov.br/
- **Dados:** Vento (vel/dir), Pressão, Temperatura, Precipitação
- **Frequência:** Horária (automáticas) ou diária (convencionais)
- **Formato:** JSON, CSV

**Estações próximas aos portos:**

| Porto | Estação INMET | Código |
|-------|---------------|--------|
| Santos | Santos (Ponta da Praia) | A701 |
| Rio Grande | Rio Grande | A802 |
| Paranaguá | Paranaguá | A851 |
| Itaqui | São Luís | A201 |
| Vila do Conde | Belém | A201 |

**Exemplo de uso da API:**
```python
import requests

url = "https://apitempo.inmet.gov.br/estacao/dados/A701"
params = {'dataInicio': '2020-01-01', 'dataFim': '2026-12-31'}
headers = {'Authorization': 'Bearer SEU_TOKEN'}

response = requests.get(url, params=params, headers=headers)
data = response.json()

# Extrair features
vento_sul = [x for x in data if x['VEN_DIR'] > 135 and x['VEN_DIR'] < 225]
```

---

#### **3. Dados Oceanográficos**

**Copernicus Marine Service**
- **Site:** https://marine.copernicus.eu/
- **Dados:** Altura de onda (Hs), Período (Tp), Direção, Correntes
- **Cobertura:** Oceano Atlântico Sul (costa brasileira)
- **Formato:** NetCDF
- **Gratuito:** Sim (requer cadastro)

**SMC-Brasil (Sistema de Modelagem Costeira)**
- **Site:** http://smcbrasil.cnpq.br/
- **Dados:** Ondas, marés, correntes (modelados para costa BR)

---

#### **4. Dados de Precipitação (Bacia Amazônica)**

**CHIRPS - Climate Hazards Group InfraRed Precipitation**
- **Site:** https://www.chc.ucsb.edu/data/chirps
- **Dados:** Precipitação em grade (0.05° resolução)
- **Cobertura:** Global, incluindo Amazônia
- **Formato:** GeoTIFF, NetCDF
- **Uso:** Calcular precipitação acumulada em bacias hidrográficas

---

### 📈 Workflow de Machine Learning Completo

```python
# 1. Carregar previsão astronômica (este projeto)
df_astro = pd.read_csv('viladoconde_extremos_2020_2026.csv')

# 2. Buscar dados fluviais (ANA)
vazao_amazonas = buscar_vazao_ana(estacao='15400000', inicio='2020-01-01', fim='2026-12-31')
vazao_tocantins = buscar_vazao_ana(estacao='29280000', inicio='2020-01-01', fim='2026-12-31')

# 3. Buscar dados meteorológicos (INMET)
meteo = buscar_inmet(estacao='A201', inicio='2020-01-01', fim='2026-12-31')

# 4. Buscar precipitação de bacia (CHIRPS ou ANA)
chuva_amazonia = buscar_precipitacao_bacia(bacia='amazonia', dias=30)

# 5. Criar dataset de features
features = pd.DataFrame({
    'data': df_astro['Data_Hora'],
    'mare_astro': df_astro['Altura_m'],
    'vazao_amazonas': vazao_amazonas,
    'vazao_tocantins': vazao_tocantins,
    'vazao_total': vazao_amazonas + vazao_tocantins,
    'vento_vel': meteo['VEN_VEL'],
    'vento_dir': meteo['VEN_DIR'],
    'pressao': meteo['PRE_INS'],
    'chuva_30d': chuva_amazonia.rolling(30).sum(),
    'mes': pd.to_datetime(df_astro['Data_Hora']).dt.month,
})

# 6. Buscar observações reais (régua/sensor do porto)
observacoes = buscar_observacoes_porto('viladoconde')

# 7. Treinar modelo
from sklearn.ensemble import RandomForestRegressor

X = features[['mare_astro', 'vazao_total', 'vento_vel', 'pressao', 'chuva_30d', 'mes']]
y = observacoes['nivel_real']

modelo = RandomForestRegressor(n_estimators=100)
modelo.fit(X, y)

# 8. Prever com correções
previsao_final = modelo.predict(X)
```

---

**Porto de Paranaguá - Correções Meteorológicas:**
- Feature principal: Previsão astronômica (este projeto)
- Feature de erro: Intensidade e direção do vento
- Target: Altura real observada
- O modelo aprende a corrigir distorções de águas rasas + efeitos meteorológicos

**Porto de Santos:**
- Previsão astronômica como baseline
- Ventos sul e frentes frias como features meteorológicas
- Ressacas podem adicionar +1m ao nível previsto

**Vila do Conde (Barcarena):**
- Feature principal: Previsão astronômica (este projeto)
- **Feature fluvial crítica:** Vazão dos rios Amazonas e Tocantins
- Target: Altura real observada
- Desvios sazonais significativos devido à descarga fluvial
- Distorção de assimetria capturada por componentes M4 (0.054m) e M6 (0.021m)
- Modelo deve aprender que a maré sobe mais rápido do que desce

## Referências

- Marinha do Brasil - Centro de Hidrografia da Marinha (CHM)
- Diretoria de Hidrografia e Navegação (DHN)
- Fichas de Marés: https://www.marinha.mil.br/chm/

## Autor

Scripts baseados nas constantes harmônicas oficiais das fichas de maré da Marinha do Brasil.
