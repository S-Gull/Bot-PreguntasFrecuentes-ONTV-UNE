class Accion:
    def __init__(self, nombre: str) -> None:
        self.Nombre = nombre

    def MostrarNombre(self) -> str:
        return self.Nombre

    def MostrarMensaje(self):
        pass

    def Seleccionado(self, callback: str, estado):
        pass
    
    def AString(self, nivel) -> str:
        pass