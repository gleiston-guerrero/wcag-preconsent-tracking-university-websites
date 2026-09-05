@echo off
REM ===========================================================================
REM  Lanzador de la auditoria multipunto — version 2
REM  Pregunta el punto de observacion y CUANTAS pasadas faltan por hacer,
REM  y las ejecuta en cadena numerandolas automaticamente.
REM ===========================================================================
setlocal enabledelayedexpansion
cd /d "%~dp0"
color 07
cls

echo ===========================================================================
echo   AUDITORIA MULTIPUNTO — lanzador
echo   Carpeta: %CD%
echo ===========================================================================
echo.

REM --------------------------------------------------------------- requisitos
where node >nul 2>&1
if errorlevel 1 (
	echo   ERROR: no se encuentra Node.js. Ejecute primero INSTALAR.bat
	echo.
	pause
	exit /b 1
)
if not exist "auditar_multipunto.js" (
	echo   ERROR: falta auditar_multipunto.js en esta carpeta.
	echo.
	pause
	exit /b 1
)
if not exist "universidades.json" (
	echo   ERROR: falta universidades.json en esta carpeta.
	echo.
	pause
	exit /b 1
)
if not exist "node_modules\playwright" (
	echo   ERROR: faltan las dependencias. Ejecute primero INSTALAR.bat
	echo.
	pause
	exit /b 1
)

REM ------------------------------------------------- punto de observacion
echo   Puntos de observacion:
echo.
echo      EC   Ecuador          — la VPN debe estar APAGADA
echo      EU   Union Europea    — VPN conectada a un pais de la UE
echo      US   Estados Unidos   — VPN conectada a EE.UU.
echo      GB   Reino Unido      — VPN conectada al REINO UNIDO
echo.
set "VANTAGE="
set /p VANTAGE="  Escriba el punto y pulse Entrar: "
set "VANTAGE=%VANTAGE: =%"
if /i "%VANTAGE%"=="EC" goto :vok
if /i "%VANTAGE%"=="EU" goto :vok
if /i "%VANTAGE%"=="US" goto :vok
if /i "%VANTAGE%"=="GB" goto :vok
echo.
echo   ERROR: valor no valido. Solo se admite EC, EU, US o GB.
echo.
pause
exit /b 1
:vok
REM normalizar a mayusculas
if /i "%VANTAGE%"=="ec" set "VANTAGE=EC"
if /i "%VANTAGE%"=="eu" set "VANTAGE=EU"
if /i "%VANTAGE%"=="us" set "VANTAGE=US"
if /i "%VANTAGE%"=="gb" set "VANTAGE=GB"

REM ------------------------------------------- que pasadas existen ya
set "YA="
set /a NYA=0
for /L %%N in (1,1,20) do (
	if exist "resultados_%VANTAGE%_r%%N.json" (
		set "YA=!YA! %%N"
		set /a NYA+=1
	)
)

echo.
echo ---------------------------------------------------------------------------
if %NYA% EQU 0 (
	echo   Para el punto %VANTAGE% no hay ninguna pasada hecha todavia.
) else (
	echo   Para el punto %VANTAGE% ya existen !NYA! pasada^(s^):!YA!
)
echo ---------------------------------------------------------------------------
echo.

REM --------------------------------------------- cuantas pasadas nuevas
set "CUANTAS="
set /p CUANTAS="  Cuantas pasadas NUEVAS quiere ejecutar ahora: "
set "CUANTAS=%CUANTAS: =%"
echo %CUANTAS%| findstr /r "^[1-9][0-9]*$" >nul
if errorlevel 1 (
	echo.
	echo   ERROR: escriba un numero entero mayor que cero.
	echo.
	pause
	exit /b 1
)
if %CUANTAS% GTR 10 (
	echo.
	echo   ERROR: maximo 10 pasadas de una vez.
	echo.
	pause
	exit /b 1
)

REM ----------------------------------- elegir los numeros de pasada libres
set "PENDIENTES="
set /a CUENTA=0
for /L %%N in (1,1,20) do (
	if !CUENTA! LSS %CUANTAS% (
		if not exist "resultados_%VANTAGE%_r%%N.json" (
			set "PENDIENTES=!PENDIENTES! %%N"
			set /a CUENTA+=1
		)
	)
)

set /a MINUTOS=%CUANTAS%*40
echo.
echo ===========================================================================
echo   Se van a ejecutar estas pasadas del punto %VANTAGE%:!PENDIENTES!
echo   Duracion aproximada total: %MINUTOS% minutos.
echo ===========================================================================
echo.
if /i "%VANTAGE%"=="EC" (
	echo   COMPRUEBE AHORA: la VPN debe estar APAGADA.
) else (
	echo   COMPRUEBE AHORA: la VPN conectada al pais correcto,
	echo   y su bloqueador de rastreadores DESACTIVADO.
	echo   Abra https://ipinfo.io/json y confirme el pais.
)
echo.
echo   Durante la ejecucion NO use el equipo. Las pasadas se encadenan solas.
echo.
pause

set /a HECHAS=0
for %%N in (!PENDIENTES!) do (
	set /a HECHAS+=1
	echo.
	echo ===========================================================================
	echo   PASADA !HECHAS! de %CUANTAS%   —   punto %VANTAGE%, numero de pasada %%N
	echo ===========================================================================
	echo.
	node auditar_multipunto.js --vantage=%VANTAGE% --run=%%N
	if errorlevel 2 (
		echo.
		echo   *** LA PASADA %%N SE ABORTO: la VPN cambio de pais o se cayo. ***
		echo   Se detiene la cadena. Reconecte la VPN, borre los archivos
		echo   resultados_%VANTAGE%_r%%N.* y meta_%VANTAGE%_r%%N.json,
		echo   y vuelva a lanzar este archivo.
		echo.
		pause
		exit /b 2
	)
	if errorlevel 1 (
		echo.
		echo   *** ERROR en la pasada %%N. Se detiene la cadena. ***
		echo.
		pause
		exit /b 1
	)
	if !HECHAS! LSS %CUANTAS% (
		echo.
		echo   Pausa de 60 segundos antes de la siguiente pasada...
		timeout /t 60 /nobreak >nul
	)
)

echo.
echo ===========================================================================
echo   TERMINADO: %CUANTAS% pasada^(s^) del punto %VANTAGE%
echo ===========================================================================
echo.
echo   Anote en la hoja de registro la fecha, la hora y el servidor de VPN.
echo.
echo   Revise que los archivos meta_%VANTAGE%_r*.json digan
echo   "coincide_con_vantage": true
echo.
echo   Cuando tenga los tres puntos, ejecute el analisis:
echo       python analizar_multipunto.py
echo.
echo   MIRE LA SECCION 1b DEL INFORME. Si algun punto aparece como
echo   SOSPECHOSO, ese nodo de VPN perdio contenido y hay que repetirlo
echo   desde otro servidor antes de usar los resultados.
echo.
pause
endlocal
