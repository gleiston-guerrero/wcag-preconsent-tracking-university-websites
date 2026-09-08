@echo off
REM ===================================================================
REM  SUIZA (centro de datos)
REM  Conecte la VPN a SUIZA (Zurich o Ginebra).
REM ===================================================================
echo.
echo  ANTES DE CONTINUAR: Conecte la VPN a SUIZA (Zurich o Ginebra).
echo.
pause

node audit_multivantage.js --vantage=CH --run=1 --red=centro_datos --ciudad=Zurich
if errorlevel 2 goto abortada

node audit_multivantage.js --vantage=CH --run=2 --red=centro_datos --ciudad=Zurich
if errorlevel 2 goto abortada

node audit_multivantage.js --vantage=CH --run=3 --red=centro_datos --ciudad=Zurich
if errorlevel 2 goto abortada

echo.
echo  Las tres pasadas de SUIZA (centro de datos) han terminado correctamente.
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
