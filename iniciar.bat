@echo off
REM Script para Iniciar Livro Caixa da Igreja
REM Verifica dependências, inicia o banco e a aplicação

cls
echo.
echo ========================================
echo   LIVRO CAIXA DA IGREJA
echo   Sistema de Gestão Financeira
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python não encontrado!
    echo Instale Python 3.8+ em https://www.python.org/
    echo.
    pause
    exit /b 1
)

echo ✓ Python encontrado
echo.

REM Verificar se banco de dados existe
if not exist "livro_caixa.db" (
    echo 📝 Inicializando banco de dados...
    python init.py
    if %errorlevel% neq 0 (
        echo ERRO ao inicializar banco!
        pause
        exit /b 1
    )
    echo ✓ Banco de dados criado
    echo.
) else (
    echo ✓ Banco de dados já existe
    echo.
)

REM Verificar dependências
echo 📦 Verificando dependências...
pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚙️  Instalando Streamlit...
    pip install -q streamlit pandas plotly
    if %errorlevel% neq 0 (
        echo ERRO ao instalar dependências!
        pause
        exit /b 1
    )
    echo ✓ Dependências instaladas
) else (
    echo ✓ Dependências já instaladas
)

echo.
echo ========================================
echo   INICIANDO APLICAÇÃO
echo ========================================
echo.
echo 🚀 Abrindo em http://localhost:8501
echo.
echo ⏰ Aguarde alguns segundos...
echo.
echo 💡 Para parar a aplicação, pressione CTRL+C
echo.
timeout /t 2 >nul

REM Iniciar a aplicação
streamlit run app.py

pause
