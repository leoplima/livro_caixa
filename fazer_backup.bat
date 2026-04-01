@echo off
REM Script de Backup do Livro Caixa da Igreja
REM Cria uma cópia do banco de dados com data/hora

setlocal enabledelayedexpansion

REM Obter data e hora
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)

REM Paths
set SOURCE=livro_caixa.db
set BACKUP_DIR=backups
set BACKUP_FILE=%BACKUP_DIR%\livro_caixa_backup_%mydate%_%mytime%.db

REM Criar pasta de backups se não existir
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

REM Copiar arquivo
if exist "%SOURCE%" (
    copy "%SOURCE%" "%BACKUP_FILE%"
    echo.
    echo ========================================
    echo    BACKUP REALIZADO COM SUCESSO!
    echo ========================================
    echo Arquivo: %BACKUP_FILE%
    echo Data: %mydate% %mytime%
    echo.
    echo Dica: Mantenha cópias em local seguro!
    echo ========================================
    pause
) else (
    echo.
    echo ERRO: Arquivo %SOURCE% não encontrado!
    echo Certifique-se de estar no diretório correto.
    echo.
    pause
)
