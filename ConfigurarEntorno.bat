@echo off
:: Script para configurar entorno y credenciales del bot de Telegram
SETLOCAL

:: 1. Configuración del entorno virtual
echo Instalando virtualenv...
pip install virtualenv || (
    echo Error al instalar virtualenv
    pause
    exit /b 1
)

echo Creando entorno virtual...
python -m virtualenv venv || (
    echo Error al crear el entorno virtual
    pause
    exit /b 1
)

echo Activando entorno virtual...
call venv\Scripts\activate || (
    echo Error al activar el entorno virtual
    pause
    exit /b 1
)

:: 2. Instalación de dependencias
echo Instalando requerimientos...
pip install -r requerimientos.txt || (
    echo Error al instalar los requerimientos
    pause
    exit /b 1
)

:: 3. Configuración del token
:ask_token
echo.
echo ********************************************
echo * CONFIGURACION DEL TOKEN DE TELEGRAM *
echo ********************************************
set /p token="Por favor ingrese el token de su bot de Telegram: "

:: Validar que se ingresó un token
if "%token%"=="" (
    echo No ha ingresado ningun token. Intente nuevamente.
    goto ask_token
)

:: Crear el JSON con el token
echo Creando archivo de credenciales...
(
    echo {
    echo    "token": "%token%"
    echo }
) > ".\Bot-PreguntasFrecuentes\Datos\Credentials.json" || (
    echo Error al crear el archivo Credentials.json
    pause
    exit /b 1
)

echo.
echo ¡Configuracion completada con exito!
echo Entorno virtual creado y activado
echo Dependencias instaladas
echo Token configurado en Credentials.json
echo.

pause