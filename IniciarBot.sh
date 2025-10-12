#!/bin/bash

# IniciarBot.sh - Script para ejecutar el bot de Telegram en Linux

# Colores para la salida
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para mostrar título centrado
mostrar_titulo() {
    local titulo=" EJECUTANDO BOT DE PREGUNTAS FRECUENTES "
    local ancho=$(tput cols)
    local margen=$(( ($ancho - ${#titulo}) / 2 ))
    printf "\n${YELLOW}%*s%s%*s${NC}\n\n" $((margen)) "" "$titulo" $((margen)) ""
}

# Función principal
main() {
    mostrar_titulo

    # Verificar si el entorno virtual existe
    if [ ! -d "venv" ] || [ ! -f "venv/bin/activate" ]; then
        echo -e "${RED}Error: Entorno virtual no encontrado.${NC}"
        echo -e "Por favor, configure primero el entorno con:"
        echo -e "  python3 -m venv venv"
        echo -e "  source venv/bin/activate"
        echo -e "  pip install -r requerimientos.txt"
        exit 1
    fi

    # Verificar credenciales
    if [ ! -f "Bot-PreguntasFrecuentes/Datos/Credentials.json" ]; then
        echo -e "${RED}Error: Archivo de credenciales no encontrado.${NC}"
        echo -e "Por favor, cree el archivo Credentials.json con formato:"
        echo -e '  {"token": "SU_TOKEN_DE_TELEGRAM"}'
        exit 1
    fi

    # Mostrar instrucciones
    echo -e "${GREEN}Iniciando bot de Telegram...${NC}"
    echo
    echo -e "${YELLOW}[INSTRUCCIONES IMPORTANTES]${NC}"
    echo -e "- Para detener el bot correctamente:"
    echo -e "  1. Presione CTRL+C en esta terminal"
    echo -e "  2. Espere a que el proceso termine"
    echo
    echo -e "${YELLOW}[REGISTRO DEL BOT]${NC}"
    echo -e "----------------------------------------------------"
    echo

    # Activar entorno y ejecutar bot
    source venv/bin/activate && python3 Bot-PreguntasFrecuentes/bot.py

    # Manejar estado de salida
    if [ $? -ne 0 ]; then
        echo -e "\n${RED}El bot se ha detenido debido a un error${NC}"
    else
        echo -e "\n${GREEN}El bot se ha detenido correctamente${NC}"
        sleep 3
    fi
}

# Ejecutar función principal
main