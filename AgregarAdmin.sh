#!/bin/bash

# Script mejorado para agregar administradores al bot con interfaz user-friendly
# Versión 2.0 - Interfaz mejorada

# Colores y estilos
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Símbolos Unicode
CHECK="✅"
CROSS="❌"
WARNING="⚠️"
INFO="ℹ️"
ROCKET="🚀"
ROBOT="🤖"
ADMIN="👑"
PLUS="➕"
LIST="📋"
EXIT="🚪"

# Variables
CONFIG_FILE="Bot-PreguntasFrecuentes/config.py"
SCRIPT_VERSION="2.0"

# Función para limpiar pantalla
clear_screen() {
    clear
}

# Función para mostrar línea separadora
show_separator() {
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
}

# Función para mostrar encabezado principal
show_main_header() {
    clear_screen
    echo -e "${PURPLE}${BOLD}"
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║                                                           ║"
    echo "║           ${ROBOT} BOT ONTV - GESTIÓN DE ADMINS ${ADMIN}           ║"
    echo "║                                                           ║"
    echo "║                    Versión ${SCRIPT_VERSION}                         ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo
}

# Función para mostrar el menú principal
show_main_menu() {
    echo -e "${CYAN}${BOLD}¿Qué desea hacer?${NC}"
    echo
    echo -e "${WHITE}1.${NC} ${PLUS} Agregar nuevo administrador"
    echo -e "${WHITE}2.${NC} ${LIST} Ver administradores actuales"
    echo -e "${WHITE}3.${NC} ${INFO} Información del sistema"
    echo -e "${WHITE}4.${NC} ${EXIT} Salir"
    echo
    show_separator
}

# Función para validar que el archivo de configuración existe
validate_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        echo -e "${RED}${CROSS} Error: No se encontró el archivo de configuración.${NC}"
        echo -e "${YELLOW}${WARNING} Asegúrese de ejecutar este script desde el directorio raíz del proyecto.${NC}"
        echo
        echo -e "${CYAN}Ruta esperada: ${WHITE}$CONFIG_FILE${NC}"
        echo
        read -p "Presione Enter para salir..."
        exit 1
    fi
}

# Función para mostrar administradores actuales con formato mejorado
show_current_admins() {
    clear_screen
    show_main_header
    
    echo -e "${CYAN}${BOLD}${LIST} ADMINISTRADORES ACTUALES${NC}"
    show_separator
    echo
    
    # Extraer IDs de administradores
    local admin_line=$(grep "ADMIN_IDS" "$CONFIG_FILE")
    local admin_ids=$(echo "$admin_line" | grep -oP '\[\K[^\]]*')
    
    if [ -z "$admin_ids" ] || [ "$admin_ids" = " " ]; then
        echo -e "${YELLOW}${WARNING} No hay administradores configurados actualmente.${NC}"
        echo
        echo -e "${INFO} ${CYAN}Use la opción 1 para agregar el primer administrador.${NC}"
    else
        echo -e "${GREEN}${CHECK} Administradores encontrados:${NC}"
        echo
        
        # Convertir la cadena de IDs en un array
        IFS=',' read -ra ADDR <<< "$admin_ids"
        local count=1
        
        for id in "${ADDR[@]}"; do
            # Limpiar espacios
            id=$(echo "$id" | xargs)
            if [ ! -z "$id" ]; then
                echo -e "   ${WHITE}${count}.${NC} ${ADMIN} ID: ${YELLOW}${BOLD}$id${NC}"
                ((count++))
            fi
        done
        
        echo
        echo -e "${CYAN}Total de administradores: ${WHITE}$((count-1))${NC}"
    fi
    
    echo
    show_separator
    echo
    read -p "Presione Enter para continuar..."
}

# Función para mostrar información del sistema
show_system_info() {
    clear_screen
    show_main_header
    
    echo -e "${CYAN}${BOLD}${INFO} INFORMACIÓN DEL SISTEMA${NC}"
    show_separator
    echo
    
    echo -e "${WHITE}📁 Archivo de configuración:${NC} $CONFIG_FILE"
    
    if [ -f "$CONFIG_FILE" ]; then
        echo -e "${GREEN}${CHECK} Estado: Encontrado${NC}"
        local file_size=$(stat -f%z "$CONFIG_FILE" 2>/dev/null || stat -c%s "$CONFIG_FILE" 2>/dev/null)
        echo -e "${WHITE}📊 Tamaño:${NC} $file_size bytes"
        local mod_date=$(stat -f%Sm "$CONFIG_FILE" 2>/dev/null || stat -c%y "$CONFIG_FILE" 2>/dev/null)
        echo -e "${WHITE}📅 Última modificación:${NC} $mod_date"
    else
        echo -e "${RED}${CROSS} Estado: No encontrado${NC}"
    fi
    
    echo
    echo -e "${WHITE}🐍 Python:${NC} $(python3 --version 2>/dev/null || echo 'No encontrado')"
    echo -e "${WHITE}💻 Sistema:${NC} $(uname -s) $(uname -r)"
    echo -e "${WHITE}👤 Usuario:${NC} $(whoami)"
    echo -e "${WHITE}📂 Directorio actual:${NC} $(pwd)"
    
    echo
    show_separator
    echo
    read -p "Presione Enter para continuar..."
}

# Función para validar ID de administrador con mejor feedback
validate_admin_id() {
    local admin_id=$1
    
    # Verificar que no esté vacío
    if [ -z "$admin_id" ]; then
        echo -e "${RED}${CROSS} Error: El ID no puede estar vacío.${NC}"
        return 1
    fi
    
    # Verificar que sea un número
    if ! [[ "$admin_id" =~ ^[0-9]+$ ]]; then
        echo -e "${RED}${CROSS} Error: El ID debe ser un número válido.${NC}"
        echo -e "${YELLOW}${INFO} Ejemplo de ID válido: 123456789${NC}"
        return 1
    fi
    
    # Verificar longitud mínima (IDs de Telegram suelen tener al menos 8 dígitos)
    if [ ${#admin_id} -lt 8 ]; then
        echo -e "${YELLOW}${WARNING} Advertencia: El ID parece muy corto para ser un ID de Telegram.${NC}"
        echo -e "${CYAN}${INFO} Los IDs de Telegram suelen tener 9-10 dígitos.${NC}"
        echo
        read -p "¿Está seguro de que este ID es correcto? (s/n): " confirm
        if [[ ! "$confirm" =~ ^[Ss]$ ]]; then
            return 1
        fi
    fi
    
    # Verificar que no esté ya registrado
    if grep -q "$admin_id" "$CONFIG_FILE"; then
        echo -e "${YELLOW}${WARNING} El administrador con ID $admin_id ya está registrado.${NC}"
        return 1
    fi
    
    return 0
}

# Función para agregar administrador con interfaz mejorada
add_admin_interface() {
    clear_screen
    show_main_header
    
    echo -e "${CYAN}${BOLD}${PLUS} AGREGAR NUEVO ADMINISTRADOR${NC}"
    show_separator
    echo
    
    echo -e "${INFO} ${CYAN}Para obtener su ID de Telegram:${NC}"
    echo -e "   ${WHITE}1.${NC} Abra Telegram y busque el bot @userinfobot"
    echo -e "   ${WHITE}2.${NC} Envíe el comando /start"
    echo -e "   ${WHITE}3.${NC} El bot le mostrará su ID numérico"
    echo
    show_separator
    echo
    
    while true; do
        echo -e "${CYAN}${BOLD}Ingrese el ID del nuevo administrador:${NC}"
        echo -e "${YELLOW}(o escriba 'menu' para volver al menú principal)${NC}"
        echo
        read -p "🆔 ID: " admin_id
        
        if [ "$admin_id" = "menu" ] || [ "$admin_id" = "salir" ] || [ "$admin_id" = "exit" ]; then
            return 0
        fi
        
        echo
        if validate_admin_id "$admin_id"; then
            echo -e "${GREEN}${CHECK} ID válido: $admin_id${NC}"
            echo
            
            # Confirmación
            echo -e "${YELLOW}${WARNING} ¿Está seguro de que desea agregar este administrador?${NC}"
            echo -e "${WHITE}ID a agregar: ${BOLD}$admin_id${NC}"
            echo
            read -p "Confirmar (s/n): " confirm
            
            if [[ "$confirm" =~ ^[Ss]$ ]]; then
                if add_admin "$admin_id"; then
                    echo
                    echo -e "${GREEN}${ROCKET} ¡Proceso completado exitosamente!${NC}"
                    echo
                    read -p "¿Desea agregar otro administrador? (s/n): " continue_adding
                    if [[ ! "$continue_adding" =~ ^[Ss]$ ]]; then
                        return 0
                    fi
                    echo
                    clear_screen
                    show_main_header
                    echo -e "${CYAN}${BOLD}${PLUS} AGREGAR OTRO ADMINISTRADOR${NC}"
                    show_separator
                    echo
                else
                    echo
                    read -p "Presione Enter para intentar nuevamente..."
                fi
            else
                echo -e "${YELLOW}Operación cancelada.${NC}"
                echo
            fi
        else
            echo
            echo -e "${CYAN}Por favor, intente nuevamente.${NC}"
        fi
        echo
    done
}

# Función para agregar administrador (lógica mejorada)
add_admin() {
    local admin_id=$1
    
    echo -e "${CYAN}Procesando...${NC}"
    
    # Crear script temporal de Python con mejor manejo de errores
    cat > temp_update_admin.py << EOF
import re
import sys
import os

def update_admin_config(admin_id):
    config_file = '$CONFIG_FILE'
    
    try:
        # Verificar que el archivo existe
        if not os.path.exists(config_file):
            print('Error: Archivo de configuración no encontrado')
            return False
            
        # Leer el archivo
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar la línea ADMIN_IDS
        pattern = r'ADMIN_IDS\\s*=\\s*\\[(.*?)\\]'
        match = re.search(pattern, content)
        
        if match:
            current_ids = match.group(1).strip()
            
            # Verificar si ya existe el ID
            if admin_id in current_ids:
                print('Error: El administrador ya existe')
                return False
                
            if current_ids:
                new_ids = current_ids + ', ' + admin_id
            else:
                new_ids = admin_id
            
            new_line = f'ADMIN_IDS = [{new_ids}]'
            new_content = re.sub(pattern, new_line, content)
            
            # Crear backup
            backup_file = config_file + '.backup'
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Escribir el nuevo contenido
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print('SUCCESS')
            return True
        else:
            print('Error: No se pudo encontrar la línea ADMIN_IDS')
            return False
            
    except Exception as e:
        print(f'Error: {e}')
        return False

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Error: ID de administrador requerido')
        sys.exit(1)
    
    admin_id = sys.argv[1]
    if update_admin_config(admin_id):
        sys.exit(0)
    else:
        sys.exit(1)
EOF
    
    # Ejecutar el script de Python
    local result=$(python3 temp_update_admin.py "$admin_id" 2>&1)
    
    if [ $? -eq 0 ] && [[ "$result" == *"SUCCESS"* ]]; then
        echo -e "${GREEN}${CHECK} ¡Administrador $admin_id agregado correctamente!${NC}"
        echo
        
        echo -e "${CYAN}${LIST} Configuración actualizada:${NC}"
        grep "ADMIN_IDS" "$CONFIG_FILE" | sed 's/^/   /'
        echo
        
        echo -e "${GREEN}${ROBOT} El administrador ya puede usar los comandos del bot.${NC}"
        
        # Limpiar archivos temporales
        rm -f temp_update_admin.py
        return 0
    else
        echo -e "${RED}${CROSS} Error al agregar el administrador.${NC}"
        echo -e "${YELLOW}Detalles: $result${NC}"
        
        # Limpiar archivos temporales
        rm -f temp_update_admin.py
        return 1
    fi
}

# Función para limpiar archivos temporales
cleanup() {
    rm -f temp_update_admin.py
}

# Función principal con menú interactivo
main() {
    # Configurar limpieza al salir
    trap cleanup EXIT
    
    # Validar configuración inicial
    validate_config
    
    while true; do
        show_main_header
        show_main_menu
        
        read -p "Seleccione una opción (1-4): " option
        
        case $option in
            1)
                add_admin_interface
                ;;
            2)
                show_current_admins
                ;;
            3)
                show_system_info
                ;;
            4)
                clear_screen
                echo -e "${GREEN}${CHECK} ¡Gracias por usar el gestor de administradores!${NC}"
                echo -e "${CYAN}${ROBOT} Bot ONTV - Hasta la vista${NC}"
                echo
                exit 0
                ;;
            *)
                echo
                echo -e "${RED}${CROSS} Opción inválida. Por favor seleccione 1, 2, 3 o 4.${NC}"
                echo
                read -p "Presione Enter para continuar..."
                ;;
        esac
    done
}

# Verificar dependencias
check_dependencies() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}${CROSS} Error: Python3 no está instalado.${NC}"
        echo -e "${YELLOW}${INFO} Por favor instale Python3 para continuar.${NC}"
        exit 1
    fi
}

# Ejecutar función principal
echo -e "${CYAN}Iniciando gestor de administradores...${NC}"
check_dependencies
main "$@"