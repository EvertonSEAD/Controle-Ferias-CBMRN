@echo off
title Controle de Ferias - CBMRN
cls

REM Muda para a pasta onde este script esta localizado
cd /d "%~dp0"

REM Define codificacao UTF-8 para o Python
set PYTHONIOENCODING=utf-8

echo ======================================================================
echo           CONTROLE DE FERIAS - CBMRN (Corpo de Bombeiros RN)
echo ======================================================================
echo.
echo [*] Iniciando servidor do sistema...
echo.

REM Abre o navegador padrao no endereco local
start "" "http://localhost:5000"

REM Executa a aplicacao em Python
python app.py

pause
