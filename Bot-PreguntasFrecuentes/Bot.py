import json
import os
from telebot import TeleBot, types

# Configuración de directorios
MULTIMEDIA_DIR = "Bot-PreguntasFrecuentes/multimedia/"
FAQ_FILE = "Bot-PreguntasFrecuentes/Datos/faq.json"

# Crear directorios si no existen
os.makedirs(MULTIMEDIA_DIR, exist_ok=True)
os.makedirs(os.path.dirname(FAQ_FILE), exist_ok=True)

# Cargar preguntas desde JSON
def cargar_preguntas():
    try:
        with open(FAQ_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Si el archivo no existe o está vacío, crear estructura básica
        estructura_inicial = {"categorias": []}
        with open(FAQ_FILE, 'w', encoding='utf-8') as f:
            json.dump(estructura_inicial, f, indent=2)
        return estructura_inicial

# Inicializar bot
with open('Bot-PreguntasFrecuentes/Datos/Credentials.json') as f:
    credenciales = json.load(f)

bot = TeleBot(credenciales["token"])
preguntas = cargar_preguntas()

# --------------------------
# COMANDOS PARA USUARIOS
# --------------------------

@bot.message_handler(commands=['start', 'help', 'preguntas'])
def start(message):
    """Muestra las categorías disponibles"""
    # Mensaje de bienvenida personalizado
    welcome_msg = (
        "🌟 <b>¡Bienvenido al bot de la ONTV (Organización Nacional de Trasplantes de Venezuela)!</b> 🌟\n\n"
        "Aquí encontrarás información importante sobre donación y trasplantes.\n\n"
        "Selecciona una categoría:"
    )
    
    markup = types.InlineKeyboardMarkup()
    
    if not preguntas['categorias']:
        bot.send_message(
            message.chat.id, 
            "ℹ️ No hay preguntas frecuentes disponibles todavía.\n\n"
            "Por favor, contacta al administrador para agregar contenido."
        )
        return
    
    for categoria in preguntas['categorias']:
        markup.add(
            types.InlineKeyboardButton(
                categoria['nombre'], 
                callback_data=f"categoria_{preguntas['categorias'].index(categoria)}"
            )
        )
    
    bot.send_message(
        message.chat.id, 
        welcome_msg, 
        reply_markup=markup,
        parse_mode='HTML'
    )
    
@bot.callback_query_handler(func=lambda call: call.data.startswith('categoria_'))
def mostrar_preguntas(call):
    """Muestra las preguntas de una categoría específica"""
    categoria_id = int(call.data.split('_')[1])
    categoria = preguntas['categorias'][categoria_id]
    
    markup = types.InlineKeyboardMarkup()
    
    for pregunta in categoria['preguntas']:
        markup.add(
            types.InlineKeyboardButton(
                pregunta['pregunta'], 
                callback_data=f"pregunta_{categoria_id}_{categoria['preguntas'].index(pregunta)}"
            )
        )
    
    markup.add(types.InlineKeyboardButton("🔙 Volver al inicio", callback_data="volver"))
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"❓ <b>{categoria['nombre']}</b>\n\nSelecciona una pregunta:",
        reply_markup=markup,
        parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('pregunta_'))
def mostrar_respuesta(call):
    """Muestra la respuesta a una pregunta específica"""
    _, categoria_id, pregunta_id = call.data.split('_')
    categoria_id = int(categoria_id)
    pregunta_id = int(pregunta_id)
    
    pregunta = preguntas['categorias'][categoria_id]['preguntas'][pregunta_id]
    
    # Si hay multimedia
    if pregunta.get('multimedia'):
        extension = pregunta['multimedia'].split('.')[-1].lower()
        media_path = os.path.join(MULTIMEDIA_DIR, pregunta['multimedia'])
        
        try:
            with open(media_path, 'rb') as media:
                if extension in ['jpg', 'jpeg', 'png']:
                    bot.send_photo(call.message.chat.id, media, caption=pregunta['respuesta'])
                elif extension in ['mp4', 'gif', 'mov']:
                    bot.send_video(call.message.chat.id, media, caption=pregunta['respuesta'])
                elif extension in ['mp3', 'ogg', 'wav']:
                    bot.send_audio(call.message.chat.id, media, caption=pregunta['respuesta'])
                elif extension in ['pdf', 'doc', 'docx']:
                    bot.send_document(call.message.chat.id, media, caption=pregunta['respuesta'])
                else:
                    bot.send_document(call.message.chat.id, media, caption=pregunta['respuesta'])
        except FileNotFoundError:
            bot.send_message(
                call.message.chat.id, 
                f"⚠️ <b>Multimedia no encontrada</b>\n\n{pregunta['respuesta']}", 
                parse_mode='HTML'
            )
    else:
        bot.send_message(call.message.chat.id, pregunta['respuesta'])
    
    # Mostrar botón para volver
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        "🔙 Volver a preguntas", 
        callback_data=f"categoria_{categoria_id}"
    ))
    
    bot.send_message(
        call.message.chat.id, 
        "¿Necesitas algo más?", 
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "volver")
def volver(call):
    """Maneja el botón de volver al inicio"""
    start(call.message)

@bot.message_handler(func=lambda message: True)
def manejar_otros_mensajes(message):
    """Responde a cualquier otro mensaje no reconocido"""
    bot.reply_to(
        message, 
        "ℹ️ Usa el comando /start o /preguntas para ver las preguntas frecuentes.\n\n"
        "Si necesitas ayuda adicional, por favor contacta al soporte técnico."
    )

# --------------------------
# INICIAR EL BOT
# --------------------------

if __name__ == '__main__':
    print("🤖 Bot de Preguntas Frecuentes iniciado...")
    print(f"📂 Directorio multimedia: {MULTIMEDIA_DIR}")
    print(f"📄 Archivo de preguntas: {FAQ_FILE}")
    bot.polling(none_stop=True)