import json
from telebot import types
import config
import os

def es_admin(user_id):
    """Check if user is admin"""
    return user_id in config.ADMIN_IDS

def menu_admin(chat_id):
    """Show admin menu"""
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("📝 Agregar Pregunta", "📋 Listar Preguntas")
    markup.add("🚪 Menú Principal")
    
    config.bot_instance.send_message(
        chat_id,
        "🔧 <b>Panel de Administración</b>\nSelecciona una opción:",
        reply_markup=markup,
        parse_mode='HTML'
    )

def iniciar_agregar_pregunta(message):
    """Inicia el flujo para agregar pregunta"""
    msg = config.bot_instance.send_message(
        message.chat.id,
        "✏️ <b>Agregar nueva pregunta</b>\n\nPor favor escribe la pregunta:",
        parse_mode='HTML'
    )
    config.bot_instance.register_next_step_handler(msg, procesar_pregunta)

def procesar_pregunta(message):
    """Procesa el texto de la pregunta"""
    if message.content_type != 'text':
        config.bot_instance.reply_to(message, "❌ Debes enviar texto. Por favor intenta nuevamente.")
        return
    
    pregunta = message.text
    user_data = {
        'pregunta': pregunta,
        'chat_id': message.chat.id,
        'message_id': message.message_id
    }
    
    msg = config.bot_instance.send_message(
        message.chat.id,
        "📝 Ahora escribe la respuesta para esta pregunta:",
        reply_markup=types.ForceReply(selective=True)
    )
    config.bot_instance.register_next_step_handler(msg, procesar_respuesta, user_data)

def procesar_respuesta(message, user_data):
    """Procesa la respuesta proporcionada"""
    if message.content_type != 'text':
        config.bot_instance.reply_to(message, "❌ Debes enviar texto. Por favor intenta nuevamente.")
        return
    
    user_data['respuesta'] = message.text
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("✅ Sí", "❌ No")
    
    msg = config.bot_instance.send_message(
        message.chat.id,
        "🖼️ ¿Deseas agregar multimedia (imagen, video, etc.) a esta pregunta?",
        reply_markup=markup
    )
    config.bot_instance.register_next_step_handler(msg, preguntar_multimedia, user_data)

def preguntar_multimedia(message, user_data):
    """Pregunta si desea agregar multimedia"""
    if message.text.lower() not in ['sí', 'si', '✅ sí', 's']:
        user_data['multimedia'] = None
        seleccionar_categoria(message, user_data)
        return
    
    msg = config.bot_instance.send_message(
        message.chat.id,
        "📤 Por favor envía la imagen, video o documento que deseas asociar a esta pregunta:",
        reply_markup=types.ReplyKeyboardRemove()
    )
    config.bot_instance.register_next_step_handler(msg, procesar_multimedia, user_data)

def procesar_multimedia(message, user_data):
    """Procesa el archivo multimedia enviado"""
    if message.content_type not in ['photo', 'video', 'document']:
        config.bot_instance.reply_to(message, "❌ Debes enviar un archivo multimedia válido.")
        return
    
    try:
        # Obtener el archivo según el tipo
        if message.content_type == 'photo':
            file_info = config.bot_instance.get_file(message.photo[-1].file_id)
            extension = '.jpg'
        elif message.content_type == 'video':
            file_info = config.bot_instance.get_file(message.video.file_id)
            extension = '.mp4'
        else:  # document
            file_info = config.bot_instance.get_file(message.document.file_id)
            extension = os.path.splitext(message.document.file_name)[1]
        
        # Descargar y guardar el archivo
        downloaded_file = config.bot_instance.download_file(file_info.file_path)
        filename = f"media_{message.message_id}{extension}"
        filepath = os.path.join(config.MULTIMEDIA_DIR, filename)
        
        with open(filepath, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        user_data['multimedia'] = filename
        config.bot_instance.reply_to(message, "✅ Multimedia guardado correctamente!")
        
    except Exception as e:
        config.bot_instance.reply_to(message, f"❌ Error al guardar multimedia: {str(e)}")
        user_data['multimedia'] = None
    
    seleccionar_categoria(message, user_data)

def seleccionar_categoria(message, user_data):
    """Permite seleccionar o crear categoría"""
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    
    # Agregar categorías existentes
    if config.preguntas['categorias']:
        for categoria in config.preguntas['categorias']:
            markup.add(categoria['nombre'])
    
    markup.add("➕ Crear nueva categoría")
    
    msg = config.bot_instance.send_message(
        message.chat.id,
        "📂 Selecciona una categoría o crea una nueva:",
        reply_markup=markup
    )
    config.bot_instance.register_next_step_handler(msg, guardar_pregunta_completa, user_data)

def guardar_pregunta_completa(message, user_data):
    """Guarda la pregunta completa en la categoría seleccionada"""
    categoria_nombre = message.text
    
    # Si elige crear nueva categoría
    if categoria_nombre == "➕ Crear nueva categoría":
        msg = config.bot_instance.send_message(
            message.chat.id,
            "📝 Escribe el nombre de la nueva categoría:",
            reply_markup=types.ForceReply(selective=True)
        )
        config.bot_instance.register_next_step_handler(msg, crear_nueva_categoria, user_data)
        return
    
    # Buscar categoría existente
    categoria_existente = next(
        (c for c in config.preguntas['categorias'] if c['nombre'].lower() == categoria_nombre.lower()),
        None
    )
    
    if categoria_existente:
        categoria_existente['preguntas'].append({
            'pregunta': user_data['pregunta'],
            'respuesta': user_data['respuesta'],
            'multimedia': user_data.get('multimedia')
        })
    else:
        # Crear nueva categoría si no coincide exactamente
        config.preguntas['categorias'].append({
            'nombre': categoria_nombre,
            'preguntas': [{
                'pregunta': user_data['pregunta'],
                'respuesta': user_data['respuesta'],
                'multimedia': user_data.get('multimedia')
            }]
        })
    
    guardar_pregunta_en_json()
    config.bot_instance.send_message(
        message.chat.id,
        f"✅ Pregunta agregada correctamente a la categoría <b>{categoria_nombre}</b>!",
        parse_mode='HTML',
        reply_markup=types.ReplyKeyboardRemove()
    )
    menu_admin(message.chat.id)

def crear_nueva_categoria(message, user_data):
    """Crea una nueva categoría con la pregunta"""
    if message.content_type != 'text':
        config.bot_instance.reply_to(message, "❌ Debes enviar texto. Por favor intenta nuevamente.")
        return
    
    nueva_categoria = message.text
    
    config.preguntas['categorias'].append({
        'nombre': nueva_categoria,
        'preguntas': [{
            'pregunta': user_data['pregunta'],
            'respuesta': user_data['respuesta'],
            'multimedia': user_data.get('multimedia')
        }]
    })
    
    guardar_pregunta_en_json()
    config.bot_instance.send_message(
        message.chat.id,
        f"✅ Nueva categoría <b>{nueva_categoria}</b> creada con la pregunta!",
        parse_mode='HTML',
        reply_markup=types.ReplyKeyboardRemove()
    )
    menu_admin(message.chat.id)

def guardar_pregunta_en_json():
    """Guarda las preguntas en el archivo JSON"""
    with open(config.FAQ_FILE, 'w', encoding='utf-8') as f:
        json.dump(config.preguntas, f, ensure_ascii=False, indent=2)

def listar_preguntas(message):
    """List all questions for admin"""
    if not config.preguntas['categorias']:
        config.bot_instance.reply_to(message, "ℹ️ No hay preguntas frecuentes registradas todavía.")
        return
    
    response = ["📋 <b>Listado de Preguntas</b>"]
    for categoria in config.preguntas['categorias']:
        response.append(f"\n<b>{categoria['nombre']}</b>:")
        response.extend(
            f"- {p['pregunta']}" + (f" (📁 {p['multimedia']})" if p.get('multimedia') else "")
            for p in categoria['preguntas']
        )
    
    config.bot_instance.reply_to(message, "\n".join(response), parse_mode='HTML')
