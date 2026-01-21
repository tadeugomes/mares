#!/bin/bash
# Script para executar previsão de marés de portos brasileiros

echo "========================================="
echo "Previsão de Marés - Portos Brasileiros"
echo "========================================="
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Erro: Python 3 não está instalado."
    exit 1
fi

# Verificar se as dependências estão instaladas
echo "Verificando dependências..."
python3 -c "import pandas, numpy" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "Instalando dependências..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Erro ao instalar dependências. Execute manualmente:"
        echo "  pip install -r requirements.txt"
        exit 1
    fi
    echo "Dependências instaladas com sucesso!"
fi

echo ""
echo "Escolha o porto para calcular previsões:"
echo ""
echo "1) Porto de Itaqui (MA) - Macromaré"
echo "2) Terminal Gás Sul (SC) - Micro-maré"
echo "3) Porto de Santos (SP) - Micro-maré"
echo "4) Todos"
echo "0) Cancelar"
echo ""
read -p "Opção [1-4]: " opcao

case $opcao in
    1)
        echo ""
        echo "========================================="
        echo "Calculando: Porto de Itaqui (MA)"
        echo "========================================="
        echo ""
        python3 previsao_mares_itaqui.py
        ;;
    2)
        echo ""
        echo "========================================="
        echo "Calculando: Terminal Gás Sul (SC)"
        echo "========================================="
        echo ""
        python3 previsao_mares_tgs.py
        ;;
    3)
        echo ""
        echo "========================================="
        echo "Calculando: Porto de Santos (SP)"
        echo "========================================="
        echo ""
        python3 previsao_mares_santos.py
        ;;
    4)
        echo ""
        echo "========================================="
        echo "Calculando: Porto de Itaqui (MA)"
        echo "========================================="
        echo ""
        python3 previsao_mares_itaqui.py

        if [ $? -eq 0 ]; then
            echo ""
            echo "========================================="
            echo "Calculando: Terminal Gás Sul (SC)"
            echo "========================================="
            echo ""
            python3 previsao_mares_tgs.py
        fi

        if [ $? -eq 0 ]; then
            echo ""
            echo "========================================="
            echo "Calculando: Porto de Santos (SP)"
            echo "========================================="
            echo ""
            python3 previsao_mares_santos.py
        fi
        ;;
    0)
        echo "Operação cancelada."
        exit 0
        ;;
    *)
        echo "Opção inválida!"
        exit 1
        ;;
esac

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================="
    echo "Processamento concluído com sucesso!"
    echo "========================================="
else
    echo ""
    echo "Erro ao executar o script."
    exit 1
fi
