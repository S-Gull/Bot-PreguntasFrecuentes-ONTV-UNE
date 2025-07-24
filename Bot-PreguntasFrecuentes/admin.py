from telebot import types
import config

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

def procesar_nueva_pregunta(message):
    """Process new question from admin"""
    try:
        lines = [line.strip() for line in message.text.split('\n') if line.strip()]
        data = {}
        
        for line in lines:
            if line.lower().startswith('categoría:') or line.lower().startswith('categoria:'):
                data['categoria'] = line.split(':', 1)[1].strip()
            elif line.lower().startswith('pregunta:'):
                data['pregunta'] = line.split(':', 1)[1].strip()
            elif line.lower().startswith('respuesta:'):
                data['respuesta'] = line.split(':', 1)[1].strip()
            elif line.lower().startswith('multimedia:'):
                data['multimedia'] = line.split(':', 1)[1].strip()
        
        # Validation and processing...
        config.bot_instance.reply_to(message, "✅ Pregunta agregada correctamente!")
    except Exception as e:
        config.bot_instance.reply_to(message, f"❌ Error: {str(e)}")

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