@echo off
REM ===================================================================
REM  ESTADOS UNIDOS (centro de datos)
REM  Conecte la VPN a ESTADOS UNIDOS (Miami).
REM ===================================================================
echo.
echo  ANTES DE CONTINUAR: Conecte la VPN a ESTADOS UNIDOS (Miami).
echo.
pause

node auditar_multipunto.js --vantage=US --run=1 --red=centro_datos --ciudad=Miami
if errorlevel 2 goto abortada

node auditar_multipunto.js --vantage=US --run=2 --red=centro_datos --ciudad=Miami
if errorlevel 2 goto abortada

node auditar_multipunto.js --vantage=US --run=3 --red=centro_datos --ciudad=Miami
if errorlevel 2 goto abortada

echo.
echo  Las tres pasadas de ESTADOS UNIDOS (centro de datos) han terminado correctamente.
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
