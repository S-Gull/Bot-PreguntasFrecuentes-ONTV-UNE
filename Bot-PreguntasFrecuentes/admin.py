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
    btn_admins = types.KeyboardButton("👑 Administradores")

    markup.add(btn_preguntas, btn_admins, )

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
    btn_list = types.KeyboardButton("📋 Listar Preguntas")
    btn_del = types.KeyboardButton("🗑️ Eliminar Pregunta")
    btn_back = types.KeyboardButton("🔙 Volver")
    markup.add(btn_add, btn_list, btn_del, btn_back)

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

        downloaded_file = config.bot_instance.download_file(
            file_info.file_path)
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

    config.save_questions()
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

    config.save_questions()
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
# SECCIÓN PARA ELIMINAR PREGUNTAS
# ==============================================


def iniciar_eliminar_pregunta(message):
    """Inicia el proceso para eliminar una pregunta"""
    if not config.preguntas['categorias']:
        return config.bot_instance.send_message(message.chat.id, "ℹ️ No hay preguntas para eliminar.")

    markup = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True)
    for cat in config.preguntas['categorias']:
        markup.add(cat['nombre'])
    markup.add("🔙 Cancelar")

    msg = config.bot_instance.send_message(
        message.chat.id,
        "🗑️ <b>Eliminar pregunta</b>\nSelecciona una categoría:",
        parse_mode='HTML',
        reply_markup=markup
    )
    config.bot_instance.register_next_step_handler(
        msg, seleccionar_pregunta_para_eliminar)


def seleccionar_pregunta_para_eliminar(message):
    """Muestra preguntas de la categoría seleccionada para eliminar"""
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
        f"❓ Selecciona la pregunta a eliminar de <b>{message.text}</b>:",
        parse_mode='HTML',
        reply_markup=markup
    )
    config.bot_instance.register_next_step_handler(
        msg, confirmar_eliminacion, user_data)


def confirmar_eliminacion(message, user_data):
    """Pide confirmación antes de eliminar"""
    if message.text == "🔙 Cancelar":
        return menu_admin(message.chat.id)

    user_data['pregunta'] = message.text

    markup = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True)
    markup.add("✅ Confirmar eliminación", "❌ Cancelar")

    msg = config.bot_instance.send_message(
        message.chat.id,
        f"⚠️ ¿Estás seguro de eliminar esta pregunta?\n\n<b>{message.text}</b>",
        parse_mode='HTML',
        reply_markup=markup
    )
    config.bot_instance.register_next_step_handler(
        msg, eliminar_pregunta, user_data)


def eliminar_pregunta(message, user_data):
    """Elimina la pregunta confirmada"""
    if message.text != "✅ Confirmar eliminación":
        config.bot_instance.reply_to(message, "❌ Eliminación cancelada")
        return menu_admin(message.chat.id)

    categoria_nombre = user_data['categoria']
    pregunta_texto = user_data['pregunta']

    categoria = next(
        (c for c in config.preguntas['categorias'] if c['nombre'] == categoria_nombre), None)
    if not categoria:
        config.bot_instance.reply_to(message, "❌ Categoría no encontrada")
        return menu_admin(message.chat.id)

    pregunta = next(
        (p for p in categoria['preguntas'] if p['pregunta'] == pregunta_texto), None)
    if not pregunta:
        config.bot_instance.reply_to(message, "❌ Pregunta no encontrada")
        return menu_admin(message.chat.id)

    # Eliminar multimedia asociado si existe
    if pregunta.get('multimedia'):
        try:
            file_path = os.path.join(
                config.MULTIMEDIA_DIR, pregunta['multimedia'])
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error al eliminar multimedia: {str(e)}")

    # Eliminar la pregunta
    categoria['preguntas'] = [p for p in categoria['preguntas']
                              if p['pregunta'] != pregunta_texto]

    # Eliminar categoría si queda vacía
    if not categoria['preguntas']:
        config.preguntas['categorias'] = [
            c for c in config.preguntas['categorias'] if c['nombre'] != categoria_nombre]

    config.save_questions()
    config.bot_instance.send_message(
        message.chat.id,
        f"✅ Pregunta eliminada de <b>{categoria_nombre}</b>!",
        parse_mode='HTML'
    )
    menu_admin(message.chat.id)
