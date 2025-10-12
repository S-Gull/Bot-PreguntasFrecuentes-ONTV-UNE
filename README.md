# **Guía Paso a Paso para Usar el Bot de Preguntas Frecuentes ONTV**  

Esta guía explica cómo configurar, administrar y usar el bot de preguntas frecuentes para la **Organización Nacional de Trasplantes de Venezuela (ONTV)**.  

---

## **📌 1. Configuración Inicial**  
Antes de usar el bot, debes configurar el entorno.  

### **🔹 Paso 1: Ejecutar el Script de Configuración**  
1. Abre una terminal (`CMD` o `PowerShell` en Windows).  
2. Navega hasta la carpeta del proyecto.  
3. Ejecuta:  
   ```bash
   ConfigurarEntorno.bat
   ```  
4. El script te pedirá el **token de Telegram** (obtén uno con [@BotFather](https://t.me/BotFather)).  
5. Se instalará todo automáticamente.  

✅ **Ejemplo de salida:**  
```
********************************************
* CONFIGURACION DEL TOKEN DE TELEGRAM *
********************************************
Por favor ingrese el token de su bot de Telegram: 8118750964:AAHfYr7NqtJWqYgqbmEYdocXQuSw8Fwy7Ok
¡Configuración completada con éxito!
```  

---

## **🤖 2. Iniciar el Bot**  
Una vez configurado, ejecuta:  
```bash
IniciarBot.bat
```  
El bot estará en línea y responderá a comandos en Telegram.  

✅ **Ejemplo de inicio:**  
```
🤖 Bot de Preguntas Frecuentes iniciado...
📂 Directorio multimedia: ./Bot-PreguntasFrecuentes/multimedia
📄 Archivo de preguntas: ./Bot-PreguntasFrecuentes/Datos/faq.json
```  

---

## **👤 3. Uso Básico para Usuarios**  
Los usuarios pueden interactuar con el bot usando estos comandos:  

| **Comando** | **Descripción** | **Ejemplo** |
|------------|----------------|-------------|
| `/start` o `/help` | Muestra el menú principal | `/start` |
| `/preguntas` | Lista las categorías de preguntas | `/preguntas` |
| `/id` | Muestra tu ID de usuario (útil para admins) | `/id` |

✅ **Flujo de ejemplo:**  
1. El usuario escribe `/start`.  
2. El bot muestra:  
   ```
   🌟 ¡Bienvenido! 🌟  
   Selecciona una categoría:  
   - Donación de Órganos  
   - Proceso de Trasplante  
   - Registro y Legalidad  
   - Mitos y Verdades  
   ```  
3. El usuario selecciona una categoría y luego una pregunta.  
4. El bot responde con la información.  

---

## **👑 4. Panel de Administración (Solo para Admins)**  
Los administradores pueden gestionar preguntas y administradores.  

### **🔹 Acceso al Panel Admin**  
1. Ejecuta `/start` o escribe `📚 Preguntas` / `👑 Administradores`.  
2. Si tu ID está en `ADMIN_IDS` (en `config.py`), verás el menú de administración.  

✅ **Ejemplo:**  
```
🔧 Panel de Administración  
Selecciona una opción:  
📚 Preguntas  
👑 Administradores  
```  

---

### **📝 Gestión de Preguntas**  
| **Opción** | **Descripción** | **Ejemplo** |
|------------|----------------|-------------|
| `📝 Agregar Pregunta` | Añade una nueva pregunta | Pregunta: *"¿Puedo ser donante si tengo diabetes?"* Respuesta: *"Sí, pero depende del tipo..."* |
| `📋 Listar Preguntas` | Muestra todas las preguntas | Lista todas las categorías y preguntas |
| `🗑️ Eliminar Pregunta` | Borra una pregunta existente | Eliminar: *"¿La donación afecta los ritos funerarios?"* |

✅ **Flujo para agregar una pregunta:**  
1. Selecciona `📝 Agregar Pregunta`.  
2. Escribe la pregunta:  
   ```
   ✏️ Agregar nueva pregunta  
   Por favor escribe la pregunta:  
   ¿Puedo donar si tengo VIH?  
   ```  
3. Escribe la respuesta:  
   ```
   📝 Ahora escribe la respuesta para esta pregunta:  
   No, por razones de seguridad médica...  
   ```  
4. El bot pregunta si quieres agregar multimedia (opcional).  
5. Selecciona una categoría o crea una nueva.  
6. ¡Listo! La pregunta ya está disponible.  

---

### **👥 Gestión de Administradores**  
| **Opción** | **Descripción** | **Ejemplo** |
|------------|----------------|-------------|
| `➕ Agregar Admin` | Añade un nuevo admin | ID: `123456789` → Ahora es admin |
| `➖ Eliminar Admin` | Elimina un admin | Eliminar: `123456789` |

✅ **Flujo para agregar un admin:**  
1. Selecciona `👑 Administradores` → `➕ Agregar Admin`.  
2. Ingresa el ID del usuario (obtenlo con `/id`).  
3. El bot confirma:  
   ```
   ✅ Usuario 123456789 añadido como administrador.  
   ```  

---

## **📌 5. Ejemplo de Uso Completo**  
**Caso:** Un usuario quiere saber sobre donación y trasplantes.  

1. **Usuario escribe:** `/start`  
2. **Bot responde:**  
   ```
   🌟 ¡Bienvenido! 🌟  
   Selecciona una categoría:  
   - Donación de Órganos  
   - Proceso de Trasplante  
   ```  
3. **Usuario selecciona:** `Donación de Órganos`  
4. **Bot muestra preguntas:**  
   ```
   ❓ Donación de Órganos  
   - ¿Quién puede ser donante?  
   - ¿Qué órganos se pueden donar?  
   ```  
5. **Usuario elige:** `¿Qué órganos se pueden donar?`  
6. **Bot responde:**  
   ```
   Se pueden donar: riñones, hígado, corazón...  
   Un solo donante puede salvar hasta 8 vidas.  
   ```  

---

## **⚠️ 6. Posibles Errores y Soluciones**  
| **Error** | **Solución** |
|-----------|--------------|
| *"Token no configurado"* | Editar `Credentials.json` con el token correcto |
| *"No hay preguntas disponibles"* | Usar el panel admin para agregar preguntas |
| *"No tengo permisos de admin"* | Asegurarse de que tu ID esté en `ADMIN_IDS` |

---

## **✅ Conclusión**  
Este bot permite:  
✔ Acceso rápido a información sobre donación de órganos.  
✔ Panel de administración para gestionar contenido.  
✔ Soporte para multimedia (imágenes, videos).  

**📢 ¿Listo para usarlo?** Ejecuta `IniciarBot.bat` y comienza a interactuar. 🚀