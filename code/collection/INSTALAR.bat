@echo off
REM ===========================================================================
REM  INSTALADOR — deja el equipo listo para ejecutar la auditoria multipunto
REM  Doble clic sobre este archivo. Se ejecuta UNA SOLA VEZ.
REM ===========================================================================
setlocal
cd /d "%~dp0"
cls

echo ===========================================================================
echo   INSTALACION DE LA AUDITORIA MULTIPUNTO
echo   Carpeta: %CD%
echo ===========================================================================
echo.

REM --- 1. Node.js -------------------------------------------------------------
echo [1/5] Comprobando Node.js...
where node >nul 2>&1
if errorlevel 1 (
	echo.
	echo       Node.js NO esta instalado. Intentando instalarlo...
	winget install --id OpenJS.NodeJS.LTS -e --accept-source-agreements --accept-package-agreements
	echo.
	echo   ======================================================================
	echo     IMPORTANTE: cierre esta ventana y vuelva a hacer doble clic en
	echo     INSTALAR.bat. Windows necesita reabrir la ventana para encontrar
	echo     el programa recien instalado.
	echo   ======================================================================
	echo.
	pause
	exit /b 0
)
for /f "delims=" %%v in ('node --version') do echo       Node.js %%v  OK

REM --- 2. Python --------------------------------------------------------------
echo [2/5] Comprobando Python...
where python >nul 2>&1
if errorlevel 1 (
	echo.
	echo       Python NO esta instalado. Intentando instalarlo...
	winget install --id Python.Python.3.12 -e --accept-source-agreements --accept-package-agreements
	echo.
	echo   ======================================================================
	echo     IMPORTANTE: cierre esta ventana y vuelva a hacer doble clic en
	echo     INSTALAR.bat.
	echo   ======================================================================
	echo.
	pause
	exit /b 0
)
for /f "delims=" %%v in ('python --version') do echo       %%v  OK

REM --- 3. Archivos necesarios -------------------------------------------------
echo [3/5] Comprobando archivos...
if not exist "auditar_multipunto.js" (
	echo.
	echo   ERROR: falta auditar_multipunto.js en esta carpeta.
	echo   Copie aqui TODOS los archivos del paquete y repita.
	echo.
	pause
	exit /b 1
)
echo       auditar_multipunto.js  OK
if not exist "universidades.json" (
	echo.
	echo   AVISO: todavia no esta universidades.json en esta carpeta.
	echo   La instalacion continua, pero no podra medir hasta copiarlo.
	echo.
)

REM --- 4. Dependencias de Node ------------------------------------------------
echo [4/5] Instalando Playwright, axe-core y el navegador...
echo       (esto descarga unos 150 MB, puede tardar varios minutos)
echo.
if not exist "package.json" call npm init -y >nul 2>&1
call npm install playwright axe-core
if errorlevel 1 goto :error_npm
call npx playwright install chromium
if errorlevel 1 goto :error_npm

REM --- 5. Dependencias de Python ----------------------------------------------
echo.
echo [5/5] Instalando scipy y numpy...
python -m pip install --quiet --upgrade pip
python -m pip install --quiet scipy numpy
if errorlevel 1 (
	echo   ERROR instalando scipy/numpy. Ejecute a mano:
	echo       python -m pip install scipy numpy
	pause
	exit /b 1
)

REM --- Ajustes de energia -----------------------------------------------------
echo.
echo Evitando que el equipo se suspenda durante las mediciones...
powercfg /change standby-timeout-ac 0    >nul 2>&1
powercfg /change hibernate-timeout-ac 0  >nul 2>&1
powercfg /change monitor-timeout-ac 0    >nul 2>&1

echo.
echo ===========================================================================
echo   INSTALACION TERMINADA
echo ===========================================================================
echo.
echo   Siguiente paso: prueba piloto con 5 sitios y SIN VPN.
echo   Se lanza ahora mismo si pulsa una tecla; si prefiere no hacerla,
echo   cierre esta ventana.
echo.
pause

if not exist "universidades.json" (
	echo   No se puede hacer la prueba: falta universidades.json
	echo.
	pause
	exit /b 0
)

echo.
node auditar_multipunto.js --vantage=EC --run=0 --limit=5
echo.
echo ---------------------------------------------------------------------------
echo   Si vio lineas que empiezan por OK, todo funciona.
echo   Borre ahora los archivos resultados_EC_r0.* y meta_EC_r0.json:
echo   la pasada 0 es solo un ensayo y no debe entrar en el analisis.
echo ---------------------------------------------------------------------------
echo.
pause
exit /b 0

:error_npm
echo.
echo   ERROR instalando las dependencias de Node.
echo   Causa mas probable: PowerShell bloquea la ejecucion de guiones.
echo   Abra PowerShell COMO ADMINISTRADOR, ejecute esta linea:
echo.
echo       Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
echo.
echo   responda S, cierre PowerShell y vuelva a ejecutar INSTALAR.bat.
echo.
pause
exit /b 1
