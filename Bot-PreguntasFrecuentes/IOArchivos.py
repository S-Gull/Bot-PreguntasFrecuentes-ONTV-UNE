import json
from Constantes import NivelScript, ClaveIdentificadora_Categoria, ClaveIdentificadora_QyA
from Categoria import Categoria
from PreguntaRespuesta import PreguntaRespuesta

def RecorrerScript(script: Categoria, nivel: int) -> Categoria:
    if nivel > 0:
        if not script.ListaAcciones: return None
        return RecorrerScript(script.ListaAcciones[-1], nivel - 1) if isinstance(script.ListaAcciones[-1], Categoria) else None
    return script

def CargarScript(ruta: str, script: Categoria):
    with open(ruta, "r") as archivo:
        buffer, nivel = "", 0
        for linea in archivo:
            linea = linea.strip().rstrip("\n").lstrip("\t")
            if linea.startswith(NivelScript):
                nivel = sum(1 for c in linea if c == NivelScript)
            elif not buffer and linea.startswith("{"):
                buffer = linea
            elif buffer:
                buffer += linea
                if linea.startswith("}"):
                    datos = json.loads(buffer)
                    categoria = RecorrerScript(script, nivel - 1)
                    if categoria:
                        if ClaveIdentificadora_Categoria in datos:
                            categoria.AgregarAccion(Categoria(datos["Nombre"], datos["Mensaje"]))
                        elif ClaveIdentificadora_QyA in datos:
                            categoria.AgregarAccion(PreguntaRespuesta(
                                datos["Pregunta"], 
                                datos["Respuesta"], 
                                datos.get("Multimedia")))
                    buffer, nivel = "", 0

def GuardarScript(ruta: str, script: Categoria):
    with open(ruta, "w") as archivo:
        archivo.writelines(accion.AString(1) for accion in script.ListaAcciones)