from Accion import Accion
from Constantes import ExtensionesImagen, ExtensionesVideo, SIN_MEDIA, MEDIA_IMAGEN, MEDIA_VIDEO, DirectorioDatos, NivelScript, NuevaLinea, EspaciadoTabulador
from telebot.types import InputMediaPhoto, InputMediaVideo

class PreguntaRespuesta(Accion):
    def __init__(self, pregunta: str, respuesta: str, multimedia: str) -> None:
        super().__init__(pregunta)
        self.Respuesta = respuesta
        self.Multimedia = multimedia
        self.TipoMultimedia = self.IdentificarTipoMultimedia(multimedia)

    def MostrarMensaje(self):
        if self.TipoMultimedia == SIN_MEDIA:
            return self.Respuesta
        else:
            media = open(DirectorioDatos + self.Multimedia, "rb")
            if self.TipoMultimedia == MEDIA_IMAGEN:
                return InputMediaPhoto(media, self.Respuesta)
            elif self.TipoMultimedia == MEDIA_VIDEO:
                return InputMediaVideo(media, self.Respuesta)

    def Seleccionado(self, callback: str, estado):
        return self.MostrarMensaje()

    def AString(self, nivel) -> str:
        resultado = (NivelScript * nivel) + NuevaLinea
        espacioUnTabuladorMenos = EspaciadoTabulador * (nivel - 1)
        resultado += espacioUnTabuladorMenos + "{" + NuevaLinea

        espacioTabulador = EspaciadoTabulador * nivel
        resultado += espacioTabulador + "\"Pregunta\" : \"" + self.Nombre + "\"," + NuevaLinea
        resultado += espacioTabulador + "\"Respuesta\" : \"" + self.Respuesta + "\""

        if self.TipoMultimedia != SIN_MEDIA:
            resultado += ("," + NuevaLinea)
            resultado += espacioTabulador + "\"Multimedia\" : \"" + self.Multimedia + "\""
        resultado += NuevaLinea
        resultado += espacioUnTabuladorMenos + "}" + NuevaLinea
        return resultado

    def IdentificarTipoMultimedia(self, multimedia: str) -> int:
        if not multimedia or len(multimedia) <= 0:
            return SIN_MEDIA

        division = multimedia.split(".")
        if len(division) > 1:
            ext = "." + division[-1]
            if ext in ExtensionesImagen: return MEDIA_IMAGEN
            if ext in ExtensionesVideo: return MEDIA_VIDEO

        return SIN_MEDIA