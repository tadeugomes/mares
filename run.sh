#!/bin/bash
# Script para executar a previsão de marés do Porto de Itaqui

echo "=================================="
echo "Previsão de Marés - Porto de Itaqui"
echo "=================================="
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Erro: Python 3 não está instalado."
    exit 1
fi

# Verificar se as dependências estão instaladas
echo "Verificando dependências..."
python3 -c "import pandas, pytides" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "Instalando dependências..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Erro ao instalar dependências. Execute manualmente:"
        echo "  pip install -r requirements.txt"
        exit 1
    fi
fi

# Executar o script
echo ""
echo "Executando cálculo de marés..."
echo ""
python3 previsao_mares_itaqui.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================="
    echo "Processamento concluído com sucesso!"
    echo "=================================="
else
    echo ""
    echo "Erro ao executar o script."
    exit 1
fi
