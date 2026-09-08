@echo off
REM ===================================================================
REM  ALEMANIA (residencial)
REM  Conecte la VPN a ALEMANIA con salida RESIDENCIAL (IP domestica).
REM ===================================================================
echo.
echo  ANTES DE CONTINUAR: Conecte la VPN a ALEMANIA con salida RESIDENCIAL (IP domestica).
echo.
pause

node audit_multivantage.js --vantage=EU --run=4 --red=residencial --ciudad=Berlin
if errorlevel 2 goto abortada

node audit_multivantage.js --vantage=EU --run=5 --red=residencial --ciudad=Berlin
if errorlevel 2 goto abortada

node audit_multivantage.js --vantage=EU --run=6 --red=residencial --ciudad=Berlin
if errorlevel 2 goto abortada

echo.
echo  Las tres pasadas de ALEMANIA (residencial) han terminado correctamente.
goto fin

:abortada
echo.
echo  *** PASADA ABORTADA: la VPN se cayo o cambio de pais. ***
echo  Reconecte la VPN al pais correcto, BORRE los archivos de la pasada
echo  abortada (results_*.json, results_*.csv, meta_*.json) y vuelva
echo  a run este mismo archivo.

:fin
echo.
pause
