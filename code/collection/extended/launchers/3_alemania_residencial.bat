@echo off
REM ===================================================================
REM  ALEMANIA (residencial)
REM  Conecte la VPN a ALEMANIA con salida RESIDENCIAL (IP domestica).
REM ===================================================================
echo.
echo  ANTES DE CONTINUAR: Conecte la VPN a ALEMANIA con salida RESIDENCIAL (IP domestica).
echo.
pause

node auditar_multipunto.js --vantage=EU --run=4 --red=residencial --ciudad=Berlin
if errorlevel 2 goto abortada

node auditar_multipunto.js --vantage=EU --run=5 --red=residencial --ciudad=Berlin
if errorlevel 2 goto abortada

node auditar_multipunto.js --vantage=EU --run=6 --red=residencial --ciudad=Berlin
if errorlevel 2 goto abortada

echo.
echo  Las tres pasadas de ALEMANIA (residencial) han terminado correctamente.
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
