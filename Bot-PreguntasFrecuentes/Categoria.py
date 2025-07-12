from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from Constantes import BotonTeclado_Atras, NivelScript, EspaciadoTabulador, NuevaLinea
from Accion import Accion
from PreguntaRespuesta import PreguntaRespuesta

class Categoria(Accion):
    def __init__(self, nombre: str, mensaje: str, omitirAtras=False) -> None:
        super().__init__(nombre)
        self.Mensaje = mensaje if mensaje else f"¿Qué te gustaría saber sobre {nombre}?"
        self.ListaAcciones = []
        self.OmitirAtras = omitirAtras

    def MostrarMensaje(self):
        return self.Mensaje, self.GenerarTeclado()

    def Seleccionado(self, callback: str, estado):
        if estado and len(estado) > 0:
            if len(estado) == 1 and callback == BotonTeclado_Atras:
                return self.Mensaje, self.GenerarTeclado(), []
            else:
                mensaje, teclado, nuevoEstado = self.ListaAcciones[estado[0]].Seleccionado(callback, estado[1:])
                nuevoEstado.insert(0, estado[0])
                return mensaje, teclado, nuevoEstado

        for i, accion in enumerate(self.ListaAcciones):
            if accion.MostrarNombre() == callback:
                if type(accion) is Categoria:
                    mensaje, teclado = accion.MostrarMensaje()
                    return mensaje, teclado, [i]
                elif type(accion) is PreguntaRespuesta:
                    return accion.Seleccionado(callback, None), self.GenerarTeclado(), []

        return self.Mensaje, self.GenerarTeclado(), []

    def AString(self, nivel) -> str:
        resultado = NivelScript * nivel + NuevaLinea
        espacioUnTabuladorMenos = EspaciadoTabulador * (nivel - 1)
        resultado += espacioUnTabuladorMenos + "{" + NuevaLinea

        espacioTabulador = EspaciadoTabulador * nivel
        resultado += espacioTabulador + "\"Nombre\" : \"" + self.Nombre + "\"," + NuevaLinea
        resultado += espacioTabulador + "\"Mensaje\" : \"" + self.Mensaje + "\"" + NuevaLinea
        resultado += espacioUnTabuladorMenos + "}" + NuevaLinea

        for accion in self.ListaAcciones:
            resultado += accion.AString(nivel + 1)

        return resultado

    def AgregarAccion(self, accion):
        self.ListaAcciones.append(accion)

    def GenerarTeclado(self) -> InlineKeyboardMarkup:
        teclado = InlineKeyboardMarkup()
        for accion in self.ListaAcciones:
            teclado.add(InlineKeyboardButton(accion.MostrarNombre(), callback_data=accion.MostrarNombre()))
        if not self.OmitirAtras:
            teclado.add(InlineKeyboardButton(BotonTeclado_Atras, callback_data=BotonTeclado_Atras))
        return teclado