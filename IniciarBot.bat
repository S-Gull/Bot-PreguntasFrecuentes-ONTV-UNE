@echo off
:: Script para ejecutar el bot de Telegram
SETLOCAL EnableDelayedExpansion

title Ejecutando Bot de Preguntas Frecuentes

:: Verificar si el entorno virtual existe
if not exist "venv\Scripts\activate.bat" (
    echo Error: Entorno virtual no encontrado.
    echo Por favor, configure primero el entorno con:
    echo python -m virtualenv venv
    echo call venv\Scripts\activate
    echo pip install -r requerimientos.txt
    pause
    exit /b 1
)

:: Verificar credenciales
if not exist "Bot-PreguntasFrecuentes\Datos\Credentials.json" (
    echo Error: Archivo de credenciales no encontrado.
    echo Por favor, cree el archivo Credentials.json con formato:
    echo {"token": "SU_TOKEN_DE_TELEGRAM"}
    pause
    exit /b 1
)

:: Activar entorno y ejecutar bot
echo Iniciando bot de Telegram...
echo.
echo [INSTRUCCIONES IMPORTANTES]
echo - Para detener el bot correctamente:
echo   1. Presione CTRL+C en esta ventana
echo   2. Espere a que el proceso termine
echo   3. La ventana se cerrara automaticamente
echo.
echo [REGISTRO DEL BOT]
echo ----------------------------------------------------
echo.

call venv\Scripts\activate && python Bot-PreguntasFrecuentes/bot.py

if errorlevel 1 (
    echo.
    echo El bot se ha detenido debido a un error
    pause
) else (
    echo.
    echo El bot se ha detenido correctamente
    timeout /t 3 >nul
)