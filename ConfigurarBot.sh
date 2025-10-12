#!/bin/bash

# ==========================================================
# Configurador del Bot - BOT ONTV
# Versión 3.0 (adaptado desde ConfigurarBot.bat)
# Compatible con Linux / macOS
# ==========================================================

# --- Colores y estilos ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
BOLD='\033[1m'
NC='\033[0m'

# --- Emojis ---
CHECK="✅"
CROSS="❌"
WARNING="⚠️"
INFO="ℹ️"
ROCKET="🚀"
ROBOT="🤖"
ADMIN="👑"
TOKEN="🔑"
EXIT="🚪"
LIST="📋"
PLUS="➕"

# --- Variables ---
CONFIG_FILE="Bot-PreguntasFrecuentes/config.py"
CREDENTIALS_FILE="Bot-PreguntasFrecuentes/Datos/Credentials.json"
SCRIPT_VERSION="3.0"

# --- Funciones auxiliares ---
clear_screen() { clear; }

show_separator() {
  echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
}

show_main_header() {
  clear_screen
  echo -e "${PURPLE}${BOLD}"
  echo "╔═══════════════════════════════════════════════════════════╗"
  echo "║                                                           ║"
  echo "║            ${ROBOT} CONFIGURADOR DEL BOT ONTV ${ROBOT}              ║"
  echo "║                                                           ║"
  echo "║                     Versión ${SCRIPT_VERSION}                        ║"
  echo "╚═══════════════════════════════════════════════════════════╝"
  echo -e "${NC}"
  echo
}

# --- Validar dependencias ---
check_dependencies() {
  if ! command -v python3 &>/dev/null; then
    echo -e "${RED}${CROSS} Python3 no está instalado.${NC}"
    echo -e "${YELLOW}${INFO} Instale Python3 para continuar.${NC}"
    exit 1
  fi
}

# --- Validar archivos ---
validate_config() {
  if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}${CROSS} Error: No se encontró ${CONFIG_FILE}${NC}"
    echo -e "${YELLOW}${WARNING} Ejecute este script desde la raíz del proyecto.${NC}"
    exit 1
  fi
}

# ==========================================================
# 🪙 CONFIGURAR TOKEN DEL BOT
# ==========================================================
configure_token() {
  clear_screen
  show_main_header
  echo -e "${CYAN}${BOLD}${TOKEN} CONFIGURAR TOKEN DEL BOT${NC}"
  show_separator
  echo

  local current_token="NO CONFIGURADO"
  if [ -f "$CREDENTIALS_FILE" ]; then
    local token_value
    token_value=$(grep -oP '(?<="token": ")[^"]+' "$CREDENTIALS_FILE" 2>/dev/null)
    if [ -n "$token_value" ]; then
      current_token="${token_value:0:4}...${token_value: -4}"
    fi
  fi

  echo -e "${WHITE}Token actual:${NC} ${YELLOW}$current_token${NC}"
  echo
  echo -e "${INFO} Para obtener un nuevo token:"
  echo "   1. Abra Telegram y busque @BotFather"
  echo "   2. Envíe el comando /newbot"
  echo "   3. Copie el token que le proporcione"
  echo
  read -p "¿Desea configurar un nuevo token? (s/n): " choice

  [[ ! "$choice" =~ ^[Ss]$ ]] && return

  echo
  read -p "Ingrese el nuevo token (o escriba 'cancelar'): " new_token
  if [ "$new_token" = "cancelar" ] || [ -z "$new_token" ]; then
    echo -e "${YELLOW}Operación cancelada.${NC}"
    sleep 1
    return
  fi

  if [[ ! "$new_token" =~ : ]]; then
    echo -e "${RED}${CROSS} Formato inválido. El token debe contener ':' (ej: 12345:ABC...)${NC}"
    sleep 2
    return
  fi

  echo
  echo -e "${YELLOW}${WARNING} Nuevo token: ${WHITE}${new_token}${NC}"
  read -p "¿Confirmar actualización? (s/n): " confirm
  [[ ! "$confirm" =~ ^[Ss]$ ]] && echo -e "${YELLOW}Cancelado.${NC}" && sleep 1 && return

  mkdir -p "$(dirname "$CREDENTIALS_FILE")"
  echo "{\"token\": \"$new_token\"}" >"$CREDENTIALS_FILE"

  if [ -f "$CREDENTIALS_FILE" ]; then
    echo -e "${GREEN}${CHECK} Token actualizado correctamente.${NC}"
  else
    echo -e "${RED}${CROSS} No se pudo guardar el token.${NC}"
  fi
  echo
  read -p "Presione Enter para volver al menú..."
}

# ==========================================================
# 👑 AGREGAR ADMINISTRADOR
# ==========================================================
add_admin_interface() {
  clear_screen
  show_main_header
  echo -e "${CYAN}${BOLD}${PLUS} AGREGAR NUEVO ADMINISTRADOR${NC}"
  show_separator
  echo
  echo -e "${INFO} Para obtener su ID de Telegram:${NC}"
  echo "   1. Abra Telegram y busque @userinfobot"
  echo "   2. Envíe /start para ver su ID numérico"
  echo

  while true; do
    read -p "Ingrese el ID del nuevo administrador (o 'menu' para volver): " admin_id
    [[ "$admin_id" = "menu" ]] && return
    if [[ ! "$admin_id" =~ ^[0-9]+$ ]]; then
      echo -e "${RED}${CROSS} El ID debe ser numérico.${NC}"
      continue
    fi

    if grep -q "$admin_id" "$CONFIG_FILE"; then
      echo -e "${YELLOW}${WARNING} El administrador ya está registrado.${NC}"
      continue
    fi

    echo
    read -p "¿Confirmar agregar ID $admin_id? (s/n): " confirm
    [[ ! "$confirm" =~ ^[Ss]$ ]] && continue

    # Python helper
    cat >temp_add_admin.py <<EOF
import re, sys
cfg = "$CONFIG_FILE"
aid = "$admin_id"
with open(cfg, "r", encoding="utf-8") as f: txt = f.read()
m = re.search(r'ADMIN_IDS\\s*=\\s*\\[(.*?)\\]', txt)
if not m:
    print("Error: No se encontró ADMIN_IDS")
    sys.exit(1)
ids = m.group(1).strip()
new_ids = ids + (", " if ids else "") + aid
new_txt = re.sub(r'ADMIN_IDS\\s*=\\s*\\[.*?\\]', f'ADMIN_IDS = [{new_ids}]', txt)
with open(cfg, "w", encoding="utf-8") as f: f.write(new_txt)
print("SUCCESS")
EOF

    result=$(python3 temp_add_admin.py 2>&1)
    if [[ "$result" == *"SUCCESS"* ]]; then
      echo -e "${GREEN}${CHECK} Administrador agregado correctamente.${NC}"
    else
      echo -e "${RED}${CROSS} Error:${NC} $result"
    fi
    rm -f temp_add_admin.py
    read -p "¿Agregar otro administrador? (s/n): " again
    [[ "$again" =~ ^[Ss]$ ]] || break
  done
}

# ==========================================================
# 📋 INFORMACIÓN DEL SISTEMA
# ==========================================================
show_system_info() {
  clear_screen
  show_main_header
  echo -e "${CYAN}${BOLD}${INFO} INFORMACIÓN DEL SISTEMA${NC}"
  show_separator
  echo
  echo -e "${WHITE}Configuración:${NC} $CONFIG_FILE"
  [ -f "$CONFIG_FILE" ] && grep "ADMIN_IDS" "$CONFIG_FILE"
  echo
  echo -e "${WHITE}Credenciales:${NC} $CREDENTIALS_FILE"
  [ -f "$CREDENTIALS_FILE" ] && grep "token" "$CREDENTIALS_FILE"
  echo
  echo -e "${WHITE}Python:${NC} $(python3 --version 2>/dev/null || echo 'No encontrado')"
  echo -e "${WHITE}Sistema:${NC} $(uname -s) $(uname -r)"
  echo -e "${WHITE}Usuario:${NC} $(whoami)"
  echo -e "${WHITE}Directorio:${NC} $(pwd)"
  echo
  show_separator
  read -p "Presione Enter para continuar..."
}

# ==========================================================
# 🧭 MENÚ PRINCIPAL
# ==========================================================
main_menu() {
  while true; do
    show_main_header
    echo -e "${CYAN}${BOLD}¿Qué desea configurar?${NC}"
    echo
    echo -e "1. ${PLUS} Agregar Administradores"
    echo -e "2. ${TOKEN} Configurar Token del Bot"
    echo -e "3. ${LIST} Ver Información del Sistema"
    echo -e "4. ${EXIT} Salir"
    echo
    show_separator
    read -p "Seleccione una opción (1-4): " opt
    case $opt in
      1) add_admin_interface ;;
      2) configure_token ;;
      3) show_system_info ;;
      4)
        clear_screen
        echo -e "${GREEN}${CHECK} ¡Gracias por usar el configurador del bot!${NC}"
        echo -e "${CYAN}${ROBOT} Bot ONTV - Hasta la vista${NC}"
        exit 0
        ;;
      *) echo -e "${RED}${CROSS} Opción inválida.${NC}"; sleep 1 ;;
    esac
  done
}

# ==========================================================
# EJECUCIÓN
# ==========================================================
check_dependencies
validate_config
main_menu
