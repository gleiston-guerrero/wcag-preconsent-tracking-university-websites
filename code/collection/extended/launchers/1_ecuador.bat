@echo off
REM ===================================================================
REM  ECUADOR (residencial)
REM  DESCONECTE la VPN. Debe medirse desde su conexion domestica en Ecuador.
REM ===================================================================
echo.
echo  ANTES DE CONTINUAR: DESCONECTE la VPN. Debe medirse desde su conexion domestica en Ecuador.
echo.
pause

node audit_multivantage.js --vantage=EC --run=1 --red=residencial --ciudad=Cuenca
if errorlevel 2 goto abortada

node audit_multivantage.js --vantage=EC --run=2 --red=residencial --ciudad=Cuenca
if errorlevel 2 goto abortada

node audit_multivantage.js --vantage=EC --run=3 --red=residencial --ciudad=Cuenca
if errorlevel 2 goto abortada

echo.
echo  Las tres pasadas de ECUADOR (residencial) han terminado correctamente.
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
