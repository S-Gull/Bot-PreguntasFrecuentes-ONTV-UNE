::./ConfigurarEntorno.bat
@echo off
:: Script mejorado para configurar entorno, credenciales y administradores del bot de Telegram
SETLOCAL EnableDelayedExpansion

title Configuración del Bot de Preguntas Frecuentes ONTV

:: Configurar colores para Windows
for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do (
  set "DEL=%%a"
)

:: Definir códigos de color
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "MAGENTA=[95m"
set "CYAN=[96m"
set "WHITE=[97m"
set "RESET=[0m"

:: Habilitar colores ANSI en Windows 10+
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1

:: Variables de configuración
set "CONFIG_FILE=Bot-PreguntasFrecuentes\config.py"
set "CREDENTIALS_FILE=Bot-PreguntasFrecuentes\Datos\Credentials.json"
set "FAQ_FILE=Bot-PreguntasFrecuentes\Datos\faq.json"
set "MULTIMEDIA_DIR=Bot-PreguntasFrecuentes\multimedia"
set "ADMIN_IDS="

:: Función para mostrar encabezado
call :show_header

:: Verificar Python y pip
call :check_python

:: Verificar estructura de directorios
call :verify_structure

:: Verificar si el entorno virtual ya existe
if exist "venv\" (
    echo %BLUE%Entorno virtual ya existe. Saltando creación...%RESET%
    goto activate_env
)

:: 1. Configuración del entorno virtual
call :setup_virtualenv

:activate_env
echo %YELLOW%Activando entorno virtual...%RESET%
call venv\Scripts\activate || (
    echo %RED%Error al activar el entorno virtual%RESET%
    pause
    exit /b 1
)

:: 2. Instalación de dependencias
echo %YELLOW%Instalando requerimientos...%RESET%
pip install -r requerimientos.txt || (
    echo %RED%Error al instalar los requerimientos%RESET%
    echo %YELLOW%Intentando con python -m pip...%RESET%
    python -m pip install -r requerimientos.txt || (
        echo %RED%Error al instalar los requerimientos con python -m pip%RESET%
        pause
        exit /b 1
    )
)

:: 3. Configuración del token
call :configure_token

:: 4. Configuración de administradores
call :configure_admins

:: 5. Mostrar resumen final
call :show_summary

echo.
echo %GREEN%¡Configuración completada con éxito!%RESET%
echo.
echo Para iniciar el bot ejecute: %CYAN%IniciarBot.bat%RESET%
echo.
pause
exit /b 0

:: ============================================================================
:: FUNCIONES
:: ============================================================================

:show_header
echo.
echo %CYAN%===============================================%RESET%
echo %CYAN%    CONFIGURACIÓN DEL BOT DE TELEGRAM%RESET%
echo %CYAN%         Bot de Preguntas Frecuentes ONTV%RESET%
echo %CYAN%===============================================%RESET%
echo.
goto :eof

:check_python
echo %YELLOW%Verificando instalación de Python...%RESET%

:: Verificar Python
python --version >nul 2>&1 || (
    echo %RED%Error: Python no está instalado o no está en el PATH%RESET%
    echo %YELLOW%Por favor instale Python desde https://python.org%RESET%
    pause
    exit /b 1
)

echo %GREEN%✓ Python encontrado%RESET%

:: Verificar pip
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo %YELLOW%pip no encontrado. Intentando instalar...%RESET%
    python -m ensurepip --upgrade >nul 2>&1
    if errorlevel 1 (
        echo %RED%Error: No se pudo instalar pip%RESET%
        echo %YELLOW%Soluciones posibles:%RESET%
        echo 1. Reinstalar Python con pip incluido
        echo 2. Descargar get-pip.py desde https://bootstrap.pypa.io/get-pip.py
        echo 3. Ejecutar: python get-pip.py
        pause
        exit /b 1
    )
)

echo %GREEN%✓ pip encontrado%RESET%
goto :eof

:setup_virtualenv
echo %YELLOW%Configurando entorno virtual...%RESET%

:: Intentar crear entorno virtual con venv (incluido en Python 3.3+)
echo %YELLOW%Creando entorno virtual con venv...%RESET%
python -m venv venv
if errorlevel 1 (
    echo %YELLOW%venv falló, intentando con virtualenv...%RESET%
    
    :: Instalar virtualenv si no está disponible
    python -m pip install virtualenv || (
        echo %RED%Error al instalar virtualenv%RESET%
        pause
        exit /b 1
    )
    
    :: Crear entorno virtual con virtualenv
    python -m virtualenv venv || (
        echo %RED%Error al crear el entorno virtual%RESET%
        pause
        exit /b 1
    )
)

echo %GREEN%✓ Entorno virtual creado%RESET%
goto :eof

:verify_structure
echo %YELLOW%Verificando estructura de directorios...%RESET%

:: Crear directorios necesarios
if not exist "Bot-PreguntasFrecuentes\Datos\" mkdir "Bot-PreguntasFrecuentes\Datos"
if not exist "%MULTIMEDIA_DIR%\" mkdir "%MULTIMEDIA_DIR%"

:: Crear archivo FAQ vacío si no existe
if not exist "%FAQ_FILE%" (
    echo %YELLOW%Creando archivo de preguntas vacío...%RESET%
    echo {"categorias": []} > "%FAQ_FILE%"
)

echo %GREEN%✓ Estructura de directorios verificada%RESET%
goto :eof

:configure_token
echo.
echo %MAGENTA%============================================%RESET%
echo %MAGENTA%        CONFIGURACIÓN DEL TOKEN%RESET%
echo %MAGENTA%============================================%RESET%
echo.

:: Verificar si ya existe un token
if exist "%CREDENTIALS_FILE%" (
    for /f "tokens=2 delims=\"" %%a in ('findstr "token" "%CREDENTIALS_FILE%" 2^>nul') do (
        set "current_token=%%a"
        if not "!current_token!"=="" (
            set "token_preview=!current_token:~0,4!...!current_token:~-4!"
            echo %BLUE%Token actual: !token_preview!%RESET%
            set /p "change_token=¿Desea cambiar el token? (s/n): "
            if /i not "!change_token!"=="s" goto :eof
        )
    )
)

echo Puede omitir este paso y configurar el token manualmente después en:
echo %CYAN%%CREDENTIALS_FILE%%RESET%
echo.
set /p "token=Ingrese el token de su bot de Telegram (deje vacío para omitir): "

:: Opción para omitir la configuración del token
if "%token%"=="" (
    echo.
    echo %YELLOW%[ADVERTENCIA] Token no configurado. Puede editarlo manualmente más tarde.%RESET%
    echo.
    goto :eof
)

:: Validar formato del token
echo %token% | findstr /r "^[0-9][0-9]*:[a-zA-Z0-9_-][a-zA-Z0-9_-]*$" >nul || (
    echo %RED%Error: Token inválido. Debe tener el formato: 123456789:ABCdefghIJKlmNOPQRStuvwxyz%RESET%
    pause
    exit /b 1
)

:: Crear el JSON con el token
echo %YELLOW%Creando archivo de credenciales...%RESET%
(
    echo {
    echo     "token": "%token%"
    echo }
) > "%CREDENTIALS_FILE%" || (
    echo %RED%Error al crear el archivo Credentials.json%RESET%
    pause
    exit /b 1
)

echo %GREEN%✓ Token configurado correctamente%RESET%
goto :eof

:configure_admins
echo.
echo %MAGENTA%============================================%RESET%
echo %MAGENTA%    CONFIGURACIÓN DE ADMINISTRADORES%RESET%
echo %MAGENTA%============================================%RESET%
echo.

:: Obtener administradores actuales del archivo config.py
if exist "%CONFIG_FILE%" (
    for /f "tokens=*" %%a in ('findstr "ADMIN_IDS" "%CONFIG_FILE%" 2^>nul') do (
        set "config_line=%%a"
        :: Extraer IDs entre corchetes
        for /f "tokens=2 delims=[]" %%b in ("!config_line!") do (
            set "ADMIN_IDS=%%b"
        )
    )
)

if not "%ADMIN_IDS%"=="" (
    echo Administradores actuales: %BLUE%%ADMIN_IDS%%RESET%
) else (
    echo %YELLOW%No hay administradores configurados%RESET%
)

echo.
set /p "add_admin=¿Desea agregar administradores? (s/n): "

if /i not "!add_admin!"=="s" goto :eof

:: Crear array temporal para administradores
set "temp_admins=%ADMIN_IDS%"
set "admin_count=0"

:add_admin_loop
echo.
echo Ingrese los IDs de los administradores (uno por línea)
echo Deje vacío para terminar
set /p "admin_id=ID del administrador: "

if "!admin_id!"=="" goto update_config

:: Verificar que sea un número
echo !admin_id!| findstr /r "^[0-9][0-9]*$" >nul || (
    echo %RED%Error: El ID debe ser un número%RESET%
    goto add_admin_loop
)

:: Verificar duplicados
echo !temp_admins! | findstr /c "!admin_id!" >nul && (
    echo %YELLOW%Este administrador ya está registrado%RESET%
    goto add_admin_loop
)

:: Agregar a la lista temporal
if "!temp_admins!"=="" (
    set "temp_admins=!admin_id!"
) else (
    set "temp_admins=!temp_admins!, !admin_id!"
)

set /a admin_count+=1
echo %GREEN%✓ Administrador !admin_id! agregado%RESET%
goto add_admin_loop

:update_config
if %admin_count% equ 0 (
    echo %BLUE%No se agregaron nuevos administradores%RESET%
    goto :eof
)

:: Actualizar config.py usando PowerShell para mejor manejo de archivos
echo %YELLOW%Actualizando configuración...%RESET%
powershell -Command "$content = Get-Content '%CONFIG_FILE%' -Raw -Encoding UTF8; $content = $content -replace 'ADMIN_IDS\s*=\s*\[.*?\]', 'ADMIN_IDS = [%temp_admins%]'; Set-Content '%CONFIG_FILE%' -Value $content -Encoding UTF8" || (
    echo %RED%Error al actualizar el archivo de configuración%RESET%
    pause
    exit /b 1
)

set "ADMIN_IDS=%temp_admins%"
echo %GREEN%✓ Administradores configurados correctamente%RESET%
echo Nuevos administradores: %BLUE%%temp_admins%%RESET%
goto :eof

:show_summary
echo.
echo %CYAN%============================================%RESET%
echo %CYAN%        RESUMEN DE CONFIGURACIÓN%RESET%
echo %CYAN%============================================%RESET%
echo.

:: Verificar token
if exist "%CREDENTIALS_FILE%" (
    for /f "tokens=2 delims=\"" %%a in ('findstr "token" "%CREDENTIALS_FILE%" 2^>nul') do (
        if not "%%a"=="" (
            echo %GREEN%✓ Token del bot: ******** (configurado)%RESET%
        ) else (
            echo %RED%✗ Token del bot: NO configurado%RESET%
        )
    )
) else (
    echo %RED%✗ Token del bot: NO configurado%RESET%
)

:: Mostrar administradores
if not "%ADMIN_IDS%"=="" (
    echo %GREEN%✓ Administradores: %ADMIN_IDS%%RESET%
) else (
    echo %YELLOW%⚠ No hay administradores configurados%RESET%
)

:: Mostrar archivos
echo %GREEN%✓ Entorno virtual: venv\%RESET%
echo %GREEN%✓ Dependencias instaladas%RESET%
echo %GREEN%✓ Estructura de directorios verificada%RESET%
echo.
echo Archivos de configuración:
echo - %CYAN%%CREDENTIALS_FILE%%RESET%
echo - %CYAN%%CONFIG_FILE%%RESET%
echo - %CYAN%%FAQ_FILE%%RESET%
goto :eof