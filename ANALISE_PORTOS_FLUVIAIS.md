# Análise de Portos Puramente Fluviais no Brasil
# IMPORTANTE: Portos fluviais NÃO têm maré astronômica!

## ⚠️ DIFERENÇA CRÍTICA:

### Portos em FOZ (maré astronômica + rio):
- ✅ Vila do Conde (PA) - Foz Amazonas
- ✅ Itajaí (SC) - Foz Itajaí-Açu
- ✅ Suape (PE) - Estuário
- **Método:** Análise harmônica (este projeto)

### Portos FLUVIAIS (apenas rio, SEM maré):
- ❌ Manaus (AM) - Rio Negro/Solimões
- ❌ Porto Velho (RO) - Rio Madeira
- ❌ Corumbá (MS) - Rio Paraguai
- **Método:** Modelo hidrológico (FORA do escopo atual)

---

## PORTOS FLUVIAIS MAIS IMPORTANTES DO BRASIL:

### 🚢 1. MANAUS (AM) - RIO NEGRO/SOLIMÕES ⭐⭐⭐⭐⭐

**Características:**
- **Variação de nível:** 10-15 metros anuais (!)
- **Tipo:** 100% fluvial
- **Amplitude M2:** < 0.01m (praticamente zero)
- **Controle:** Vazão dos rios + precipitação Amazônia
- **Zona Franca:** Grande importância econômica

**Estações ANA:**
```
Código: 14990000 (Manaus - Porto)
Código: 14420000 (Manacapuru - montante)
Variável: Cota (nível do rio)
Dados: Disponível desde 1902!
```

**Por que NÃO usar análise harmônica:**
```python
# Maré astronômica em Manaus:
# M2 (principal componente) ≈ 0.005m = 0.5cm
# Variação fluvial anual = 12m = 1200cm
# Razão: 0.5/1200 = 0.04% → IRRELEVANTE!
```

**Como prever nível em Manaus:**
```python
# Modelo correto: Hidrológico
nivel_manaus = f(
    vazao_solimoes,
    vazao_negro,
    precipitacao_bacia_30d,
    mes_do_ano,  # Sazonalidade
)

# NÃO usar:
# nivel_manaus = NM + Σ(Hi * cos(...))  ← ERRADO para rios!
```

---

### 🚢 2. PORTO VELHO (RO) - RIO MADEIRA ⭐⭐⭐

**Características:**
- **Variação de nível:** 8-12 metros anuais
- **Tipo:** 100% fluvial
- **Controle:** Vazão rio Madeira + usinas (Jirau, Santo Antônio)
- **Importância:** Escoamento de grãos do Centro-Oeste

**Estações ANA:**
```
Código: 15400000 (Porto Velho)
Variável: Cota + Vazão
Período: 1967-presente
```

**Peculiaridade:**
- Afetado por usinas hidrelétricas a montante
- Nível controlado artificialmente em parte

---

### 🚢 3. CORUMBÁ (MS) - RIO PARAGUAI ⭐⭐⭐

**Características:**
- **Variação de nível:** 4-6 metros anuais
- **Tipo:** 100% fluvial (Pantanal)
- **Controle:** Ciclo de cheias do Pantanal
- **Hidrovia:** Paraguai-Paraná

**Estações ANA:**
```
Código: 66260001 (Ladário/Corumbá)
Variável: Cota
Período: Histórico longo
```

**Peculiaridade:**
- Regime do Pantanal (cheias lentas)
- Navegação sazonal

---

### 🚢 4. SANTARÉM (PA) - RIO AMAZONAS ⭐⭐⭐⭐

**Status atual no projeto:**
- ✅ JÁ TEM no Dataset 2 (apenas meteorologia)
- ❌ SEM cálculo de nível (porque não tem maré astronômica)

**Características:**
- **Variação de nível:** 6-8 metros anuais
- **Tipo:** 100% fluvial
- **Amplitude M2:** ~0.02m (2cm - desprezível)
- **Importância:** Exportação de grãos

**Estações ANA:**
```
Código: 17050001 (Santarém)
Variável: Cota + Vazão
Período: Longo histórico
```

**O que você TEM:**
```python
# Dataset 2 contém:
df = pd.read_parquet('dados_historicos_meteorologicos_complementares.parquet')
df_santarem = df[df['station'] == 'Santarem']
# Variáveis: vento, pressão, temperatura
# NÃO tem: wave_height, sea_level (são NaN para portos fluviais)
```

**O que FALTA para Santarém:**
```python
# Adicionar ao dataset:
- cota_rio (nível do rio - ANA)
- vazao_amazonas (ANA Óbidos: 15400000)
- precipitacao_bacia
```

---

### 🚢 5. BARCARENA (PA) - RIO PARÁ

**Status atual no projeto:**
- ✅ JÁ TEM no Dataset 2 (apenas meteorologia)

**Características:**
- **Variação:** Maré + fluvial (HÍBRIDO!)
- **Particularidade:** Está mais próximo da foz que Santarém
- **Pode ter** alguma maré astronômica residual

**Estações ANA:**
```
Código: Verificar estações próximas no Rio Pará
```

---

## COMPARAÇÃO: SISTEMAS DE PREVISÃO NECESSÁRIOS

| Porto | Tipo | Método | Este Projeto | Precisa Adicionar |
|-------|------|--------|--------------|-------------------|
| **Vila do Conde** | Híbrido | Harmônico + Hidrológico | ✅ Harmônico | ⚠️ Hidrológico |
| **Manaus** | Fluvial | Hidrológico puro | ❌ | ✅✅✅ Tudo |
| **Porto Velho** | Fluvial | Hidrológico | ❌ | ✅✅✅ Tudo |
| **Corumbá** | Fluvial | Hidrológico (Pantanal) | ❌ | ✅✅✅ Tudo |
| **Santarém** | Fluvial | Hidrológico | ⚠️ Meteo apenas | ✅✅ Nível/Vazão |
| **Barcarena** | Híbrido? | Verificar | ⚠️ Meteo apenas | ⚠️ Verificar maré |

---

## SE VOCÊ QUISER ADICIONAR PORTOS FLUVIAIS:

### Opção 1: Expandir Escopo do Projeto

**Criar nova categoria: "Previsão de Nível Fluvial"**

```
mares/
├── previsao_mares_*.py          # Marés (astronômico)
├── previsao_nivel_fluvial_*.py  # Rios (hidrológico)
└── README.md
```

**Modelo para portos fluviais:**
```python
def prever_nivel_fluvial(porto, data):
    """
    Modelo hidrológico (NÃO harmônico!)
    """
    # 1. Buscar vazão ANA
    vazao = buscar_ana(estacao_montante)

    # 2. Precipitação na bacia
    precip = buscar_precipitacao_bacia(ultimos_30d)

    # 3. Sazonalidade
    mes = data.month

    # 4. Curva de descarga (rating curve)
    # Relação empírica: Vazão → Nível
    nivel = curva_descarga(vazao, mes)

    return nivel
```

### Opção 2: Apenas Documentar Diferença

**Adicionar seção no README:**

```markdown
## ⚠️ Portos Fluviais vs Portos com Maré

Este projeto foca em **previsão de marés astronômicas**.

**Portos fluviais** (Manaus, Porto Velho, Corumbá) precisam de
modelo hidrológico diferente e estão FORA DO ESCOPO atual.

Para portos fluviais, consulte:
- ANA - Dados de vazão e nível
- Modelos hidrológicos (SMAP, MGB, etc.)
```

---

## MINHA RECOMENDAÇÃO:

### ❌ NÃO adicione portos puramente fluviais agora porque:

1. **Fora do escopo:** Projeto é sobre MARÉS (análise harmônica)
2. **Método diferente:** Precisaria criar todo um sistema hidrológico
3. **Complexidade:** Modelos hidrológicos são outro campo
4. **Mantém foco:** Projeto já está excelente para o que se propõe

### ✅ SE QUISER expandir no futuro:

**Fase 1 (agora):** Complete os portos COM maré
- Suape (PE)
- Itajaí (SC)
- Recife (PE)

**Fase 2 (futuro):** Adicione módulo fluvial separado
- Manaus (AM)
- Porto Velho (RO)
- Santarém (PA) - melhorar dados
- Barcarena (PA) - melhorar dados

### ✅ O QUE FAZER com Santarém e Barcarena:

**Situação atual:**
```python
# Dataset 2 tem apenas meteorologia
df = df[df['station'].isin(['Santarem', 'Barcarena'])]
# Colunas: wind_speed, pressure, temperature
# NÃO tem: wave_height (correto), sea_level (correto)
```

**Opção A - Deixar como está:**
- Dataset meteorológico serve para análise climática
- Usuário pode combinar com dados ANA separadamente

**Opção B - Adicionar dados ANA ao Dataset:**
- Incluir colunas: `cota_rio_ana`, `vazao_rio_ana`
- Documentar que são portos fluviais
- Deixar claro que não têm maré astronômica

---

## CÓDIGO PARA VERIFICAR SE PORTO TEM MARÉ:

```python
def verificar_tem_mare_astronomica(lat, lon):
    """
    Verifica se localização tem maré astronômica significativa

    Regra prática:
    - Oceano/Costa: Sim
    - Foz (< 50km mar): Geralmente sim
    - Rio (> 100km mar): Geralmente não
    - Verificar amplitude M2 > 0.05m
    """
    # Distância aproximada do oceano
    distancia_oceano = calcular_distancia_oceano(lat, lon)

    if distancia_oceano < 10:
        return "Sim - Oceânico"
    elif distancia_oceano < 50:
        return "Provável - Estuário (verificar DHN)"
    elif distancia_oceano < 100:
        return "Talvez - Foz (verificar DHN)"
    else:
        return "Não - Fluvial"

# Exemplos:
print(verificar_tem_mare_astronomica(-3.12, -60.02))  # Manaus → Não
print(verificar_tem_mare_astronomica(-1.38, -48.48))  # Vila Conde → Sim
print(verificar_tem_mare_astronomica(-2.43, -54.71))  # Santarém → Não
```

---

## RESUMO FINAL:

**Portos fluviais importantes:**
1. Manaus (AM) - Mais importante
2. Porto Velho (RO)
3. Corumbá (MS)
4. Santarém (PA) - já tem meteo
5. Barcarena (PA) - já tem meteo

**Todos eles:**
- ❌ NÃO têm maré astronômica significativa
- ❌ NÃO servem para análise harmônica
- ✅ Precisam modelo hidrológico (vazão + precipitação)
- ⚠️ FORA DO ESCOPO atual do projeto

**Recomendação:**
Mantenha o foco em portos COM maré. Se quiser incluir portos fluviais,
crie um módulo separado com metodologia hidrológica diferente.
