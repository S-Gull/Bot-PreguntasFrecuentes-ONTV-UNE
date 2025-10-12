::./ConfigurarBot.bat
@echo off
:: Script completo para configurar el bot de Telegram
SETLOCAL EnableDelayedExpansion

title Configurador del Bot - Bot ONTV

:: Variables
set "CONFIG_FILE=Bot-PreguntasFrecuentes\config.py"
set "CREDENTIALS_FILE=Bot-PreguntasFrecuentes\Datos\Credentials.json"

:: Verificar Python
echo Verificando Python...
python --version >nul 2>&1 || (
    echo ERROR: Python no esta instalado o no esta en el PATH.
    echo Por favor instale Python para continuar.
    pause
    exit /b 1
)

:: Verificar archivos de configuración
if not exist "%CONFIG_FILE%" (
    echo ERROR: No se encontro el archivo de configuracion.
    echo Asegurese de ejecutar este script desde el directorio raiz del proyecto.
    echo.
    echo Ruta esperada: %CONFIG_FILE%
    echo.
    pause
    exit /b 1
)

:main_menu
cls
echo.
echo ===============================================
echo           CONFIGURADOR DEL BOT ONTV
echo                   Version 3.0
echo ===============================================
echo.
echo Que desea configurar?
echo.
echo 1. Agregar Administradores
echo 2. Configurar Token del Bot
echo 3. Ver Informacion del Sistema
echo 4. Salir
echo.
echo ===============================================
echo.
set /p "option=Seleccione una opcion (1-4): "

if "%option%"=="1" goto add_admin
if "%option%"=="2" goto token_menu
if "%option%"=="3" goto show_info
if "%option%"=="4" goto exit_script

echo.
echo ERROR: Opcion invalida. Por favor seleccione 1, 2, 3 o 4.
echo.
pause
goto main_menu


:token_menu
cls
echo.
echo ===============================================
echo           CONFIGURAR TOKEN DEL BOT
echo ===============================================
echo.

:: Verificar token actual de forma segura
set "current_token="
set "token_preview=NO CONFIGURADO"

if exist "%CREDENTIALS_FILE%" (
    for /f "tokens=2 delims=:," %%a in ('type "%CREDENTIALS_FILE%" ^| findstr "token"') do (
        set "current_token=%%a"
        set "current_token=!current_token:"=!"
        set "current_token=!current_token: =!"
    )
)

if not "!current_token!"=="" (
    set "token_preview=!current_token:~0,4!...!current_token:~-4!"
)

echo Token actual: !token_preview!

echo.
echo Para obtener un nuevo token:
echo   1. Abra Telegram y busque @BotFather
echo   2. Envie el comando /newbot
echo   3. Siga las instrucciones para crear un bot
echo   4. Copie el token que le proporcione
echo.
echo ===============================================
echo.
set /p "token_action=¿Desea configurar un nuevo token? (s/n): "

if /i not "!token_action!"=="s" goto main_menu

:get_new_token
echo.
echo Ingrese el nuevo token del bot:
echo (o escriba 'cancelar' para volver)
echo.
set /p "new_token=Token: "

if /i "!new_token!"=="cancelar" goto token_menu
if /i "!new_token!"=="menu" goto main_menu

:: Validar token vacío
if "!new_token!"=="" (
    echo ERROR: El token no puede estar vacio.
    echo.
    goto get_new_token
)

:: Validar formato básico del token (debe tener : )
echo !new_token! | findstr ":" >nul || (
    echo ERROR: Formato de token invalido.
    echo El token debe tener el formato: 1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ
    echo.
    goto get_new_token
)

echo.
echo Esta seguro de que desea actualizar el token?
echo Nuevo token: !new_token!
echo.
set /p "confirm=Confirmar (s/n): "

if /i not "!confirm!"=="s" (
    echo Operacion cancelada.
    echo.
    pause
    goto token_menu
)

echo.
echo Actualizando token...

:: Crear directorio si no existe
if not exist "Bot-PreguntasFrecuentes\Datos" mkdir "Bot-PreguntasFrecuentes\Datos"

:: Crear o actualizar el archivo de credenciales
(
    echo {
    echo     "token": "!new_token!"
    echo }
) > "%CREDENTIALS_FILE%"

if exist "%CREDENTIALS_FILE%" (
    echo.
    echo EXITO: Token actualizado correctamente!
    echo.
    echo El bot usara este token en la proxima ejecucion.
) else (
    echo.
    echo ERROR: No se pudo guardar el token.
)

echo.
pause
goto main_menu

:add_admin
cls
echo.
echo ===============================================
echo           AGREGAR NUEVO ADMINISTRADOR
echo ===============================================
echo.
echo Para obtener su ID de Telegram:
echo   1. Abra Telegram y busque el bot @userinfobot
echo   2. Envie el comando /start
echo   3. El bot le mostrara su ID numerico
echo.
echo ===============================================
echo.

:ask_id
echo Ingrese el ID del nuevo administrador:
echo (o escriba 'menu' para volver al menu principal)
echo.
set /p "admin_id=ID: "

if /i "!admin_id!"=="menu" goto admin_menu
if /i "!admin_id!"=="salir" goto admin_menu
if /i "!admin_id!"=="cancelar" goto admin_menu

:: Validar ID
if "!admin_id!"=="" (
    echo ERROR: El ID no puede estar vacio.
    echo.
    goto ask_id
)

echo !admin_id!| findstr /r "^[0-9][0-9]*$" >nul || (
    echo ERROR: El ID debe ser un numero valido.
    echo Ejemplo de ID valido: 123456789
    echo.
    goto ask_id
)

:: Verificar que no esté ya registrado
findstr "!admin_id!" "%CONFIG_FILE%" >nul && (
    echo AVISO: El administrador con ID !admin_id! ya esta registrado.
    echo.
    pause
    goto admin_menu
)

echo.
echo ID valido: !admin_id!
echo.
echo Esta seguro de que desea agregar este administrador?
echo ID a agregar: !admin_id!
echo.
set /p "confirm=Confirmar (s/n): "

if /i not "!confirm!"=="s" (
    echo Operacion cancelada.
    echo.
    pause
    goto admin_menu
)

echo.
echo Procesando...

:: Crear script temporal de Python para actualizar config.py
echo import re > temp_update.py
echo import sys >> temp_update.py
echo. >> temp_update.py
echo try: >> temp_update.py
echo     with open('%CONFIG_FILE%', 'r', encoding='utf-8'^) as f: >> temp_update.py
echo         content = f.read(^) >> temp_update.py
echo. >> temp_update.py
echo     pattern = r'ADMIN_IDS\s*=\s*\[(.*?)\]' >> temp_update.py
echo     match = re.search(pattern, content^) >> temp_update.py
echo. >> temp_update.py
echo     if match: >> temp_update.py
echo         current_ids = match.group(1^).strip(^) >> temp_update.py
echo         if current_ids: >> temp_update.py
echo             new_ids = current_ids + ', !admin_id!' >> temp_update.py
echo         else: >> temp_update.py
echo             new_ids = '!admin_id!' >> temp_update.py
echo         new_line = f'ADMIN_IDS = [{new_ids}]' >> temp_update.py
echo         new_content = re.sub(pattern, new_line, content^) >> temp_update.py
echo         with open('%CONFIG_FILE%', 'w', encoding='utf-8'^) as f: >> temp_update.py
echo             f.write(new_content^) >> temp_update.py
echo         print('SUCCESS'^) >> temp_update.py
echo     else: >> temp_update.py
echo         print('ERROR: No se encontro ADMIN_IDS'^) >> temp_update.py
echo except Exception as e: >> temp_update.py
echo     print(f'ERROR: {e}'^) >> temp_update.py

:: Ejecutar script de Python
python temp_update.py > temp_result.txt 2>&1
set "python_exit=!errorlevel!"

:: Leer resultado
set "result="
for /f "tokens=*" %%i in (temp_result.txt) do set "result=%%i"

if "!python_exit!"=="0" (
    echo !result! | findstr "SUCCESS" >nul
    if !errorlevel! equ 0 (
        echo.
        echo EXITO: Administrador !admin_id! agregado correctamente!
        echo.
        echo Configuracion actualizada:
        type "%CONFIG_FILE%" | findstr "ADMIN_IDS"
        echo.
        echo El administrador ya puede usar los comandos del bot.
    ) else (
        echo ERROR: No se pudo agregar el administrador.
        echo Detalles: !result!
    )
) else (
    echo ERROR: No se pudo agregar el administrador.
    echo Detalles: !result!
)

:: Limpiar archivos temporales
del temp_update.py 2>nul
del temp_result.txt 2>nul

echo.
set /p "continue=Desea agregar otro administrador? (s/n): "
if /i "!continue!"=="s" goto add_admin
goto admin_menu




:show_info
cls
echo.
echo ===============================================
echo           INFORMACION DEL SISTEMA
echo ===============================================
echo.

echo ARCHIVOS DE CONFIGURACION:
echo.

echo [1] %CONFIG_FILE%
if exist "%CONFIG_FILE%" (
    echo    Estado: ENCONTRADO
    for %%F in ("%CONFIG_FILE%") do (
        echo    Tamaño: %%~zF bytes
        echo    Modificado: %%~tF
    )
    echo.
    echo    Administradores configurados:
    type "%CONFIG_FILE%" | findstr "ADMIN_IDS"
) else (
    echo    Estado: NO ENCONTRADO
)

echo.
echo [2] %CREDENTIALS_FILE%
if exist "%CREDENTIALS_FILE%" (
    echo    Estado: ENCONTRADO
    for %%F in ("%CREDENTIALS_FILE%") do (
        echo    Tamaño: %%~zF bytes
        echo    Modificado: %%~tF
    )
    echo.
    echo    Token configurado:
    type "%CREDENTIALS_FILE%" | findstr "token"
) else (
    echo    Estado: NO ENCONTRADO
)

echo.
echo INFORMACION DEL SISTEMA:
echo.
python --version 2>nul && (
    for /f "tokens=*" %%i in ('python --version 2^>nul') do echo    Python: %%i
) || echo    Python: NO ENCONTRADO

echo    Sistema: %OS%
echo    Usuario: %USERNAME%
echo    Directorio: %CD%

echo.
echo ===============================================
echo.
pause
goto main_menu

:exit_script
cls
echo.
echo Gracias por usar el configurador del bot!
echo Bot ONTV - Hasta la vista
echo.
exit /b 0