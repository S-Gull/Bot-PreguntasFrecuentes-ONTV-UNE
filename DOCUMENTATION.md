# **Documentación Técnica Detallada del Bot de Preguntas Frecuentes ONTV**  

Esta documentación explica **el propósito y funcionamiento de cada archivo** en el proyecto del bot de Telegram para la ONTV.  

---

## **📁 Estructura del Proyecto**  
```
Bot-PreguntasFrecuentes/
│
├── Bot.py                # Lógica principal del bot
├── admin.py              # Funciones de administración
├── config.py             # Configuración global
├── Datos/
│   ├── Credentials.json  # Token del bot
│   └── faq.json          # Base de datos de preguntas
├── multimedia/           # Archivos adjuntos (imágenes/videos)
├── ConfigurarEntorno.bat # Instalación automática
└── IniciarBot.bat        # Ejecución del bot
```  

---

## **📄 1. `Bot.py` - Lógica Principal del Bot**  

### **🔹 Propósito**  
- **Inicializa el bot** de Telegram.  
- **Maneja los comandos** (`/start`, `/id`, `/preguntas`).  
- **Gestiona las interacciones** con usuarios (mostrar categorías, preguntas y respuestas).  

### **🔹 Funciones Clave**  
| **Función** | **Descripción** |  
|-------------|----------------|  
| `initialize_bot()` | Carga credenciales, crea el bot y configura handlers. |  
| `load_questions()` | Lee las preguntas desde `faq.json`. |  
| `save_questions()` | Guarda cambios en `faq.json`. |  
| `setup_handlers()` | Define cómo responde el bot a mensajes y comandos. |  
| `show_categories()` | Muestra las categorías disponibles al usuario. |  

### **🔹 Ejemplo de Flujo**  
1. Un usuario envía `/start`.  
2. El bot verifica si es admin o usuario normal.  
3. Muestra categorías desde `faq.json`.  
4. Cuando el usuario selecciona una pregunta, el bot responde con texto o multimedia.  

---

## **📄 2. `admin.py` - Panel de Administración**  

### **🔹 Propósito**  
- **Gestiona preguntas** (agregar, eliminar, listar).  
- **Administra usuarios con privilegios** (agregar/eliminar admins).  

### **🔹 Funciones Clave**  
| **Función** | **Descripción** |  
|-------------|----------------|  
| `menu_admin()` | Muestra el menú principal de administración. |  
| `iniciar_agregar_pregunta()` | Inicia el flujo para añadir una nueva pregunta. |  
| `procesar_multimedia()` | Guarda imágenes/videos en `/multimedia`. |  
| `iniciar_eliminar_admin()` | Elimina un admin de `ADMIN_IDS` en `config.py`. |  

### **🔹 Ejemplo de Uso**  
1. Un admin escribe `📚 Preguntas`.  
2. Selecciona `📝 Agregar Pregunta`.  
3. Sigue los pasos para añadir texto y opcionalmente una imagen.  
4. La pregunta se guarda en `faq.json`.  

---

## **📄 3. `config.py` - Configuración Global**  

### **🔹 Propósito**  
- **Almacena rutas críticas** (archivos JSON, multimedia).  
- **Gestiona la lista de administradores** (`ADMIN_IDS`).  
- **Provee funciones de utilidad** (cargar/guardar datos).  

### **🔹 Variables Importantes**  
| **Variable** | **Descripción** |  
|--------------|----------------|  
| `ADMIN_IDS` | Lista de IDs de usuarios administradores. |  
| `MULTIMEDIA_DIR` | Ruta donde se guardan imágenes/videos. |  
| `FAQ_FILE` | Ruta del archivo `faq.json`. |  

### **🔹 Funciones Útiles**  
| **Función** | **Descripción** |  
|-------------|----------------|  
| `es_admin(user_id)` | Verifica si un usuario es admin. |  
| `save_questions()` | Guarda cambios en `faq.json`. |  

### **🔹 Ejemplo**  
Si un usuario ejecuta `/id`, el bot verifica:  
```python
if es_admin(message.from_user.id):
    mostrar_menu_admin()
else:
    mostrar_menu_usuario()
```  

---

## **📄 4. `Datos/faq.json` - Base de Datos de Preguntas**  

### **🔹 Estructura**  
```json
{
  "categorias": [
    {
      "nombre": "Donación de Órganos",
      "preguntas": [
        {
          "pregunta": "¿Quién puede ser donante?",
          "respuesta": "Cualquier mayor de 18 años...",
          "multimedia": "imagen.png"  // Opcional
        }
      ]
    }
  ]
}
```  

### **🔹 Propósito**  
- **Almacena todas las preguntas y respuestas.**  
- **Soporta adjuntos multimedia** (imágenes, videos).  

### **🔹 Ejemplo de Modificación**  
Si un admin agrega una pregunta:  
1. Se actualiza `faq.json`.  
2. Si hay multimedia, se guarda en `/multimedia`.  

---

## **📄 5. `Datos/Credentials.json` - Token del Bot**  

### **🔹 Estructura**  
```json
{
  "token": "TU_TOKEN_DE_TELEGRAM"
}
```  

### **🔹 Propósito**  
- **Contiene el token único** del bot (obtenido con [@BotFather](https://t.me/BotFather)).  
- **Debe mantenerse privado** (no compartirlo públicamente).  

### **🔹 Ejemplo**  
```json
{
  "token": "8118750964:AAHfYr7NqtJWqYgqbmEYdocXQuSw8Fwy7Ok"
}
```  
- **Este token ⬆️** Es un token de prueba creado por nosotros para testear el bot y no deberia de funcionar al dia que se esta leyendo esto.  


---

## **📄 6. `ConfigurarEntorno.bat` - Instalación Automática**  

### **🔹 Propósito**  
- **Crea un entorno virtual Python** (para aislar dependencias).  
- **Instala los paquetes necesarios** (`python-telegram-bot`, etc.).  
- **Configura el token del bot** interactivamente.  

### **🔹 Ejemplo de Uso**  
```bash
ConfigurarEntorno.bat
> Ingrese token: 8118750964:AAHfYr7NqtJWqYgqbmEYdocXQuSw8Fwy7Ok
> ¡Configuración completada!
```  

---

## **📄 7. `IniciarBot.bat` - Ejecución del Bot**  

### **🔹 Propósito**  
- **Activa el entorno virtual.**  
- **Ejecuta `Bot.py`** para poner el bot en línea.  

### **🔹 Ejemplo de Salida**  
```bash
IniciarBot.bat
🤖 Bot iniciado...
📂 Multimedia: ./multimedia
📄 FAQ: ./Datos/faq.json
```  
- **Asi mismo tenemos estos .bat en el formato sh, hacen basicamente lo mismo pero son para entornos lnux**
---

## **📌 Resumen Final**  

| **Archivo** | **Función Principal** |  
|-------------|----------------------|  
| `Bot.py` | Lógica del bot, comandos y respuestas. |  
| `admin.py` | Gestión de preguntas y administradores. |  
| `config.py` | Configuración global y funciones útiles. |  
| `faq.json` | Base de datos de preguntas/respuestas. |  
| `Credentials.json` | Token de autenticación del bot. |  
| `ConfigurarEntorno.bat` | Instalación automática. |  
| `IniciarBot.bat` | Ejecución del bot. |  

Este sistema permite:  
✅ **Brindar información rápida** sobre donación de órganos.  
✅ **Actualizar contenido fácilmente** mediante el panel admin.  
✅ **Soporte multimedia** para respuestas más completas.  

🚀 **¡El bot está listo para usar!** Ejecuta `IniciarBot.bat` y comienza a interactuar.