@echo off
:: Script mejorado para configurar entorno, credenciales y administradores del bot de Telegram
SETLOCAL EnableDelayedExpansion

title Configuración del Bot de Preguntas Frecuentes ONTV

:: Verificar si el entorno virtual ya existe
if exist "venv\" (
    echo Entorno virtual ya existe. Saltando creación...
    goto ask_credentials
)

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

:ask_credentials
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

:: 3. Configuración del token y administradores
:ask_token
echo.
echo ********************************************
echo * CONFIGURACION DEL BOT *
echo ********************************************

:token_section
set /p token="Por favor ingrese el token de su bot de Telegram (deje vacío para omitir): "

:: Opción para omitir la configuración del token
if "%token%"=="" (
    echo.
    echo [ADVERTENCIA] No se configurará el token ahora. Puede editarlo manualmente en:
    echo Bot-PreguntasFrecuentes\Datos\Credentials.json
    echo.
    goto admin_config
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

:admin_config
echo.
echo ********************************************
echo * CONFIGURACION DE ADMINISTRADORES *
echo ********************************************
echo Los administradores se configuran en:
echo Bot-PreguntasFrecuentes\config.py
echo.
echo Administradores actuales: %ADMIN_IDS%
echo.

set /p add_admin="¿Desea agregar un administrador ahora? (s/n): "

if /i "!add_admin!"=="s" (
    :add_admin_loop
    set /p admin_id="Ingrese el ID del administrador (o deje vacío para terminar): "
    
    if "!admin_id!"=="" (
        goto config_complete
    )
    
    :: Verificar que sea un número
    echo !admin_id!| findstr /r "^[0-9][0-9]*$" >nul || (
        echo Error: El ID debe ser un número
        goto add_admin_loop
    )
    
    :: Actualizar lista de administradores
    set "updated_admins=!ADMIN_IDS!"
    if "!updated_admins!"=="" (
        set "updated_admins=!admin_id!"
    ) else (
        set "updated_admins=!updated_admins!, !admin_id!"
    )
    
    :: Actualizar config.py
    python -c "import re; content=open('Bot-PreguntasFrecuentes\config.py', 'r', encoding='utf-8').read(); new_content=re.sub(r'ADMIN_IDS\s*=\s*\[.*?\]', 'ADMIN_IDS = [%updated_admins%]', content, flags=re.DOTALL); open('Bot-PreguntasFrecuentes\config.py', 'w', encoding='utf-8').write(new_content)"
    
    echo Administrador !admin_id! agregado correctamente.
    set "ADMIN_IDS=!updated_admins!"
    goto add_admin_loop
)

:config_complete
echo.
echo ********************************************
echo * RESUMEN DE CONFIGURACION *
echo ********************************************
if not "%token%"=="" (
    echo Token del bot: ******** (configurado)
) else (
    echo Token del bot: NO configurado
)

echo.
echo Administradores configurados: %ADMIN_IDS%
echo.
echo Directorio virtual: venv\
echo Dependencias instaladas
echo.
echo ¡Configuración completada!
echo.
echo Puede iniciar el bot con IniciarBot.bat
echo o editar la configuración manualmente en:
echo - Bot-PreguntasFrecuentes\Datos\Credentials.json
echo - Bot-PreguntasFrecuentes\config.py
echo.

pause