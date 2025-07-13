import json
import os
from telebot import TeleBot, types

# Configuración inicial
ADMIN_IDS = [123456789]  # Reemplaza con tu ID de Telegram
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

@bot.message_handler(commands=['start', 'help'])
def start(message):
    """Muestra las categorías disponibles"""
    markup = types.InlineKeyboardMarkup()
    
    if not preguntas['categorias']:
        bot.send_message(message.chat.id, "ℹ️ No hay preguntas frecuentes disponibles todavía.")
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
        "📚 <b>Preguntas Frecuentes</b>\n\nSelecciona una categoría:", 
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
    
    markup.add(types.InlineKeyboardButton("🔙 Volver", callback_data="volver"))
    
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

# --------------------------
# COMANDOS PARA ADMINISTRADORES
# --------------------------

@bot.message_handler(commands=['agregar'])
def agregar_pregunta(message):
    """Inicia el proceso para agregar una nueva pregunta"""
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ No tienes permisos para este comando.")
        return
    
    instrucciones = """
📝 <b>Agregar nueva pregunta</b>

Envía los datos en este formato:

<b>Categoría:</b> Nombre de categoría (existente o nueva)
<b>Pregunta:</b> ¿Tu pregunta aquí?
<b>Respuesta:</b> La respuesta completa
<b>Multimedia:</b> nombre_archivo.ext (opcional)

<u>Ejemplo:</u>
Categoría: Pagos
Pregunta: ¿Cómo pagar?
Respuesta: Puedes pagar con tarjeta o transferencia
Multimedia: metodos-pago.jpg

<u>Para enviar multimedia:</u>
1. Sube el archivo a este chat
2. Luego usa /agregar y escribe el nombre del archivo
"""
    msg = bot.reply_to(message, instrucciones, parse_mode='HTML')
    bot.register_next_step_handler(msg, procesar_nueva_pregunta)

def procesar_nueva_pregunta(message):
    """Procesa los datos para una nueva pregunta"""
    try:
        # Si el usuario envió un archivo multimedia
        if message.content_type in ['photo', 'video', 'document', 'audio']:
            file_info = None
            file_extension = ''
            
            if message.content_type == 'photo':
                file_info = bot.get_file(message.photo[-1].file_id)
                file_extension = '.jpg'
            elif message.content_type == 'video':
                file_info = bot.get_file(message.video.file_id)
                file_extension = '.mp4'
            elif message.content_type == 'document':
                file_info = bot.get_file(message.document.file_id)
                file_extension = os.path.splitext(message.document.file_name)[1]
            elif message.content_type == 'audio':
                file_info = bot.get_file(message.audio.file_id)
                file_extension = '.mp3'
            
            if file_info:
                downloaded_file = bot.download_file(file_info.file_path)
                file_name = f"file_{message.message_id}{file_extension}"
                file_path = os.path.join(MULTIMEDIA_DIR, file_name)
                
                with open(file_path, 'wb') as new_file:
                    new_file.write(downloaded_file)
                
                bot.reply_to(
                    message, 
                    f"✅ Archivo guardado como: <code>{file_name}</code>\n\n"
                    "Ahora envía los detalles de la pregunta en el formato indicado.",
                    parse_mode='HTML'
                )
                return
        
        # Procesar texto con los datos de la pregunta
        if message.content_type != 'text':
            bot.reply_to(message, "❌ Por favor envía solo texto con el formato indicado.")
            return
        
        lineas = [linea.strip() for linea in message.text.split('\n') if linea.strip()]
        datos = {}
        
        for linea in lineas:
            if linea.lower().startswith('categoría:') or linea.lower().startswith('categoria:'):
                datos['categoria'] = linea.split(':', 1)[1].strip()
            elif linea.lower().startswith('pregunta:'):
                datos['pregunta'] = linea.split(':', 1)[1].strip()
            elif linea.lower().startswith('respuesta:'):
                datos['respuesta'] = linea.split(':', 1)[1].strip()
            elif linea.lower().startswith('multimedia:'):
                datos['multimedia'] = linea.split(':', 1)[1].strip()
        
        # Validar datos mínimos
        if not all(k in datos for k in ['categoria', 'pregunta', 'respuesta']):
            missing = [k for k in ['categoria', 'pregunta', 'respuesta'] if k not in datos]
            bot.reply_to(message, f"❌ Faltan datos: {', '.join(missing)}")
            return
        
        # Verificar si el archivo multimedia existe
        if 'multimedia' in datos and datos['multimedia']:
            if not os.path.exists(os.path.join(MULTIMEDIA_DIR, datos['multimedia'])):
                bot.reply_to(
                    message, 
                    f"⚠️ El archivo '{datos['multimedia']}' no existe en {MULTIMEDIA_DIR}\n\n"
                    "Sube el archivo primero o deja el campo Multimedia vacío."
                )
                return
        
        # Actualizar el JSON
        with open(FAQ_FILE, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            
            # Buscar la categoría
            categoria_existente = next(
                (c for c in data['categorias'] if c['nombre'].lower() == datos['categoria'].lower()), 
                None
            )
            
            nueva_pregunta = {
                'pregunta': datos['pregunta'],
                'respuesta': datos['respuesta'],
                'multimedia': datos.get('multimedia')
            }
            
            if categoria_existente:
                # Actualizar pregunta existente si ya está en la categoría
                pregunta_existente = next(
                    (p for p in categoria_existente['preguntas'] 
                     if p['pregunta'].lower() == datos['pregunta'].lower()),
                    None
                )
                
                if pregunta_existente:
                    pregunta_existente.update({
                        'respuesta': datos['respuesta'],
                        'multimedia': datos.get('multimedia', pregunta_existente.get('multimedia'))
                    })
                    bot.reply_to(message, "✅ Pregunta actualizada correctamente!")
                else:
                    categoria_existente['preguntas'].append(nueva_pregunta)
                    bot.reply_to(message, "✅ Nueva pregunta agregada a la categoría existente!")
            else:
                data['categorias'].append({
                    'nombre': datos['categoria'],
                    'preguntas': [nueva_pregunta]
                })
                bot.reply_to(message, "✅ Nueva categoría y pregunta agregadas!")
            
            # Guardar cambios
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.truncate()
    
    except Exception as e:
        bot.reply_to(message, f"❌ Error al procesar: {str(e)}")

# --------------------------
# INICIAR EL BOT
# --------------------------

if __name__ == '__main__':
    print("🤖 Bot de Preguntas Frecuentes iniciado...")
    bot.polling(none_stop=True)