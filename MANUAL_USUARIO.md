# Manual de Usuario — Bot de Preguntas Frecuentes ONTV

Este manual explica cómo instalar, usar y administrar el bot de Telegram que responde preguntas frecuentes sobre donación y trasplantes en Venezuela.

## 1. Introducción
- El bot organiza información por categorías y preguntas.
- Responde con texto y puede adjuntar multimedia (imágenes, videos, documentos).
- Ofrece un panel de administración para gestionar contenido y administradores.

## 2. Requisitos
- Python 3.7 o superior.
- Token de bot de Telegram (obténlo con `@BotFather`).
- Permisos de escritura en `Bot-PreguntasFrecuentes/Datos` y `Bot-PreguntasFrecuentes/multimedia`.

## 3. Instalación
### Windows
- Ejecuta `ConfigurarEntorno.bat` para crear el entorno virtual e instalar dependencias.
- Ejecuta `ConfigurarBot.bat` para configurar el token y los administradores.
- Inicia el bot con `IniciarBot.bat`.

### Linux
- Otorga permisos: `chmod +x ConfigurarEntorno.sh ConfigurarBot.sh IniciarBot.sh`.
- Ejecuta `./ConfigurarEntorno.sh`, luego `./ConfigurarBot.sh`.
- Inicia el bot con `./IniciarBot.sh`.

## 4. Inicio rápido (usuario)
- Busca tu bot en Telegram y envía `/start`.
- Navega por las categorías con los botones.
- Selecciona una pregunta para ver su respuesta; si existe multimedia, se enviará junto al texto.
- Usa `🔙 Volver` para regresar.

### Comandos útiles
- `/start` muestra categorías y bienvenida.
- `/preguntas` reabre el listado de categorías.
- `/help` muestra ayuda básica.
- `/id` muestra tu ID y datos del chat.

## 5. Uso para administradores
### Acceso
- Si tu ID está en `ADMIN_IDS`, `/start` muestra el “Panel de Administración”.

### Menús principales
- `📚 Preguntas`: añadir, editar, listar y eliminar preguntas.
- `📁 Categorías`: crear, listar y eliminar categorías.
- `👑 Administradores`: agregar o eliminar administradores.
- `👁️ Ver como Usuario`: vista previa del bot como usuario final.

### Flujos comunes
- Agregar pregunta: escribe la pregunta → respuesta → decide si adjuntas multimedia → selecciona o crea categoría → se guarda en `Datos/faq.json`.
- Editar pregunta: cambia texto, respuesta, multimedia o categoría; el sistema actual identifica preguntas por su texto.
- Eliminar pregunta: selecciona categoría y pregunta, confirma; se borra multimedia asociado si existe.
- Categorías: crea nuevas, lista existentes con conteo de preguntas, elimina categorías (con confirmación y limpieza de multimedia).
- Administradores: agrega por ID numérico y elimina; la lista se persiste en `config.py`.

## 6. Estructura de datos
- Base de datos en `Bot-PreguntasFrecuentes/Datos/faq.json`.
- Formato por categoría:
```json
{
  "nombre": "Nombre Categoría",
  "preguntas": [
    {
      "pregunta": "Texto de la pregunta",
      "respuesta": "Texto de la respuesta",
      "multimedia": "archivo.ext" // o null/"" si no hay
    }
  ]
}
```
- El campo `multimedia` puede ser `null`, cadena vacía `""` o nombre de archivo.

## 7. Multimedia
- Se guarda en `Bot-PreguntasFrecuentes/multimedia/`.
- Imágenes (`jpg/png`) se envían como foto; videos (`mp4/gif/mov`) como video; otros formatos como documento.
- Al editar/eliminar, el bot gestiona la limpieza de archivos antiguos.

## 8. Copias de seguridad y restauración
- Copia `Bot-PreguntasFrecuentes/Datos/faq.json` y la carpeta `Bot-PreguntasFrecuentes/multimedia/`.
- Para restaurar: reemplaza `faq.json` y los archivos multimedia en la misma ruta; reinicia el bot.

## 9. Resolución de problemas
- El bot no inicia: verifica token en `Datos/Credentials.json`; reinstala deps con `ConfigurarEntorno`.
- No se envía multimedia: confirma que el archivo existe en `multimedia/` y el formato es compatible.
- No ves panel admin: asegúrate de que tu ID esté en `ADMIN_IDS`; usa `/id` para obtenerlo.
- Cambios no se guardan: revisa permisos de escritura en `Datos/` y `multimedia/`.

## 10. Buenas prácticas
- Evita duplicar exactamente el texto de preguntas dentro de la misma categoría.
- Usa nombres de categorías claros y específicos.
- Mantén respuestas breves y enfocadas; añade multimedia sólo cuando aporte valor.
- Realiza respaldos periódicos de `faq.json` y `multimedia/`.

## 11. Limitaciones conocidas
- La edición y eliminación identifican preguntas por su texto; los duplicados pueden generar ambigüedad.
- La lista de administradores se persiste editando `config.py` (sensible a formato); se recomienda gestionar desde el panel o script.

## 12. Seguridad y privacidad
- `Datos/Credentials.json` contiene el token; no compartas este archivo.
- `.gitignore` evita incluir credenciales en commits.
- Revisa permisos del sistema para proteger datos y multimedia.

## 13. Estructura del proyecto
- Código: `Bot-PreguntasFrecuentes/Bot.py`, `admin.py`, `config.py`.
- Datos: `Bot-PreguntasFrecuentes/Datos/faq.json`, `Credentials.json`.
- Multimedia: `Bot-PreguntasFrecuentes/multimedia/`.
- Scripts: `ConfigurarEntorno`, `ConfigurarBot`, `IniciarBot` (`.bat`/`.sh`).

---
¿Necesitas un manual técnico para desarrolladores o capturas de flujo? Puedo añadirlo en una sección adicional.