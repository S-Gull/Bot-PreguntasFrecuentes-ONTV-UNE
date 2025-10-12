# 🤖 Bot de Preguntas Frecuentes - ONTV

Bot de Telegram para la Organización Nacional de Trasplantes de Venezuela que responde preguntas frecuentes sobre donación y trasplantes de órganos.

## 📁 Estructura del Proyecto

### 🐍 **Bot.py** - Archivo Principal
**Ubicación:** `./Bot-PreguntasFrecuentes/Bot.py`

**Descripción:** Archivo principal que inicializa el bot y configura todos los manejadores de comandos y callbacks.

**Funcionalidades:**
- ✅ Inicialización del bot con el token de Telegram
- ✅ Configuración de handlers para comandos (`/start`, `/help`, `/preguntas`, `/id`)
- ✅ Manejo de callbacks para navegación entre categorías y preguntas
- ✅ Detección automática de administradores
- ✅ Sistema de navegación con botones inline
- ✅ Gestión de multimedia (imágenes, videos, documentos)

**Comandos disponibles:**
- `/start` - Inicia el bot y muestra el menú principal
- `/help` - Muestra ayuda
- `/preguntas` - Muestra las categorías de preguntas
- `/id` - Muestra información del usuario y chat

---

### 👑 **admin.py** - Panel de Administración
**Ubicación:** `./Bot-PreguntasFrecuentes/admin.py`

**Descripción:** Módulo completo de administración con todas las funciones de gestión.

**Funcionalidades de Administración:**

#### 🏠 **Menú Principal**
- Panel de control con opciones organizadas
- Navegación entre diferentes módulos

#### 📚 **Gestión de Preguntas**
- ➕ Agregar nuevas preguntas con respuesta y multimedia
- ✏️ Editar preguntas existentes (texto, respuesta, multimedia)
- 📋 Listar todas las preguntas organizadas por categorías
- 🗑️ Eliminar preguntas con confirmación

#### 📁 **Gestión de Categorías**
- ➕ Crear nuevas categorías
- 📋 Listar categorías existentes con estadísticas
- 🗑️ Eliminar categorías (con eliminación de preguntas asociadas)

#### 👑 **Gestión de Administradores**
- ➕ Agregar nuevos administradores por ID
- ➖ Eliminar administradores existentes
- 👁️ Ver como usuario (modo preview)

#### 🔧 **Características Avanzadas**
- Sistema de confirmación para eliminaciones
- Soporte para multimedia (imágenes, videos, documentos)
- Validación de datos de entrada
- Manejo de errores robusto

---

### ⚙️ **config.py** - Configuración del Sistema
**Ubicación:** `./Bot-PreguntasFrecuentes/config.py`

**Descripción:** Archivo de configuración central con todas las variables del sistema.

**Configuraciones:**
- 📁 Rutas de directorios (multimedia, datos)
- 👑 Lista de administradores (`ADMIN_IDS`)
- 🔑 Manejo del token del bot
- 💾 Funciones de guardado y carga de datos
- 🛡️ Verificación de permisos de administrador

**Variables importantes:**
```python
ADMIN_IDS = [1851963523, 1181943029]  # IDs de administradores
MULTIMEDIA_DIR = "ruta/a/multimedia"   # Directorio para archivos
FAQ_FILE = "ruta/a/faq.json"           # Archivo de preguntas
```

---

### ❓ **faq.json** - Base de Datos de Preguntas
**Ubicación:** `./Bot-PreguntasFrecuentes/Datos/faq.json`

**Descripción:** Archivo JSON que almacena todas las preguntas frecuentes organizadas por categorías.

**Estructura:**
```json
{
  "categorias": [
    {
      "nombre": "Nombre Categoría",
      "preguntas": [
        {
          "pregunta": "Texto de la pregunta",
          "respuesta": "Texto de la respuesta",
          "multimedia": "archivo.jpg"
        }
      ]
    }
  ]
}
```

**Categorías incluidas:**
- 🏢 Sobre la ONTV
- 📋 Requisitos y Procesos
- ⚖️ Aspectos Legales
- ❓ Mitos y Realidades
- 🚨 Emergencias y Soporte

---

### 🔑 **Credentials.json** - Credenciales del Bot
**Ubicación:** `./Bot-PreguntasFrecuentes/Datos/Credentials.json`

**Descripción:** Almacena el token de autenticación del bot de Telegram.

**Formato:**
```json
{
    "token": "8339849180:AAG6g6BUsCZxTA2hYa8NuOdES7hfEQ7llRQ"
}
```

---

## 🛠️ Scripts de Configuración

### ⚡ **ConfigurarEntorno.bat**
**Descripción:** Script completo de configuración inicial del entorno.

**Funcionalidades:**
- ✅ Verifica instalación de Python y pip
- ✅ Crea entorno virtual automáticamente
- ✅ Instala dependencias desde `requerimientos.txt`
- ✅ Configura token del bot interactivamente
- ✅ Gestión de administradores iniciales
- ✅ Crea estructura de directorios necesaria
- ✅ Verificación completa del sistema

**Uso:**
```cmd
ConfigurarEntorno.bat
```

---

### ⚙️ **ConfigurarBot.bat** (Reemplaza a AgregarAdmin.bat)
**Descripción:** Herramienta completa de configuración y mantenimiento del bot.

**Funcionalidades:**
- 👑 **Gestión de Administradores**
  - Agregar nuevos administradores
  - Eliminar administradores existentes
  - Lista numerada para selección fácil

- 🔑 **Gestión de Token**
  - Ver token actual (formato seguro)
  - Configurar nuevo token
  - Validaciones de formato

- ℹ️ **Información del Sistema**
  - Estado de archivos de configuración
  - Información de Python y sistema
  - Detalles de administradores configurados

**Uso:**
```cmd
ConfigurarBot.bat
```

---

### 🚀 **IniciarBot.bat**
**Descripción:** Script para ejecutar el bot de forma segura.

**Funcionalidades:**
- ✅ Verifica existencia del entorno virtual
- ✅ Confirma archivos de configuración
- ✅ Activa entorno automáticamente
- ✅ Ejecuta el bot con manejo de errores
- ✅ Instrucciones claras para detener el bot

**Uso:**
```cmd
IniciarBot.bat
```

---

### 📦 **requerimientos.txt**
**Descripción:** Lista de dependencias Python necesarias para el bot.

**Dependencias:**
- `pyTelegramBotAPI>=4.12.0` - Biblioteca principal para Telegram Bot API
- `requests>=2.31.0` - Para peticiones HTTP
- `certifi>=2023.7.22` - Certificados SSL
- `chardet>=5.1.0` - Detección de codificación
- `urllib3>=2.0.4` - Cliente HTTP

---

## 🎯 Características Principales

### 🤖 **Para Usuarios Finales**
- 🔍 Navegación intuitiva por categorías
- 📱 Interfaz responsive con botones
- 🖼️ Soporte para multimedia en respuestas
- 🔄 Navegación fluida entre preguntas

### 👑 **Para Administradores**
- 🛡️ Panel de control seguro
- 📊 Gestión completa de contenido
- 🎨 Interfaz administrativa intuitiva
- 🔄 Sincronización en tiempo real
- 📁 Organización por categorías

### 🔧 **Para Desarrolladores**
- 🏗️ Arquitectura modular y escalable
- 📝 Código bien documentado
- 🐛 Manejo robusto de errores
- 🔒 Validación de datos de entrada
- 💾 Persistencia de datos en JSON

---

## 🚀 Instalación y Uso

### Prerrequisitos
- Python 3.7 o superior
- Token de bot de Telegram (@BotFather)

### Pasos de Instalación
1. **Ejecutar configuración inicial:**
   ```cmd
   ConfigurarEntorno.bat
   ```

2. **Configurar el bot:**
   ```cmd
   ConfigurarBot.bat
   ```

3. **Iniciar el bot:**
   ```cmd
   IniciarBot.bat
   ```

---

## 📞 Soporte y Mantenimiento

### Comandos Útiles
- `Ctrl + C` - Detener el bot correctamente
- `/id` - Obtener ID de usuario para agregar como admin
- `@userinfobot` - Bot de Telegram para obtener tu ID

### Solución de Problemas Comunes
- **Error 409**: Cerrar todas las instancias del bot
- **Error 401**: Verificar token en Credentials.json
- **Multimedia no carga**: Verificar permisos de directorio

---

## 📊 Estructura de Datos

```
Bot-PreguntasFrecuentes/
├── 📄 Bot.py                 # Archivo principal
├── 📄 admin.py               # Panel de administración
├── 📄 config.py              # Configuración
├── 📁 Datos/
│   ├── 📄 Credentials.json   # Token del bot
│   └── 📄 faq.json          # Base de datos
├── 📁 multimedia/           # Archivos multimedia
└── 🛠️ Scripts/
    ├── ⚡ ConfigurarEntorno.bat
    ├── ⚙️ ConfigurarBot.bat
    └── 🚀 IniciarBot.bat
```

---

## 🎉 Características Destacadas

- ✅ **Fácil configuración** con scripts automatizados
- ✅ **Interfaz intuitiva** para usuarios y administradores
- ✅ **Gestión completa** de contenido multimedia
- ✅ **Sistema de permisos** robusto
- ✅ **Base de datos** en JSON fácil de editar
- ✅ **Documentación completa** y ejemplos
- ✅ **Código mantenible** y escalable

---

**✨ Desarrollado para la Organización Nacional de Trasplantes de Venezuela**
