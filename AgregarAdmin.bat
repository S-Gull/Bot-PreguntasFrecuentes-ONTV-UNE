::./AgregarAdmin.bat
@echo off
:: Script simplificado para agregar administradores al bot
SETLOCAL EnableDelayedExpansion

title Gestor de Administradores - Bot ONTV

:: Variables
set "CONFIG_FILE=Bot-PreguntasFrecuentes\config.py"

:: Verificar Python
echo Verificando Python...
python --version >nul 2>&1 || (
    echo ERROR: Python no esta instalado o no esta en el PATH.
    echo Por favor instale Python para continuar.
    pause
    exit /b 1
)

:: Verificar archivo de configuración
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
echo           BOT ONTV - GESTION DE ADMINS
echo                   Version 2.1
echo ===============================================
echo.
echo Que desea hacer?
echo.
echo 1. Agregar nuevo administrador
echo 2. Ver administradores actuales
echo 3. Informacion del sistema
echo 4. Salir
echo.
echo ===============================================
echo.
set /p "option=Seleccione una opcion (1-4): "

if "%option%"=="1" goto add_admin
if "%option%"=="2" goto show_admins
if "%option%"=="3" goto show_info
if "%option%"=="4" goto exit_script

echo.
echo ERROR: Opcion invalida. Por favor seleccione 1, 2, 3 o 4.
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

if /i "%admin_id%"=="menu" goto main_menu
if /i "%admin_id%"=="salir" goto main_menu
if /i "%admin_id%"=="exit" goto main_menu

:: Validar ID
if "%admin_id%"=="" (
    echo ERROR: El ID no puede estar vacio.
    echo.
    goto ask_id
)

echo %admin_id%| findstr /r "^[0-9][0-9]*$" >nul || (
    echo ERROR: El ID debe ser un numero valido.
    echo Ejemplo de ID valido: 123456789
    echo.
    goto ask_id
)

:: Verificar que no esté ya registrado
findstr "%admin_id%" "%CONFIG_FILE%" >nul && (
    echo AVISO: El administrador con ID %admin_id% ya esta registrado.
    echo.
    pause
    goto main_menu
)

echo.
echo ID valido: %admin_id%
echo.
echo Esta seguro de que desea agregar este administrador?
echo ID a agregar: %admin_id%
echo.
set /p "confirm=Confirmar (s/n): "

if /i not "%confirm%"=="s" (
    echo Operacion cancelada.
    echo.
    pause
    goto main_menu
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
echo             new_ids = current_ids + ', %admin_id%' >> temp_update.py
echo         else: >> temp_update.py
echo             new_ids = '%admin_id%' >> temp_update.py
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
set "python_exit=%errorlevel%"

:: Leer resultado
set "result="
for /f "tokens=*" %%i in (temp_result.txt) do set "result=%%i"

if "%python_exit%"=="0" (
    echo !result! | findstr "SUCCESS" >nul
    if !errorlevel! equ 0 (
        echo.
        echo EXITO: Administrador %admin_id% agregado correctamente!
        echo.
        echo Configuracion actualizada:
        findstr "ADMIN_IDS" "%CONFIG_FILE%"
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
if /i "%continue%"=="s" goto add_admin
goto main_menu

:show_admins
cls
echo.
echo ===============================================
echo           ADMINISTRADORES ACTUALES
echo ===============================================
echo.

:: Extraer administradores
for /f "tokens=*" %%i in ('findstr "ADMIN_IDS" "%CONFIG_FILE%"') do (
    set "admin_line=%%i"
)

:: Extraer IDs entre corchetes
set "admin_ids="
for /f "tokens=2 delims=[]" %%a in ("!admin_line!") do set "admin_ids=%%a"

if "!admin_ids!"=="" (
    echo No hay administradores configurados actualmente.
    echo.
    echo Use la opcion 1 para agregar el primer administrador.
) else (
    echo Administradores encontrados:
    echo.
    
    set "count=1"
    for %%a in (!admin_ids!) do (
        set "id=%%a"
        set "id=!id:,=!"
        set "id=!id: =!"
        if not "!id!"=="" (
            echo    !count!. ID: !id!
            set /a count+=1
        )
    )
    
    set /a total=!count!-1
    echo.
    echo Total de administradores: !total!
)

echo.
echo ===============================================
echo.
pause
goto main_menu

:show_info
cls
echo.
echo ===============================================
echo           INFORMACION DEL SISTEMA
echo ===============================================
echo.

echo Archivo de configuracion: %CONFIG_FILE%

if exist "%CONFIG_FILE%" (
    echo Estado: Encontrado
    for %%F in ("%CONFIG_FILE%") do (
        echo Tamaño: %%~zF bytes
        echo Ultima modificacion: %%~tF
    )
) else (
    echo Estado: No encontrado
)

echo.
echo Python:
python --version 2>nul || echo No encontrado

echo Sistema: %OS%
echo Usuario: %USERNAME%
echo Directorio actual: %CD%

echo.
echo ===============================================
echo.
pause
goto main_menu

:exit_script
cls
echo.
echo Gracias por usar el gestor de administradores!
echo Bot ONTV - Hasta la vista
echo.
exit /b 0