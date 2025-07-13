# 📚 Bot de Preguntas Frecuentes para Telegram

## 🤖 Descripción
Este bot permite organizar y responder preguntas frecuentes mediante un menú interactivo en Telegram, con soporte para categorías, subpreguntas y multimedia (imágenes, videos, documentos).

## 🛠️ Funcionamiento del Bot

### 1. Estructura básica
- **Categorías**: Agrupan preguntas relacionadas (ej: "Pagos", "Soporte Técnico")
- **Preguntas**: Cada una con su respuesta correspondiente
- **Multimedia**: Opcionalmente puede incluir imágenes/videos/documentos

### 2. Flujo de interacción
1. Usuario envía `/start` o `/preguntas`
2. Bot muestra lista de categorías disponibles
3. Usuario selecciona categoría → ve lista de preguntas
4. Usuario selecciona pregunta → recibe respuesta
5. Bot ofrece opción de volver atrás o al inicio

### 3. Características técnicas
- Desarrollado en Python con `pyTelegramBotAPI`
- Datos almacenados en formato JSON
- Multimedia almacenada en local (`/multimedia`)
- Soporte multiplataforma

## 📝 Cómo Agregar Preguntas

### Método manual (recomendado):
1. Editar el archivo `Bot-PreguntasFrecuentes/Datos/faq.json`
2. Seguir esta estructura:

```json
{
  "categorias": [
    {
      "nombre": "Nombre Categoría",
      "preguntas": [
        {
          "pregunta": "Texto de la pregunta",
          "respuesta": "Texto de la respuesta",
          "multimedia": "nombre_archivo.ext"  // Opcional
        }
      ]
    }
  ]
}
```

### Para multimedia:
1. Subir archivos a `Bot-PreguntasFrecuentes/multimedia/`
2. Referenciarlos en el campo "multimedia"

## ⚙️ Cómo Funcionan las Preguntas

### Jerarquía:
```
Categoría Principal
├── Pregunta 1 (respuesta directa)
├── Pregunta 2 (con imagen)
└── Subcategoría
    ├── Pregunta A
    └── Pregunta B
```

### Tipos de respuestas:
1. **Texto simple**: Solo respuesta escrita
2. **Con multimedia**: 
   - Imágenes (JPEG, PNG)
   - Videos (MP4)
   - Documentos (PDF)
   - Audio (MP3)

## 💻 Instalación en Cualquier Equipo

### Requisitos:
- Python 3.8+
- Pip
- Git (opcional)

### Pasos:

1. **Clonar repositorio**:
```bash
git clone https://github.com/tu-repositorio/ot-PreguntasFrecuentes-ONTV-UNE.git
cd Bot-PreguntasFrecuentes
```

2. **Configurar entorno** (Linux/macOS):
```bash
chmod +x ConfigurarEntorno.sh
./ConfigurarEntorno.sh
```

3. **Configurar entorno** (Windows):
```bat
ConfigurarEntorno.bat
```

4. **Editar configuración**:
- Agregar tu token de bot en `Bot-PreguntasFrecuentes/Datos/Credentials.json`
- Configurar preguntas en `faq.json`

5. **Iniciar el bot**:
```bash
# Linux/macOS
./IniciarBot.sh

# Windows
IniciarBot.bat
```

## 📂 Estructura de Archivos
```
bot-preguntas/
├── Bot-PreguntasFrecuentes/
│   ├── Datos/
│   │   ├── Credentials.json
│   │   └── faq.json
│   └── multimedia/          # Multimedia
├── ConfigurarEntorno.sh
├── IniciarBot.sh
├── requerimientos.txt
└── README.md
```

## 🚨 Solución de Problemas

### Problemas comunes:
1. **Token no válido**:
   - Verificar que el token en Credentials.json sea correcto
   - Obtener nuevo token con @BotFather si es necesario

2. **Multimedia no aparece**:
   - Verificar que el archivo existe en `/multimedia`
   - Comprobar nombre y extensión en faq.json

3. **Error al iniciar**:
   - Asegurarse que todas las dependencias están instaladas
   - Verificar que Python 3.8+ está instalado



---

💡 **Sugerencia**: Para mantener actualizado el bot, sincroniza periódicamente las preguntas desde tu repositorio Git.