@echo off
REM ===================================================================
REM  REINO UNIDO (centro de datos)
REM  Conecte la VPN al REINO UNIDO (Londres).
REM ===================================================================
echo.
echo  ANTES DE CONTINUAR: Conecte la VPN al REINO UNIDO (Londres).
echo.
pause

node audit_multivantage.js --vantage=GB --run=1 --red=centro_datos --ciudad=Londres
if errorlevel 2 goto abortada

node audit_multivantage.js --vantage=GB --run=2 --red=centro_datos --ciudad=Londres
if errorlevel 2 goto abortada

node audit_multivantage.js --vantage=GB --run=3 --red=centro_datos --ciudad=Londres
if errorlevel 2 goto abortada

echo.
echo  Las tres pasadas de REINO UNIDO (centro de datos) han terminado correctamente.
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
