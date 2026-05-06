@echo off
echo ============================================
echo   Crypto Protector - Installation
echo ============================================
echo.

echo [1/3] Verification de Python...
python --version
if %errorlevel% neq 0 (
    echo ERREUR: Python n'est pas installe!
    echo Telechargez Python sur https://www.python.org/
    pause
    exit /b 1
)

echo.
echo [2/3] Installation des dependances...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ERREUR: L'installation des dependances a echoue!
    pause
    exit /b 1
)

echo.
echo [3/3] Creation des fichiers de configuration...
if not exist config.json (
    echo Configuration par defaut creee
)

echo.
echo ============================================
echo   Installation terminee avec succes!
echo ============================================
echo.
echo Pour lancer le programme:
echo   python launcher.py
echo.
pause
