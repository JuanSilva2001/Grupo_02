#!/bin/bash

# Verifica se o ambiente virtual já existe
if [ ! -d "venv" ]; then
    # Cria o ambiente virtual
    python3 -m venv venv
fi

# Ativa o ambiente virtual
source venv/bin/activate

# Instala as dependências a partir do requirements.txt
pip install -r requirements.txt

echo "Ambiente virtual criado e dependências instaladas."
