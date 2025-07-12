import json
from telebot import TeleBot
from telebot.types import InputMediaPhoto, InputMediaVideo
from Categoria import Categoria
from Constantes import DirectorioDatos, NombreScriptFAQ
from IOArchivos import CargarScript

EstadosUsuarios = {}
ScriptPrincipal = Categoria("Principal", "¿Qué te gustaría saber?", True)

with open(f"{DirectorioDatos}Credentials.json") as archivo:
    credenciales = json.load(archivo)

bot = TeleBot(credenciales["token"])

def EnviarMensaje(usuario, mensaje, teclado=None):
    if isinstance(mensaje, str):
        bot.send_message(usuario, mensaje, reply_markup=teclado)
    elif isinstance(mensaje, (InputMediaPhoto, InputMediaVideo)):
        bot.send_media_group(usuario, [mensaje])
        bot.send_message(usuario, mensaje.caption, reply_markup=teclado)
        mensaje.media.close()

@bot.message_handler(func=lambda m: not m.text.startswith("/"), content_types=["text"])
def ManejarTexto(m):
    EnviarMensaje(m.chat.id, "¿Qué?")

@bot.message_handler(commands=["start"])
def Iniciar(m):
    mensaje, teclado, _ = ScriptPrincipal.Seleccionado(None, [])
    EstadosUsuarios[m.chat.id] = []
    EnviarMensaje(m.chat.id, mensaje, teclado)

@bot.callback_query_handler(func=lambda query: query.data)
def ManejarCallback(query):
    usuario = query.message.chat.id
    estado = EstadosUsuarios.get(usuario, [])
    mensaje, teclado, nuevoEstado = ScriptPrincipal.Seleccionado(query.data, estado)
    EstadosUsuarios[usuario] = nuevoEstado
    EnviarMensaje(usuario, mensaje, teclado)

CargarScript(f"{DirectorioDatos}{NombreScriptFAQ}", ScriptPrincipal)
bot.polling(none_stop=True)