#!/bin/bash

# Script de configuración mejorado para el bot de Telegram en Linux
# Permite configuración opcional del token y administradores

# Colores para la salida
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables de configuración
CONFIG_FILE="Bot-PreguntasFrecuentes/config.py"
CREDENTIALS_FILE="Bot-PreguntasFrecuentes/Datos/Credentials.json"
FAQ_FILE="Bot-PreguntasFrecuentes/Datos/faq.json"
MULTIMEDIA_DIR="Bot-PreguntasFrecuentes/multimedia"

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
        (arch|manjaro|endeavouros)
            sudo pacman -Sy --noconfirm python python-pip python-virtualenv
            ;;
        (debian|ubuntu|pop|linuxmint)
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip python3-venv
            ;;
        (fedora|centos|rhel)
            sudo dnf install -y python3 python3-pip python3-virtualenv
            ;;
        (*)
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
    if [ -d "venv" ]; then
        echo -e "${BLUE}Entorno virtual ya existe. Saltando creación...${NC}"
        return 0
    fi

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

# Función para configurar token (opcional)
configurar_token() {
    if [ -f "$CREDENTIALS_FILE" ]; then
        current_token=$(grep -oP '(?<="token": ")[^"]*' "$CREDENTIALS_FILE")
        if [ -n "$current_token" ]; then
            echo -e "${BLUE}Token actual: ${current_token:0:4}...${current_token: -4}${NC}"
            read -p "¿Desea cambiar el token? (s/n): " cambiar_token
            if [[ ! "$cambiar_token" =~ ^[Ss]$ ]]; then
                return 0
            fi
        fi
    fi

    echo -e "\n${YELLOW}CONFIGURACIÓN DEL TOKEN DE TELEGRAM${NC}"
    echo -e "Puede omitir este paso y configurar el token manualmente después en:"
    echo -e "$CREDENTIALS_FILE"
    read -p "Ingrese el token de su bot de Telegram (deje vacío para omitir): " token
    
    if [ -z "$token" ]; then
        echo -e "${BLUE}Token no configurado. Puede editarlo manualmente más tarde.${NC}"
        return 0
    fi
    
    # Validar token (formato básico)
    if [[ ! $token =~ ^[0-9]+:[a-zA-Z0-9_-]+$ ]]; then
        echo -e "${RED}Token inválido. Debe tener el formato: 123456789:ABCdefghIJKlmNOPQRStuvwxyz${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}Creando archivo de credenciales...${NC}"
    mkdir -p "$(dirname "$CREDENTIALS_FILE")"
    cat > "$CREDENTIALS_FILE" <<EOF
{
    "token": "$token"
}
EOF
    
    echo -e "${GREEN}¡Token configurado correctamente!${NC}"
}

# Función para configurar administradores
configurar_administradores() {
    echo -e "\n${YELLOW}CONFIGURACIÓN DE ADMINISTRADORES${NC}"
    
    # Obtener administradores actuales
    current_admins=$(grep -oP '(?<=ADMIN_IDS = \[)[^\]]*' "$CONFIG_FILE" | tr -d '[:space:]')
    
    if [ -n "$current_admins" ]; then
        echo -e "Administradores actuales: ${BLUE}$current_admins${NC}"
    else
        echo -e "No hay administradores configurados"
    fi
    
    read -p "¿Desea agregar administradores? (s/n): " agregar_admin
    if [[ ! "$agregar_admin" =~ ^[Ss]$ ]]; then
        return 0
    fi

    admins=()
    IFS=',' read -ra admins <<< "$current_admins"
    
    while true; do
        echo -e "\nIngrese los IDs de los administradores (uno por línea)"
        echo -e "Deje vacío para terminar"
        read -p "ID del administrador: " admin_id
        
        if [ -z "$admin_id" ]; then
            break
        fi
        
        # Validar que sea numérico
        if [[ ! "$admin_id" =~ ^[0-9]+$ ]]; then
            echo -e "${RED}Error: El ID debe ser un número${NC}"
            continue
        fi
        
        # Evitar duplicados
        if [[ " ${admins[@]} " =~ " $admin_id " ]]; then
            echo -e "${YELLOW}Este administrador ya está registrado${NC}"
            continue
        fi
        
        admins+=("$admin_id")
        echo -e "${GREEN}Administrador $admin_id agregado${NC}"
    done
    
    if [ ${#admins[@]} -eq 0 ]; then
        echo -e "${BLUE}No se agregaron administradores${NC}"
        return 0
    fi
    
    # Actualizar archivo de configuración
    echo -e "${YELLOW}Actualizando configuración...${NC}"
    admin_list=$(IFS=, ; echo "${admins[*]}")
    sed -i "s/ADMIN_IDS\s*=\s*\[.*\]/ADMIN_IDS = [$admin_list]/" "$CONFIG_FILE"
    
    echo -e "${GREEN}¡Administradores configurados correctamente!${NC}"
    echo -e "Nuevos administradores: ${BLUE}$admin_list${NC}"
}

# Función para verificar estructura de directorios
verificar_estructura() {
    echo -e "${YELLOW}Verificando estructura de directorios...${NC}"
    
    mkdir -p "$MULTIMEDIA_DIR"
    mkdir -p "$(dirname "$FAQ_FILE")"
    
    if [ ! -f "$FAQ_FILE" ]; then
        echo -e "${YELLOW}Creando archivo de preguntas vacío...${NC}"
        echo '{"categorias": []}' > "$FAQ_FILE"
    fi
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
    
    # Verificar estructura de directorios
    verificar_estructura
    
    # Configurar token (opcional)
    configurar_token
    
    # Configurar administradores (opcional)
    configurar_administradores
    
    echo -e "\n${GREEN}¡Configuración completada con éxito!${NC}"
    echo -e "Resumen:"
    echo -e "- Entorno virtual: ${BLUE}venv/${NC}"
    echo -e "- Token: ${BLUE}$([ -f "$CREDENTIALS_FILE" ] && grep -oP '(?<="token": ")[^"]*' "$CREDENTIALS_FILE" || echo "No configurado")${NC}"
    echo -e "- Administradores: ${BLUE}$(grep -oP '(?<=ADMIN_IDS = \[)[^\]]*' "$CONFIG_FILE")${NC}"
    
    echo -e "\nPara iniciar el bot:"
    echo -e "${YELLOW}source venv/bin/activate && python Bot-PreguntasFrecuentes/bot.py${NC}"
    
    deactivate
}

# Ejecutar función principal
main