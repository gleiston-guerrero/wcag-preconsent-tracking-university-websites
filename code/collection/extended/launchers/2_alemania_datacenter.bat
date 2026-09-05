@echo off
REM ===================================================================
REM  ALEMANIA (centro de datos)
REM  Conecte la VPN a ALEMANIA, servidor de centro de datos (Frankfurt).
REM ===================================================================
echo.
echo  ANTES DE CONTINUAR: Conecte la VPN a ALEMANIA, servidor de centro de datos (Frankfurt).
echo.
pause

node auditar_multipunto.js --vantage=EU --run=1 --red=centro_datos --ciudad=Frankfurt
if errorlevel 2 goto abortada

node auditar_multipunto.js --vantage=EU --run=2 --red=centro_datos --ciudad=Frankfurt
if errorlevel 2 goto abortada

node auditar_multipunto.js --vantage=EU --run=3 --red=centro_datos --ciudad=Frankfurt
if errorlevel 2 goto abortada

echo.
echo  Las tres pasadas de ALEMANIA (centro de datos) han terminado correctamente.
goto fin

:abortada
echo.
echo  *** PASADA ABORTADA: la VPN se cayo o cambio de pais. ***
echo  Reconecte la VPN al pais correcto, BORRE los archivos de la pasada
echo  abortada (resultados_*.json, resultados_*.csv, meta_*.json) y vuelva
echo  a ejecutar este mismo archivo.

:fin
echo.
pause
