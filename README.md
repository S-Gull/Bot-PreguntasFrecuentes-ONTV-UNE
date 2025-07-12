# 🤖 Bot de Preguntas Frecuentes para Telegram

![Banner](https://via.placeholder.com/800x200.png?text=Bot+FAQ+Telegram) *(Reemplazar con imagen real)*

Un bot **fácil de configurar** para responder automáticamente preguntas frecuentes en Telegram. Ideal para negocios pequeños, comunidades o servicios que necesitan brindar información rápida.

## 🔍 Índice
- [Características](#-características)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Configuración Inicial](#-configuración-inicial)
- [Uso del Bot](#-uso-del-bot)
- [Formato del FAQ.script](#-formato-del-faqscript)
- [Preguntas Frecuentes](#-preguntas-frecuentes)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

## ✨ Características

| Función | Descripción |
|---------|-------------|
| 📂 Menú jerárquico | Organiza preguntas en categorías y subcategorías |
| 🖼️ Multimedia | Soporta imágenes (.jpg, .png) y videos (.mp4) |
| 🔙 Navegación | Botón "Atrás" para retroceder en el menú |
| 📝 Editor simple | Configuración mediante archivos de texto |
| ☁️ Auto-hospedaje | Funciona en cualquier PC o servidor |

## 📂 Estructura del Proyecto

```plaintext
Bot-PreguntasFrecuentes/
├── 📜 IniciarBot.bat          - Script para lanzar el bot
├── ⚙️ ConfigurarEntorno.bat   - Instalador automático
├── 📝 requerimientos.txt      - Dependencias necesarias
│
├── 📂 CodigoFuente/           - Código principal
│   ├── 🤖 Bot.py              - Lógica del bot
│   ├── 📁 Categoria.py        - Manejo de menús
│   └── ...                   - Otros módulos
│
└── 📂 Datos/                  *No modificar nombre*
    ├── 🔑 Credentials.json    - Token del bot
    └── 📜 FAQ.script         - Base de conocimiento
```
## 🛠️ Configuración Inicial

### 1. Requisitos Previos
Antes de comenzar, necesitarás:

- [Python 3.8 o superior](https://www.python.org/downloads/)  
  *(Marca la opción "Add Python to PATH" durante la instalación)*
  
- Un bot de Telegram:  
  1. Busca [@BotFather](https://t.me/BotFather) en Telegram  
  2. Envía `/newbot` y sigue las instrucciones  
  3. Al final, recibirás un **token** (guárdalo seguro)

### 2. Instalación Paso a Paso

1. **Descargar el proyecto**:
   ```bash
   git clone https://github.com/tu-usuario/Bot-PreguntasFrecuentes.git
   cd Bot-PreguntasFrecuentes
    ```

2. **Editar Datos/`Credentials.json`:**:
    ```json
    {"token": "TU_TOKEN_AQUI"}  
    ```

3. **Ejecutar `ConfigurarEntorno.bat` (Windows) o:**
    ```bash
    pip install -r requerimientos.txt
    ```
## 🚀 Uso del Bot
1. *Iniciar el bot:*

 - Doble clic en IniciarBot.bat o:

    ```bash
    python CodigoFuente/Bot.py
    ```
    - Interactuar:
    ```text
        /start - Muestra el menú principal
    ```
    - Flujo típico:

    ```text
    Usuario: /start
    Bot: "¿En qué puedo ayudarte?" (con botones)
    → Usuario selecciona categoría
    → Bot muestra preguntas disponibles
    → Usuario elige pregunta
    → Bot responde (texto/imagen/video)
    ```
## 📝 Formato del FAQ.script
####   Ejemplo básico:

    -
    {
      "Nombre": "Principal",
      "Mensaje": "Elige una opción:"
    }
    -
    {
      "Pregunta": "Horario",
      "Respuesta": "Abierto de 9am a 6pm"
    }
    

####    Ejemplo avanzado:
    -
    {
      "Nombre": "Soporte",
      "Mensaje": "Problemas técnicos:"
    }
    --
    {
      "Pregunta": "Error 404",
      "Respuesta": "Reinicie la aplicación",
      "Multimedia": "solucion_error.jpg"
    }
    