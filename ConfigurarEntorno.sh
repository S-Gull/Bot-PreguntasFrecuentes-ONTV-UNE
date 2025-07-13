#!/bin/bash

# ConfigurarEntorno.sh - Script de configuración para el bot de Telegram en Linux

# Colores para la salida
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para detectar la distribución
detectar_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo $ID
    else
        echo "unknown"
    fi
}

# Función para instalar dependencias
instalar_dependencias() {
    local distro=$1
    
    echo -e "${YELLOW}Instalando dependencias para ${distro}...${NC}"
    
    case $distro in
        arch|manjaro|endeavouros)
            sudo pacman -Sy --noconfirm python python-pip python-virtualenv
            ;;
        debian|ubuntu|pop|linuxmint)
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip python3-venv
            ;;
        fedora|centos|rhel)
            sudo dnf install -y python3 python3-pip python3-virtualenv
            ;;
        *)
            echo -e "${RED}Distribución no soportada. Instala manualmente:${NC}"
            echo "- python3"
            echo "- python3-pip"
            echo "- python3-venv"
            exit 1
            ;;
    esac
    
    # Verificar instalación
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Error: Python3 no se instaló correctamente${NC}"
        exit 1
    fi
}

# Función para configurar entorno virtual
configurar_entorno() {
    echo -e "${YELLOW}Creando entorno virtual...${NC}"
    python3 -m venv venv || {
        echo -e "${RED}Error al crear el entorno virtual${NC}"
        exit 1
    }
    
    echo -e "${YELLOW}Activando entorno virtual...${NC}"
    source venv/bin/activate || {
        echo -e "${RED}Error al activar el entorno virtual${NC}"
        exit 1
    }
    
    echo -e "${YELLOW}Instalando requerimientos...${NC}"
    pip install -r requerimientos.txt || {
        echo -e "${RED}Error al instalar los requerimientos${NC}"
        exit 1
    }
}

# Función para configurar token
configurar_token() {
    echo -e "\n${YELLOW}CONFIGURACIÓN DEL TOKEN DE TELEGRAM${NC}"
    read -p "Ingrese el token de su bot de Telegram: " token
    
    # Validar token (formato básico)
    if [[ ! $token =~ ^[0-9]+:[a-zA-Z0-9_-]+$ ]]; then
        echo -e "${RED}Token inválido. Debe tener el formato: 123456789:ABCdefghIJKlmNOPQRStuvwxyz${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}Creando archivo de credenciales...${NC}"
    mkdir -p "Bot-PreguntasFrecuentes/Datos"
    cat > "Bot-PreguntasFrecuentes/Datos/Credentials.json" <<EOF
{
    "token": "$token"
}
EOF
    
    # Crear estructura de directorios
    mkdir -p "Bot-PreguntasFrecuentes/img"
    touch "Bot-PreguntasFrecuentes/Datos/faq.json"
    
    echo -e "${GREEN}¡Token configurado correctamente!${NC}"
}

# Función principal
main() {
    echo -e "${GREEN}\n=== CONFIGURACIÓN DEL BOT DE TELEGRAM ===${NC}"
    
    # Detectar distribución
    distro=$(detectar_distro)
    echo -e "Detectada distribución: ${YELLOW}$distro${NC}"
    
    # Instalar dependencias
    instalar_dependencias $distro
    
    # Configurar entorno virtual
    configurar_entorno
    
    # Configurar token
    configurar_token
    
    echo -e "\n${GREEN}¡Configuración completada con éxito!${NC}"
    echo -e "Para iniciar el bot, ejecuta:"
    echo -e "${YELLOW}source venv/bin/activate && python Bot-PreguntasFrecuentes/bot.py${NC}"
    
    deactivate
}

# Ejecutar función principal
main