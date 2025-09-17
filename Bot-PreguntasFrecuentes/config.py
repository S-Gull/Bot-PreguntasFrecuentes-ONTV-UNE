import os
import json

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MULTIMEDIA_DIR = os.path.join(
    BASE_DIR, "Bot-PreguntasFrecuentes", "multimedia")
FAQ_FILE = os.path.join(
    BASE_DIR, "Bot-PreguntasFrecuentes", "Datos", "faq.json")
CREDENTIALS_FILE = os.path.join(
    BASE_DIR, "Bot-PreguntasFrecuentes", "Datos", "Credentials.json")

# Configuración de administradores
# ==============================================
# (Agrega los IDs de los administradores como números enteros)
# ==============================================
ADMIN_IDS = [1851963523, 1181943029]  # Reemplaza con tus IDs reales

# Variables globales que se inicializarán después
bot_instance = None
preguntas = {"categorias": []}

# Crear directorios si no existen
os.makedirs(MULTIMEDIA_DIR, exist_ok=True)
os.makedirs(os.path.dirname(FAQ_FILE), exist_ok=True)
os.makedirs(os.path.dirname(CREDENTIALS_FILE), exist_ok=True)


def save_questions():
    """Guarda las preguntas en el archivo JSON"""
    try:
        with open(FAQ_FILE, 'w', encoding='utf-8') as f:
            json.dump(preguntas, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error al guardar preguntas: {str(e)}")
        return False


def load_questions():
    """Carga las preguntas desde el archivo JSON"""
    global preguntas
    try:
        if os.path.exists(FAQ_FILE):
            with open(FAQ_FILE, 'r', encoding='utf-8') as f:
                preguntas = json.load(f)
        else:
            preguntas = {"categorias": []}
            save_questions()
    except json.JSONDecodeError:
        print("Error: Archivo de preguntas corrupto. Se creará uno nuevo.")
        preguntas = {"categorias": []}
        save_questions()
    except Exception as e:
        print(f"Error al cargar preguntas: {str(e)}")
        preguntas = {"categorias": []}


def get_bot_token():
    """Obtiene el token del bot desde el archivo de credenciales"""
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            credentials = json.load(f)
        return credentials.get("token", "")
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: No se pudo leer el archivo de credenciales")
        return ""


def es_admin(user_id):
    """Verifica si un usuario es administrador"""
    return user_id in ADMIN_IDS


def initialize_config():
    """Inicializa la configuración del bot"""
    load_questions()

    # Verificar que exista el archivo de credenciales
    if not os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'w') as f:
            json.dump({"token": "TU_TOKEN_AQUI"}, f)
        print(f"Archivo de credenciales creado en {CREDENTIALS_FILE}")
        print("Por favor configura tu token de bot antes de continuar")
        exit(1)

    # Verificar que el token esté configurado
    token = get_bot_token()
    if not token or token == "TU_TOKEN_AQUI":
        print("Error: Token no configurado. Edita el archivo Credentials.json")
        exit(1)


# Inicializar configuración al importar
initialize_config()
