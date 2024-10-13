#!/bin/bash

# Instalar dependencias de Python
pip install -r requirements.txt

# Instalar GoSpider
GO111MODULE=on go install github.com/jaeles-project/gospider@latest

# Mover GoSpider a /usr/bin para fácil acceso
sudo cp ~/go/bin/gospider /usr/bin

# Instrucciones para instalar Geckodriver
echo "Asegúrate Manito de descargar e instalar la versión compatible de Geckodriver con tu versión de Firefox desde:"
echo "https://github.com/mozilla/geckodriver/releases"

# Ejecutar el script principal
echo "Mano para ejecutar el script, usa el siguiente comando:"
echo "python3 pruebadieciseis.py"
