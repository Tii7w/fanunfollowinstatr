@echo off
chcp 65001 >nul
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo Python bulunamadı.
    echo https://www.python.org/downloads/ adresinden Python 3.10 veya üstünü kur.
    echo Kurulumda "Add python.exe to PATH" kutusunu işaretlemeyi unutma.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Sanal ortam oluşturuluyor...
    python -m venv .venv
)

echo Gerekli paketler kuruluyor...
".venv\Scripts\python.exe" -m pip install --upgrade pip >nul
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo Paket kurulumu başarısız oldu.
    pause
    exit /b 1
)

if not exist ".env" (
    copy ".env.example" ".env" >nul
    echo .env dosyası oluşturuldu.
)

echo.
echo Kurulum tamam.
echo 1^) .env dosyasını aç, kullanıcı adını ve şifreni yaz.
echo 2^) baslat.bat ile programı başlat.
pause
