import json
import os
from telebot import TeleBot, types
import config
from admin import *
from config import *

def initialize_bot():
    """Initialize bot instance and setup handlers"""
    # 1. Load credentials
    with open(config.CREDENTIALS_FILE) as f:
        credentials = json.load(f)
    
    # 2. Create bot instance
    config.bot_instance = TeleBot(credentials["token"])
    
    # 3. Setup handlers
    setup_handlers()
    
    # 4. Load questions
    load_questions()
    
    return config.bot_instance

def load_questions():
    """Load questions from JSON file"""
    try:
        with open(config.FAQ_FILE, 'r', encoding='utf-8') as f:
            config.preguntas = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        config.preguntas = {"categorias": []}
        save_questions()

def save_questions():
    """Save questions to JSON file"""
    with open(config.FAQ_FILE, 'w', encoding='utf-8') as f:
        json.dump(config.preguntas, f, ensure_ascii=False, indent=2)

def setup_handlers():
    """Configure all bot handlers"""
    
    @config.bot_instance.message_handler(commands=['start', 'help', 'preguntas'])
    def start(message):
        """Handle start command"""
        if es_admin(message.from_user.id):
            config.bot_instance.send_message(
                message.chat.id,
                f"👑 <b>Bienvenido Administrador {message.from_user.first_name}!</b>",
                parse_mode='HTML'
            )
            menu_admin(message.chat.id)
        else:
            show_categories(
                message.chat.id,
                "🌟 <b>¡Bienvenido!</b> 🌟\n\nSelecciona una categoría:"
            )
    
    @config.bot_instance.message_handler(func=lambda m: m.text == "🚪 Menú Principal" and es_admin(m.from_user.id))
    def back_to_main_menu(message):
        start(message)
    
    @config.bot_instance.message_handler(func=lambda m: m.text == "📝 Agregar Pregunta" and es_admin(m.from_user.id))
    def add_question_handler(message):
        msg = config.bot_instance.send_message(
            message.chat.id,
            "📝 <b>Agregar Nueva Pregunta</b>\n\nEnvia a continuacion la pregunta:",
            parse_mode='HTML'
        )
        config.bot_instance.register_next_step_handler(msg, procesar_pregunta)
    
    @config.bot_instance.message_handler(func=lambda m: m.text == "📋 Listar Preguntas" and es_admin(m.from_user.id))
    def list_questions_handler(message):
        listar_preguntas(message)
    
    @config.bot_instance.callback_query_handler(func=lambda call: True)
    def handle_callbacks(call):
        if call.data == "volver":
            show_categories(call.message.chat.id)
        elif call.data.startswith('categoria_'):
            handle_category_selection(call)
        elif call.data.startswith('pregunta_'):
            handle_question_selection(call)

def show_categories(chat_id, message=None):
    """Show available categories"""
    markup = types.InlineKeyboardMarkup()
    
    if not config.preguntas['categorias']:
        config.bot_instance.send_message(chat_id, "ℹ️ No hay preguntas frecuentes disponibles todavía.")
        return
    
    for category in config.preguntas['categorias']:
        markup.add(
            types.InlineKeyboardButton(
                category['nombre'], 
                callback_data=f"categoria_{config.preguntas['categorias'].index(category)}"
            )
        )
    
    message = message or "📚 <b>Preguntas Frecuentes</b>\n\nSelecciona una categoría:"
    config.bot_instance.send_message(chat_id, message, reply_markup=markup, parse_mode='HTML')

def handle_category_selection(call):
    """Handle category selection"""
    category_id = int(call.data.split('_')[1])
    category = config.preguntas['categorias'][category_id]
    
    markup = types.InlineKeyboardMarkup()
    for question in category['preguntas']:
        markup.add(types.InlineKeyboardButton(
            question['pregunta'], 
            callback_data=f"pregunta_{category_id}_{category['preguntas'].index(question)}"
        ))
    
    markup.add(types.InlineKeyboardButton("🔙 Volver", callback_data="volver"))
    
    config.bot_instance.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"❓ <b>{category['nombre']}</b>\n\nSelecciona una pregunta:",
        reply_markup=markup,
        parse_mode='HTML'
    )

def handle_question_selection(call):
    """Handle question selection"""
    _, category_id, question_id = call.data.split('_')
    category = config.preguntas['categorias'][int(category_id)]
    question = category['preguntas'][int(question_id)]
    
    if question.get('multimedia'):
        extension = question['multimedia'].split('.')[-1].lower()
        media_path = os.path.join(config.MULTIMEDIA_DIR, question['multimedia'])
        
        try:
            with open(media_path, 'rb') as media:
                if extension in ['jpg', 'jpeg', 'png']:
                    config.bot_instance.send_photo(call.message.chat.id, media, caption=question['respuesta'])
                elif extension in ['mp4', 'gif', 'mov']:
                    config.bot_instance.send_video(call.message.chat.id, media, caption=question['respuesta'])
                else:
                    config.bot_instance.send_document(call.message.chat.id, media, caption=question['respuesta'])
        except FileNotFoundError:
            config.bot_instance.send_message(call.message.chat.id, f"⚠️\n\n{question['respuesta']}", parse_mode='HTML')
    else:
        config.bot_instance.send_message(call.message.chat.id, question['respuesta'])
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        "🔙 Volver a preguntas", 
        callback_data=f"categoria_{category_id}"
    ))
    config.bot_instance.send_message(call.message.chat.id, "¿Necesitas algo más?", reply_markup=markup)

if __name__ == '__main__':
    bot = initialize_bot()
    print("🤖 Bot de Preguntas Frecuentes iniciado...")
    print(f"📂 Directorio multimedia: {MULTIMEDIA_DIR}")
    print(f"📄 Archivo de preguntas: {FAQ_FILE}")
    bot.polling(none_stop=True)
