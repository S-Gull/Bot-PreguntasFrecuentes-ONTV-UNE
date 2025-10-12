#./Bot-PreguntasFrecuentes/admin.py
import json
import os
import re
from telebot import types
import config

# ==============================================
# FUNCIONES DE MENÚ
# ==============================================


def menu_admin(chat_id):
    """Muestra el menú principal de administración"""
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_preguntas = types.KeyboardButton("📚 Preguntas")
    btn_categorias = types.KeyboardButton("📁 Categorías")
    btn_admins = types.KeyboardButton("👑 Administradores")
    btn_ver_usuario = types.KeyboardButton("👁️ Ver como Usuario")

    markup.add(btn_preguntas, btn_categorias)
    markup.add(btn_admins, btn_ver_usuario)

    config.bot_instance.send_message(
        chat_id,
        "🔧 <b>Panel de Administración</b>\nSelecciona una opción:",
        reply_markup=markup,
        parse_mode='HTML'
    )


def menu_preguntas(chat_id):
    """Muestra el submenú de gestión de preguntas"""
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_add = types.KeyboardButton("📝 Agregar Pregunta")
    btn_edit = types.KeyboardButton("✏️ Editar Pregunta")
    btn_list = types.KeyboardButton("📋 Listar Preguntas")
    btn_del = types.KeyboardButton("🗑️ Eliminar Pregunta")
    btn_back = types.KeyboardButton("🔙 Volver")
    markup.add(btn_add, btn_edit, btn_list, btn_del, btn_back)

    config.bot_instance.send_message(
        chat_id,
        "📚 <b>Menú de Preguntas</b>\nSelecciona una opción:",
        parse_mode='HTML',
        reply_markup=markup
    )


def menu_administradores(chat_id):
    """Muestra el submenú de gestión de administradores"""
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_add = types.KeyboardButton("➕ Agregar Admin")
    btn_remove = types.KeyboardButton("➖ Eliminar Admin")
    btn_back = types.KeyboardButton("🔙 Volver")
    markup.add(btn_add, btn_remove, btn_back)

    config.bot_instance.send_message(
        chat_id,
        "👑 <b>Menú de Administradores</b>\nSelecciona una opción:",
        parse_mode='HTML',
        reply_markup=markup
    )

# ==============================================
# FUNCIONES DE GESTIÓN DE ADMINISTRADORES
# ==============================================


def iniciar_agregar_admin(message):
    """Inicia el proceso para agregar un administrador"""
    msg = config.bot_instance.send_message(
        message.chat.id,
        "👤 Ingresa el ID del nuevo administrador:",
        reply_markup=types.ForceReply(selective=True)
    )
    config.bot_instance.register_next_step_handler(msg, procesar_nuevo_admin)


def procesar_nuevo_admin(message):
    """Procesa el ID del nuevo administrador"""
    try:
        admin_id = int(message.text.strip())
    except ValueError:
        config.bot_instance.reply_to(
            message, "❌ El ID debe ser un número entero.")
        return menu_administradores(message.chat.id)

    if admin_id in config.ADMIN_IDS:
        config.bot_instance.reply_to(
            message, "ℹ️ Este usuario ya es administrador.")
    else:
        config.ADMIN_IDS.append(admin_id)
        actualizar_lista_admins()
        config.bot_instance.reply_to(
            message, f"✅ Usuario {admin_id} añadido como administrador.")

    menu_administradores(message.chat.id)


def iniciar_eliminar_admin(message):
    """Inicia el proceso para eliminar un administrador"""
    if not config.ADMIN_IDS:
        config.bot_instance.send_message(
            message.chat.id, "ℹ️ No hay administradores registrados.")
        return menu_administradores(message.chat.id)

    markup = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True)
    
    # Obtener información de cada admin
    for admin_id in config.ADMIN_IDS:
        try:
            # Intentar obtener información del usuario
            user = config.bot_instance.get_chat(admin_id)
            username = f"@{user.username}" if user.username else "Sin usuario"
            first_name = user.first_name or "Sin nombre"
            last_name = f" {user.last_name}" if user.last_name else ""
            full_name = f"{first_name}{last_name}"
            
            # Crear texto para el botón y mostrar información
            button_text = f"{full_name} ({username})"
            markup.add(button_text)
            
            # Mostrar información detallada
            config.bot_instance.send_message(
                message.chat.id,
                f"👤 Admin ID: {admin_id}\n"
                f"Nombre: {full_name}\n"
                f"Usuario: {username}\n"
                "────────────────────"
            )
        except Exception as e:
            print(f"Error al obtener info del admin {admin_id}: {str(e)}")
            # Si falla, mostrar solo el ID
            markup.add(str(admin_id))
    
    markup.add("🔙 Cancelar")

    msg = config.bot_instance.send_message(
        message.chat.id,
        "🗑️ Selecciona el administrador a eliminar:",
        reply_markup=markup
    )
    config.bot_instance.register_next_step_handler(
        msg, procesar_eliminar_admin)
    
def procesar_eliminar_admin(message):
    """Procesa la eliminación del administrador"""
    if message.text == "🔙 Cancelar":
        return menu_administradores(message.chat.id)

    try:
        # Extraer el ID del admin del texto del botón (que ahora puede contener más info)
        # Buscar el admin cuyo botón coincide con el texto seleccionado
        selected_text = message.text.strip()
        admin_id = None
        
        # Primero intentamos encontrar coincidencia con los botones que tienen texto completo
        for id in config.ADMIN_IDS:
            try:
                user = config.bot_instance.get_chat(id)
                username = f"@{user.username}" if user.username else "Sin usuario"
                first_name = user.first_name or "Sin nombre"
                last_name = f" {user.last_name}" if user.last_name else ""
                full_name = f"{first_name}{last_name}"
                button_text = f"{full_name} ({username})"
                
                if selected_text == button_text:
                    admin_id = id
                    break
            except:
                # Si falla, comparar directamente con el ID
                if selected_text == str(id):
                    admin_id = id
                    break
        
        if admin_id is None:
            # Si no encontramos coincidencia, intentar extraer el ID directamente
            admin_id = int(selected_text.split()[0])  # Esto es un fallback por si acaso
    except ValueError:
        config.bot_instance.reply_to(message, "❌ Selección inválida.")
        return menu_administradores(message.chat.id)
    except Exception as e:
        config.bot_instance.reply_to(message, f"❌ Error: {str(e)}")
        return menu_administradores(message.chat.id)

    if admin_id not in config.ADMIN_IDS:
        config.bot_instance.reply_to(
            message, "❌ Este usuario no está en la lista de administradores.")
    else:
        config.ADMIN_IDS.remove(admin_id)
        actualizar_lista_admins()
        
        # Obtener info del admin eliminado para el mensaje
        try:
            user = config.bot_instance.get_chat(admin_id)
            username = f"@{user.username}" if user.username else "Sin usuario"
            name = user.first_name or "Administrador"
            config.bot_instance.reply_to(
                message, f"✅ Administrador eliminado: {name} ({username})")
        except:
            config.bot_instance.reply_to(
                message, f"✅ Administrador ID {admin_id} eliminado.")

    menu_administradores(message.chat.id)

def actualizar_lista_admins():
    """Actualiza el archivo config.py con la lista actual de administradores"""
    try:
        # Leer el archivo config.py
        config_path = os.path.join(os.path.dirname(__file__), 'config.py')
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Actualizar la línea de ADMIN_IDS
        new_line = f"ADMIN_IDS = {config.ADMIN_IDS}"
        content = re.sub(
            r"ADMIN_IDS\s*=\s*\[.*?\]",
            new_line,
            content,
            flags=re.DOTALL
        )

        # Guardar los cambios
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True
    except Exception as e:
        print(f"Error al actualizar lista de admins: {str(e)}")
        return False

# ==============================================
# SECCIÓN PARA AGREGAR PREGUNTAS
# ==============================================


def iniciar_agregar_pregunta(message):
    """Inicia el flujo para agregar una nueva pregunta"""
    msg = config.bot_instance.send_message(
        message.chat.id,
        "✏️ <b>Agregar nueva pregunta</b>\n\nPor favor escribe la pregunta:",
        parse_mode='HTML',
        reply_markup=types.ForceReply(selective=True)
    )
    config.bot_instance.register_next_step_handler(msg, procesar_pregunta)


def procesar_pregunta(message):
    """Procesa el texto de la pregunta ingresada"""
    if message.content_type != 'text':
        config.bot_instance.reply_to(
            message, "❌ Debes enviar texto. Intenta nuevamente.")
        return menu_admin(message.chat.id)

    user_data = {
        'pregunta': message.text,
        'chat_id': message.chat.id,
        'message_id': message.message_id
    }

    msg = config.bot_instance.send_message(
        message.chat.id,
        "📝 Ahora escribe la respuesta para esta pregunta:",
        reply_markup=types.ForceReply(selective=True)
    )
    config.bot_instance.register_next_step_handler(
        msg, procesar_respuesta, user_data)


def procesar_respuesta(message, user_data):
    """Procesa la respuesta ingresada"""
    if message.content_type != 'text':
        config.bot_instance.reply_to(
            message, "❌ Debes enviar texto. Intenta nuevamente.")
        return menu_admin(message.chat.id)

    user_data['respuesta'] = message.text

    markup = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True)
    markup.add("✅ Sí", "❌ No")

    msg = config.bot_instance.send_message(
        message.chat.id,
        "🖼️ ¿Deseas agregar multimedia (imagen, video, documento)?",
        reply_markup=markup
    )
    config.bot_instance.register_next_step_handler(
        msg, preguntar_multimedia, user_data)


def preguntar_multimedia(message, user_data):
    """Pregunta si desea agregar archivo multimedia"""
    if message.text.lower() not in ['sí', 'si', '✅ sí', 's']:
        user_data['multimedia'] = None
        return seleccionar_categoria(message, user_data)

    msg = config.bot_instance.send_message(
        message.chat.id,
        "📤 Envía la imagen, video o documento:",
        reply_markup=types.ReplyKeyboardRemove()
    )
    config.bot_instance.register_next_step_handler(
        msg, procesar_multimedia, user_data)


def procesar_multimedia(message, user_data):
    """Procesa y guarda el archivo multimedia"""
    file_types = {
        'photo': ('photo', '.jpg'),
        'video': ('video', '.mp4'),
        'document': ('document', '')
    }

    if message.content_type not in file_types:
        config.bot_instance.reply_to(message, "❌ Formato no soportado.")
        return seleccionar_categoria(message, user_data)

    try:
        file_type, ext = file_types[message.content_type]
        file_id = getattr(
            message, file_type)[-1].file_id if file_type == 'photo' else getattr(message, file_type).file_id
        file_info = config.bot_instance.get_file(file_id)

        if file_type == 'document':
            ext = os.path.splitext(getattr(message, file_type).file_name)[1]

        filename = f"media_{message.message_id}{ext}"
        filepath = os.path.join(config.MULTIMEDIA_DIR, filename)

        downloaded_file = config.bot_instance.download_file(file_info.file_path)
        with open(filepath, 'wb') as f:
            f.write(downloaded_file)

        user_data['multimedia'] = filename
        config.bot_instance.reply_to(
            message, "✅ Multimedia guardado correctamente!")
    except Exception as e:
        config.bot_instance.reply_to(message, f"❌ Error al guardar: {str(e)}")
        user_data['multimedia'] = None

    seleccionar_categoria(message, user_data)


def seleccionar_categoria(message, user_data):
    """Permite seleccionar o crear categoría"""
    markup = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True)

    if config.preguntas['categorias']:
        for cat in config.preguntas['categorias']:
            markup.add(cat['nombre'])

    markup.add("➕ Crear nueva categoría", "🔙 Cancelar")

    msg = config.bot_instance.send_message(
        message.chat.id,
        "📂 Selecciona categoría o crea una nueva:",
        reply_markup=markup
    )
    config.bot_instance.register_next_step_handler(
        msg, guardar_pregunta_completa, user_data)


def guardar_pregunta_completa(message, user_data):
    """Guarda la pregunta completa en la estructura de datos"""
    if message.text == "🔙 Cancelar":
        return menu_admin(message.chat.id)

    categoria_nombre = message.text

    if categoria_nombre == "➕ Crear nueva categoría":
        msg = config.bot_instance.send_message(
            message.chat.id,
            "📝 Escribe el nombre de la nueva categoría:",
            reply_markup=types.ForceReply(selective=True)
        )
        config.bot_instance.register_next_step_handler(
            msg, crear_nueva_categoria, user_data)
        return

    # Buscar o crear categoría
    categoria = next((c for c in config.preguntas['categorias'] if c['nombre'].lower(
    ) == categoria_nombre.lower()), None)

    nueva_pregunta = {
        'pregunta': user_data['pregunta'],
        'respuesta': user_data['respuesta'],
        'multimedia': user_data.get('multimedia')
    }

    if categoria:
        categoria['preguntas'].append(nueva_pregunta)
    else:
        config.preguntas['categorias'].append({
            'nombre': categoria_nombre,
            'preguntas': [nueva_pregunta]
        })

    config.guardar_preguntas()
    config.bot_instance.send_message(
        message.chat.id,
        f"✅ Pregunta agregada a <b>{categoria_nombre}</b>!",
        parse_mode='HTML'
    )
    menu_admin(message.chat.id)


def crear_nueva_categoria(message, user_data):
    """Crea una nueva categoría con la pregunta"""
    if message.content_type != 'text':
        config.bot_instance.reply_to(message, "❌ Debes enviar texto.")
        return menu_admin(message.chat.id)

    nueva_categoria = message.text

    config.preguntas['categorias'].append({
        'nombre': nueva_categoria,
        'preguntas': [{
            'pregunta': user_data['pregunta'],
            'respuesta': user_data['respuesta'],
            'multimedia': user_data.get('multimedia')
        }]
    })

    config.guardar_preguntas()
    config.bot_instance.send_message(
        message.chat.id,
        f"✅ Categoría <b>{nueva_categoria}</b> creada con la pregunta!",
        parse_mode='HTML'
    )
    menu_admin(message.chat.id)

# ==============================================
# SECCIÓN PARA LISTAR PREGUNTAS
# ==============================================


def listar_preguntas(message):
    """Muestra todas las preguntas organizadas por categorías"""
    if not config.preguntas['categorias']:
        return config.bot_instance.send_message(message.chat.id, "ℹ️ No hay preguntas registradas.")

    response = ["📚 <b>Listado completo de preguntas</b>\n"]

    for categoria in config.preguntas['categorias']:
        response.append(f"\n<b>📂 {categoria['nombre']}</b>")
        for i, pregunta in enumerate(categoria['preguntas'], 1):
            has_media = " 📎" if pregunta.get('multimedia') else ""
            response.append(f"{i}. {pregunta['pregunta']}{has_media}")

    config.bot_instance.send_message(
        message.chat.id,
        "\n".join(response),
        parse_mode='HTML'
    )

# ==============================================
# SECCIÓN PARA EDITAR PREGUNTAS
# ==============================================

def iniciar_editar_pregunta(message):
    """Inicia el proceso para editar una pregunta"""
    if not config.preguntas['categorias']:
        return config.bot_instance.send_message(message.chat.id, "ℹ️ No hay preguntas para editar.")

    markup = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True)
    for cat in config.preguntas['categorias']:
        markup.add(cat['nombre'])
    markup.add("🔙 Cancelar")

    msg = config.bot_instance.send_message(
        message.chat.id,
        "✏️ <b>Editar pregunta</b>\nSelecciona una categoría:",
        parse_mode='HTML',
        reply_markup=markup
    )
    config.bot_instance.register_next_step_handler(
        msg, seleccionar_pregunta_para_editar)


def seleccionar_pregunta_para_editar(message):
    """Muestra preguntas de la categoría seleccionada para editar"""
    if message.text == "🔙 Cancelar":
        return menu_admin(message.chat.id)

    categoria = next(
        (c for c in config.preguntas['categorias'] if c['nombre'] == message.text), None)
    if not categoria:
        config.bot_instance.reply_to(message, "❌ Categoría no encontrada")
        return menu_admin(message.chat.id)

    if not categoria['preguntas']:
        config.bot_instance.reply_to(
            message, "ℹ️ Esta categoría no tiene preguntas")
        return menu_admin(message.chat.id)

    markup = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True)
    for pregunta in categoria['preguntas']:
        markup.add(pregunta['pregunta'])
    markup.add("🔙 Cancelar")

    user_data = {
        'categoria': message.text,
        'chat_id': message.chat.id
    }

    msg = config.bot_instance.send_message(
        message.chat.id,
        f"❓ Selecciona la pregunta a editar de <b>{message.text}</b>:",
        parse_mode='HTML',
        reply_markup=markup
    )
    config.bot_instance.register_next_step_handler(
        msg, mostrar_opciones_edicion, user_data)


def mostrar_opciones_edicion(message, user_data):
    """Muestra las opciones de edición para la pregunta seleccionada"""
    if message.text == "🔙 Cancelar":
        return menu_admin(message.chat.id)

    user_data['pregunta_original'] = message.text
    
    # Buscar la pregunta completa
    categoria = next(
        (c for c in config.preguntas['categorias'] if c['nombre'] == user_data['categoria']), None)
    pregunta_obj = next(
        (p for p in categoria['preguntas'] if p['pregunta'] == message.text), None)
    
    if not pregunta_obj:
        config.bot_instance.reply_to(message, "❌ Pregunta no encontrada")
        return menu_admin(message.chat.id)

    user_data['pregunta_obj'] = pregunta_obj

    # Mostrar información actual de la pregunta
    info_actual = [
        f"📝 <b>Pregunta actual:</b>\n{pregunta_obj['pregunta']}",
        f"\n💬 <b>Respuesta actual:</b>\n{pregunta_obj['respuesta']}",
    ]
    
    if pregunta_obj.get('multimedia'):
        info_actual.append(f"\n📎 <b>Multimedia:</b> {pregunta_obj['multimedia']}")
    else:
        info_actual.append("\n📎 <b>Multimedia:</b> Sin archivo")

    config.bot_instance.send_message(
        message.chat.id,
        "\n".join(info_actual),
        parse_mode='HTML'
    )

    # Mostrar opciones de edición
    markup = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True)
    markup.add("📝 Editar Pregunta", "💬 Editar Respuesta")
    markup.add("📎 Editar Multimedia", "📂 Cambiar Categoría")
    markup.add("🔙 Cancelar")

    msg = config.bot_instance.send_message(
        message.chat.id,
        "✏️ <b>¿Qué deseas editar?</b>",
        parse_mode='HTML',
        reply_markup=markup
    )
    config.bot_instance.register_next_step_handler(
        msg, procesar_opcion_edicion, user_data)


def procesar_opcion_edicion(message, user_data):
    """Procesa la opción de edición seleccionada"""
    if message.text == "🔙 Cancelar":
        return menu_admin(message.chat.id)

    if message.text == "📝 Editar Pregunta":
        msg = config.bot_instance.send_message(
            message.chat.id,
            "📝 Escribe la nueva pregunta:",
            reply_markup=types.ForceReply(selective=True)
        )
        config.bot_instance.register_next_step_handler(
            msg, actualizar_pregunta, user_data)
    
    elif message.text == "💬 Editar Respuesta":
        msg = config.bot_instance.send_message(
            message.chat.id,
            "💬 Escribe la nueva respuesta:",
            reply_markup=types.ForceReply(selective=True)
        )
        config.bot_instance.register_next_step_handler(
            msg, actualizar_respuesta, user_data)
    
    elif message.text == "📎 Editar Multimedia":
        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=True, resize_keyboard=True)
        markup.add("📤 Subir nuevo archivo", "🗑️ Eliminar multimedia")
        markup.add("🔙 Cancelar")
        
        msg = config.bot_instance.send_message(
            message.chat.id,
            "📎 ¿Qué deseas hacer con el multimedia?",
            reply_markup=markup
        )
        config.bot_instance.register_next_step_handler(
            msg, procesar_edicion_multimedia, user_data)
    
    elif message.text == "📂 Cambiar Categoría":
        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=True, resize_keyboard=True)
        for cat in config.preguntas['categorias']:
            if cat['nombre'] != user_data['categoria']:
                markup.add(cat['nombre'])
        markup.add("➕ Crear nueva categoría", "🔙 Cancelar")
        
        msg = config.bot_instance.send_message(
            message.chat.id,
            "📂 Selecciona la nueva categoría:",
            reply_markup=markup
        )
        config.bot_instance.register_next_step_handler(
            msg, cambiar_categoria_pregunta, user_data)

def actualizar_pregunta(message, user_data):
    """Actualiza el texto de la pregunta"""
    if message.content_type != 'text':
        config.bot_instance.reply_to(message, "❌ Debes enviar texto.")
        return menu_admin(message.chat.id)

    # Si el mensaje está vacío, mantener la pregunta original
    nueva_pregunta = message.text.strip()
    if not nueva_pregunta:
        config.bot_instance.send_message(message.chat.id, "ℹ️ La pregunta se mantiene sin cambios.")
        return menu_admin(message.chat.id)

    # Buscar y actualizar la pregunta
    categoria = next(
        (c for c in config.preguntas['categorias'] if c['nombre'] == user_data['categoria']), None)
    pregunta_obj = next(
        (p for p in categoria['preguntas'] if p['pregunta'] == user_data['pregunta_original']), None)
    
    pregunta_obj['pregunta'] = nueva_pregunta
    config.guardar_preguntas()
    
    config.bot_instance.send_message(
        message.chat.id,
        f"✅ Pregunta actualizada correctamente en <b>{user_data['categoria']}</b>!",
        parse_mode='HTML'
    )
    menu_admin(message.chat.id)

def actualizar_respuesta(message, user_data):
    """Actualiza el texto de la respuesta"""
    if message.content_type != 'text':
        config.bot_instance.reply_to(message, "❌ Debes enviar texto.")
        return menu_admin(message.chat.id)

    # Si el mensaje está vacío, mantener la respuesta original
    nueva_respuesta = message.text.strip()
    if not nueva_respuesta:
        config.bot_instance.send_message(message.chat.id, "ℹ️ La respuesta se mantiene sin cambios.")
        return menu_admin(message.chat.id)

    # Buscar y actualizar la respuesta
    categoria = next(
        (c for c in config.preguntas['categorias'] if c['nombre'] == user_data['categoria']), None)
    pregunta_obj = next(
        (p for p in categoria['preguntas'] if p['pregunta'] == user_data['pregunta_original']), None)
    
    pregunta_obj['respuesta'] = nueva_respuesta
    config.guardar_preguntas()
    
    config.bot_instance.send_message(
        message.chat.id,
        f"✅ Respuesta actualizada correctamente en <b>{user_data['categoria']}</b>!",
        parse_mode='HTML'
    )
    menu_admin(message.chat.id)
    """Actualiza el texto de la respuesta"""
    if message.content_type != 'text':
        config.bot_instance.reply_to(message, "❌ Debes enviar texto.")
        return menu_admin(message.chat.id)

    # Buscar y actualizar la respuesta
    categoria = next(
        (c for c in config.preguntas['categorias'] if c['nombre'] == user_data['categoria']), None)
    pregunta_obj = next(
        (p for p in categoria['preguntas'] if p['pregunta'] == user_data['pregunta_original']), None)
    
    pregunta_obj['respuesta'] = message.text
    config.guardar_preguntas()
    
    config.bot_instance.send_message(
        message.chat.id,
        f"✅ Respuesta actualizada correctamente en <b>{user_data['categoria']}</b>!",
        parse_mode='HTML'
    )
    menu_admin(message.chat.id)


def procesar_edicion_multimedia(message, user_data):
    """Procesa la edición del multimedia"""
    if message.text == "🔙 Cancelar":
        return menu_admin(message.chat.id)
    
    if message.text == "📤 Subir nuevo archivo":
        msg = config.bot_instance.send_message(
            message.chat.id,
            "📤 Envía el nuevo archivo multimedia (imagen, video o documento):",
            reply_markup=types.ReplyKeyboardRemove()
        )
        config.bot_instance.register_next_step_handler(
            msg, actualizar_multimedia, user_data)
    
    elif message.text == "🗑️ Eliminar multimedia":
        # Buscar y eliminar multimedia
        categoria = next(
            (c for c in config.preguntas['categorias'] if c['nombre'] == user_data['categoria']), None)
        pregunta_obj = next(
            (p for p in categoria['preguntas'] if p['pregunta'] == user_data['pregunta_original']), None)
        
        # Eliminar archivo físico si existe
        if pregunta_obj.get('multimedia'):
            try:
                file_path = os.path.join(config.MULTIMEDIA_DIR, pregunta_obj['multimedia'])
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error al eliminar multimedia: {str(e)}")
        
        pregunta_obj['multimedia'] = None
        config.guardar_preguntas()
        
        config.bot_instance.send_message(
            message.chat.id,
            "✅ Multimedia eliminado correctamente!",
            parse_mode='HTML'
        )
        menu_admin(message.chat.id)


def actualizar_multimedia(message, user_data):
    """Actualiza el archivo multimedia"""
    file_types = {
        'photo': ('photo', '.jpg'),
        'video': ('video', '.mp4'),
        'document': ('document', '')
    }

    if message.content_type not in file_types:
        config.bot_instance.reply_to(message, "❌ Formato no soportado.")
        return menu_admin(message.chat.id)

    try:
        file_type, ext = file_types[message.content_type]
        file_id = getattr(
            message, file_type)[-1].file_id if file_type == 'photo' else getattr(message, file_type).file_id
        file_info = config.bot_instance.get_file(file_id)

        if file_type == 'document':
            ext = os.path.splitext(getattr(message, file_type).file_name)[1]

        filename = f"media_{message.message_id}{ext}"
        filepath = os.path.join(config.MULTIMEDIA_DIR, filename)

        downloaded_file = config.bot_instance.download_file(file_info.file_path)
        with open(filepath, 'wb') as f:
            f.write(downloaded_file)

        # Buscar y actualizar multimedia
        categoria = next(
            (c for c in config.preguntas['categorias'] if c['nombre'] == user_data['categoria']), None)
        pregunta_obj = next(
            (p for p in categoria['preguntas'] if p['pregunta'] == user_data['pregunta_original']), None)
        
        # Eliminar archivo anterior si existe
        if pregunta_obj.get('multimedia'):
            try:
                old_file_path = os.path.join(config.MULTIMEDIA_DIR, pregunta_obj['multimedia'])
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
            except Exception as e:
                print(f"Error al eliminar multimedia anterior: {str(e)}")
        
        pregunta_obj['multimedia'] = filename
        config.guardar_preguntas()
        
        config.bot_instance.reply_to(message, "✅ Multimedia actualizado correctamente!")
    except Exception as e:
        config.bot_instance.reply_to(message, f"❌ Error al guardar: {str(e)}")

    menu_admin(message.chat.id)


def cambiar_categoria_pregunta(message, user_data):
    """Cambia la pregunta a otra categoría"""
    if message.text == "🔙 Cancelar":
        return menu_admin(message.chat.id)

    nueva_categoria_nombre = message.text
    
    if nueva_categoria_nombre == "➕ Crear nueva categoría":
        msg = config.bot_instance.send_message(
            message.chat.id,
            "📝 Escribe el nombre de la nueva categoría:",
            reply_markup=types.ForceReply(selective=True)
        )
        config.bot_instance.register_next_step_handler(
            msg, crear_categoria_y_mover, user_data)
        return

    # Buscar categorías
    categoria_origen = next(
        (c for c in config.preguntas['categorias'] if c['nombre'] == user_data['categoria']), None)
    categoria_destino = next(
        (c for c in config.preguntas['categorias'] if c['nombre'] == nueva_categoria_nombre), None)
    
    if not categoria_destino:
        config.bot_instance.reply_to(message, "❌ Categoría de destino no encontrada")
        return menu_admin(message.chat.id)

    # Buscar y mover la pregunta
    pregunta_obj = next(
        (p for p in categoria_origen['preguntas'] if p['pregunta'] == user_data['pregunta_original']), None)
    
    if pregunta_obj:
        # Remover de categoría origen
        categoria_origen['preguntas'] = [p for p in categoria_origen['preguntas'] 
                                       if p['pregunta'] != user_data['pregunta_original']]
        
        # Agregar a categoría destino
        categoria_destino['preguntas'].append(pregunta_obj)
        
        # Eliminar categoría origen si queda vacía
        if not categoria_origen['preguntas']:
            config.preguntas['categorias'] = [c for c in config.preguntas['categorias'] 
                                            if c['nombre'] != user_data['categoria']]
        
        config.guardar_preguntas()
        
        config.bot_instance.send_message(
            message.chat.id,
            f"✅ Pregunta movida de <b>{user_data['categoria']}</b> a <b>{nueva_categoria_nombre}</b>!",
            parse_mode='HTML'
        )
    else:
        config.bot_instance.reply_to(message, "❌ Error al mover la pregunta")
    
    menu_admin(message.chat.id)


def crear_categoria_y_mover(message, user_data):
    """Crea una nueva categoría y mueve la pregunta allí"""
    if message.content_type != 'text':
        config.bot_instance.reply_to(message, "❌ Debes enviar texto.")
        return menu_admin(message.chat.id)

    nueva_categoria_nombre = message.text
    
    # Buscar categoría origen
    categoria_origen = next(
        (c for c in config.preguntas['categorias'] if c['nombre'] == user_data['categoria']), None)
    
    # Buscar y mover la pregunta
    pregunta_obj = next(
        (p for p in categoria_origen['preguntas'] if p['pregunta'] == user_data['pregunta_original']), None)
    
    if pregunta_obj:
        # Remover de categoría origen
        categoria_origen['preguntas'] = [p for p in categoria_origen['preguntas'] 
                                       if p['pregunta'] != user_data['pregunta_original']]
        
        # Crear nueva categoría con la pregunta
        config.preguntas['categorias'].append({
            'nombre': nueva_categoria_nombre,
            'preguntas': [pregunta_obj]
        })
        
        # Eliminar categoría origen si queda vacía
        if not categoria_origen['preguntas']:
            config.preguntas['categorias'] = [c for c in config.preguntas['categorias'] 
                                            if c['nombre'] != user_data['categoria']]
        
        config.guardar_preguntas()
        
        config.bot_instance.send_message(
            message.chat.id,
            f"✅ Categoría <b>{nueva_categoria_nombre}</b> creada con la pregunta!",
            parse_mode='HTML'
        )
    else:
        config.bot_instance.reply_to(message, "❌ Error al mover la pregunta")
    
    menu_admin(message.chat.id)


def menu_categorias(chat_id):
    """Muestra el submenú de gestión de categorías"""
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_create = types.KeyboardButton("➕ Crear Categoría")
    btn_list = types.KeyboardButton("📋 Listar Categorías")
    btn_delete = types.KeyboardButton("🗑️ Eliminar Categoría")
    btn_back = types.KeyboardButton("🔙 Volver")
    markup.add(btn_create, btn_list, btn_delete, btn_back)

    config.bot_instance.send_message(
        chat_id,
        "📁 <b>Menú de Categorías</b>\nSelecciona una opción:",
        parse_mode='HTML',
        reply_markup=markup
    )
# ==============================================
# SECCIÓN PARA ELIMINAR PREGUNTAS
# ==============================================

def iniciar_eliminar_pregunta(message):
    """Inicia el proceso para eliminar una pregunta"""
    if not config.preguntas['categorias']:
        return config.bot_instance.send_message(message.chat.id, "ℹ️ No hay preguntas para eliminar.")

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for cat in config.preguntas['categorias']:
        markup.add(cat['nombre'])
    markup.add("🔙 Cancelar")

    msg = config.bot_instance.send_message(
        message.chat.id,
        "🗑️ <b>Eliminar pregunta</b>\nSelecciona una categoría:",
        parse_mode='HTML',
        reply_markup=markup
    )
    config.bot_instance.register_next_step_handler(msg, seleccionar_categoria_para_eliminar)

def seleccionar_categoria_para_eliminar(message):
    """Selecciona la categoría para eliminar pregunta"""
    if message.text == "🔙 Cancelar":
        return menu_admin(message.chat.id)

    categoria = next((c for c in config.preguntas['categorias'] if c['nombre'] == message.text), None)
    if not categoria:
        config.bot_instance.reply_to(message, "❌ Categoría no encontrada")
        return menu_admin(message.chat.id)

    if not categoria['preguntas']:
        config.bot_instance.reply_to(message, "ℹ️ Esta categoría no tiene preguntas")
        return menu_admin(message.chat.id)

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for pregunta in categoria['preguntas']:
        markup.add(pregunta['pregunta'])
    markup.add("🔙 Cancelar")

    user_data = {
        'categoria': message.text,
        'chat_id': message.chat.id
    }

    msg = config.bot_instance.send_message(
        message.chat.id,
        f"❓ Selecciona la pregunta a eliminar de <b>{message.text}</b>:",
        parse_mode='HTML',
        reply_markup=markup
    )
    config.bot_instance.register_next_step_handler(msg, confirmar_eliminar_pregunta, user_data)

def confirmar_eliminar_pregunta(message, user_data):
    """Confirma la eliminación de la pregunta"""
    if message.text == "🔙 Cancelar":
        return menu_admin(message.chat.id)

    user_data['pregunta'] = message.text

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("✅ Sí, eliminar", "❌ No, cancelar")

    msg = config.bot_instance.send_message(
        message.chat.id,
        f"⚠️ <b>¿Estás seguro de eliminar esta pregunta?</b>\n\n"
        f"Pregunta: {message.text}\n"
        f"Categoría: {user_data['categoria']}\n\n"
        f"Esta acción no se puede deshacer.",
        parse_mode='HTML',
        reply_markup=markup
    )
    config.bot_instance.register_next_step_handler(msg, procesar_eliminar_pregunta, user_data)

def procesar_eliminar_pregunta(message, user_data):
    """Procesa la eliminación de la pregunta"""
    if message.text == "❌ No, cancelar":
        config.bot_instance.send_message(message.chat.id, "❌ Eliminación cancelada.")
        return menu_admin(message.chat.id)

    if message.text != "✅ Sí, eliminar":
        config.bot_instance.send_message(message.chat.id, "❌ Opción inválida.")
        return menu_admin(message.chat.id)

    # Buscar y eliminar la pregunta
    categoria = next((c for c in config.preguntas['categorias'] if c['nombre'] == user_data['categoria']), None)
    if categoria:
        pregunta_encontrada = None
        for pregunta in categoria['preguntas']:
            if pregunta['pregunta'] == user_data['pregunta']:
                pregunta_encontrada = pregunta
                break
        
        if pregunta_encontrada:
            # Eliminar archivo multimedia si existe
            if pregunta_encontrada.get('multimedia'):
                try:
                    multimedia_path = os.path.join(config.MULTIMEDIA_DIR, pregunta_encontrada['multimedia'])
                    if os.path.exists(multimedia_path):
                        os.remove(multimedia_path)
                except Exception as e:
                    print(f"Error al eliminar multimedia: {e}")
            
            # Eliminar la pregunta
            categoria['preguntas'] = [p for p in categoria['preguntas'] if p['pregunta'] != user_data['pregunta']]
            
            # Eliminar categoría si queda vacía
            if not categoria['preguntas']:
                config.preguntas['categorias'] = [c for c in config.preguntas['categorias'] if c['nombre'] != user_data['categoria']]
            
            config.guardar_preguntas()
            config.bot_instance.send_message(
                message.chat.id,
                f"✅ Pregunta eliminada correctamente de <b>{user_data['categoria']}</b>!",
                parse_mode='HTML'
            )
        else:
            config.bot_instance.send_message(message.chat.id, "❌ Pregunta no encontrada.")
    else:
        config.bot_instance.send_message(message.chat.id, "❌ Categoría no encontrada.")
    
    menu_admin(message.chat.id)

# ==============================================
# FUNCIONES DE GESTIÓN DE CATEGORÍAS
# ==============================================

def iniciar_crear_categoria(message):
    """Inicia el proceso para crear una nueva categoría"""
    msg = config.bot_instance.send_message(
        message.chat.id,
        "📁 Ingresa el nombre de la nueva categoría:",
        reply_markup=types.ForceReply(selective=True)
    )
    config.bot_instance.register_next_step_handler(msg, procesar_nueva_categoria)


def procesar_nueva_categoria(message):
    """Procesa la creación de una nueva categoría"""
    nombre_categoria = message.text.strip()
    
    if not nombre_categoria:
        config.bot_instance.reply_to(
            message, "❌ El nombre de la categoría no puede estar vacío.")
        return menu_categorias(message.chat.id)
    
    # Verificar si la categoría ya existe
    for categoria in config.preguntas['categorias']:
        if categoria['nombre'].lower() == nombre_categoria.lower():
            config.bot_instance.reply_to(
                message, f"❌ La categoría '{nombre_categoria}' ya existe.")
            return menu_categorias(message.chat.id)
    
    # Crear la nueva categoría
    nueva_categoria = {
        "nombre": nombre_categoria,
        "preguntas": []
    }
    
    config.preguntas['categorias'].append(nueva_categoria)
    config.guardar_preguntas()
    
    config.bot_instance.reply_to(
        message, f"✅ Categoría '{nombre_categoria}' creada exitosamente.")
    
    menu_categorias(message.chat.id)


def listar_categorias(message):
    """Lista todas las categorías existentes"""
    if not config.preguntas['categorias']:
        config.bot_instance.send_message(
            message.chat.id, "ℹ️ No hay categorías registradas.")
        return menu_categorias(message.chat.id)
    
    texto = "📁 <b>Categorías existentes:</b>\n\n"
    
    for i, categoria in enumerate(config.preguntas['categorias'], 1):
        num_preguntas = len(categoria['preguntas'])
        texto += f"{i}. <b>{categoria['nombre']}</b>\n"
        texto += f"   📊 {num_preguntas} pregunta(s)\n\n"
    
    config.bot_instance.send_message(
        message.chat.id, texto, parse_mode='HTML')
    
    menu_categorias(message.chat.id)


def iniciar_eliminar_categoria(message):
    """Inicia el proceso para eliminar una categoría"""
    if not config.preguntas['categorias']:
        config.bot_instance.send_message(
            message.chat.id, "ℹ️ No hay categorías para eliminar.")
        return menu_categorias(message.chat.id)
    
    markup = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True)
    
    for categoria in config.preguntas['categorias']:
        markup.add(categoria['nombre'])
    
    markup.add("🔙 Cancelar")
    
    msg = config.bot_instance.send_message(
        message.chat.id,
        "🗑️ Selecciona la categoría a eliminar:\n\n⚠️ <b>Advertencia:</b> Se eliminarán todas las preguntas de esta categoría.",
        reply_markup=markup,
        parse_mode='HTML'
    )
    config.bot_instance.register_next_step_handler(
        msg, procesar_eliminar_categoria)


def procesar_eliminar_categoria(message):
    """Procesa la eliminación de una categoría"""
    if message.text == "🔙 Cancelar":
        return menu_categorias(message.chat.id)
    
    nombre_categoria = message.text.strip()
    categoria_encontrada = None
    indice_categoria = None
    
    # Buscar la categoría
    for i, categoria in enumerate(config.preguntas['categorias']):
        if categoria['nombre'] == nombre_categoria:
            categoria_encontrada = categoria
            indice_categoria = i
            break
    
    if not categoria_encontrada:
        config.bot_instance.reply_to(
            message, "❌ Categoría no encontrada.")
        return menu_categorias(message.chat.id)
    
    # Eliminar archivos multimedia asociados
    for pregunta in categoria_encontrada['preguntas']:
        if pregunta.get('multimedia'):
            multimedia_path = os.path.join(
                config.MULTIMEDIA_DIR, pregunta['multimedia'])
            try:
                if os.path.exists(multimedia_path):
                    os.remove(multimedia_path)
            except Exception as e:
                print(f"Error al eliminar archivo multimedia: {e}")
    
    # Eliminar la categoría
    num_preguntas = len(categoria_encontrada['preguntas'])
    config.preguntas['categorias'].pop(indice_categoria)
    config.guardar_preguntas()
    
    config.bot_instance.reply_to(
        message, 
        f"✅ Categoría '{nombre_categoria}' eliminada exitosamente.\n"
        f"📊 Se eliminaron {num_preguntas} pregunta(s) asociada(s)."
    )
    
    menu_categorias(message.chat.id)


def ver_como_usuario(chat_id):
    """Permite al admin ver el bot como lo vería un usuario normal"""
    from Bot import show_categories
    
    # Crear un markup especial para admins que incluya el botón de volver
    markup = types.InlineKeyboardMarkup()
    
    if not config.preguntas['categorias']:
        markup.add(types.InlineKeyboardButton("🔙 Volver al Panel Admin", callback_data="volver_admin"))
        config.bot_instance.send_message(
            chat_id, 
            "ℹ️ No hay preguntas frecuentes disponibles todavía.",
            reply_markup=markup
        )
        return

    for category in config.preguntas['categorias']:
        markup.add(
            types.InlineKeyboardButton(
                category['nombre'],
                callback_data=f"categoria_{config.preguntas['categorias'].index(category)}"
            )
        )
    
    # Agregar botón especial para volver al panel de admin
    markup.add(types.InlineKeyboardButton("🔙 Volver al Panel Admin", callback_data="volver_admin"))
    
    config.bot_instance.send_message(
        chat_id, 
        "👁️ <b>Vista de Usuario</b>\n\n🌟 <b>¡Bienvenido!</b> 🌟\n\nSelecciona una categoría:",
        reply_markup=markup, 
        parse_mode='HTML'
    )
