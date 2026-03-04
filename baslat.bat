@echo off
title Smart Mailer WebApp Baslatici
echo ==============================================
echo Smart Mailer WebApp Kurulum ve Baslatma
echo ==============================================
echo.

:: Yonetici (Administrator) yetkisi kontrolü
:: Bu kontrol Python kurulumu icin (sistem geneline kurulum ve PATH ekleme) gerekebilir
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [BILGI] Bu script ilk kurulum sirasinda Python indirmek icin Yonetici yetkisine ihtiyac duyabilir.
    echo Eger daha once Python kurmadiysaniz scripti sag tiklayip "Yonetici olarak calistir" secenegiyle acin.
    echo.
)

echo [1/4] Python kurulumu kontrol ediliyor...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [UYARI] Sistemde Python bulunamadi!
    echo Otomatik olarak indirilecek ve kurulacak... Lutfen bekleyin.
    
    :: Gecici bir klasor olustur
    mkdir temp_python_setup >nul 2>&1
    
    :: Python 3.12 indir (Sessiz kurulum icin)
    echo - Python kurulum dosyasi indiriliyor...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe' -OutFile 'temp_python_setup\python_installer.exe'"
    
    :: İndirme basarisizsa
    if not exist "temp_python_setup\python_installer.exe" (
        echo [HATA] Indirme islemi basarisiz oldu! Internet baglantinizi kontrol edin.
        pause
        exit /b
    )
    
    :: Sessiz ve arka planda kurulum (PATH'e ekle)
    echo - Python sisteminize kurutuluyor. Bu islem bir kac dakika surebilir...
    temp_python_setup\python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    
    :: Gecici dosyalari sil
    rmdir /S /Q temp_python_setup
    
    :: Yeni oturuma ihtiyac duyulacagi icin CMD'de PATH degiskenini yeniden yukle veya kullaniciyi uyar
    echo.
    echo [BASARILI] Python kurulumu tamamlandi! 
    echo Sistem degisikliklerinin algilanmasi icin lutfen bu pencereyi KAPATIP TEKRAR ACIN!
    pause
    exit /b
)
echo Python yuklu, devam ediliyor...
echo.

echo [2/4] Sanal ortam (venv) kontrol ediliyor...
if not exist "venv\Scripts\activate.bat" (
    echo Sanal ortam bulunamadi. Ilk kullanim icin otomatik olusturuluyor...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [HATA] Sanal ortam olusturulamadi! Lutfen internet baglantinizi veya izinlerinizi kontrol edin.
        pause
        exit /b
    )
    echo Sanal ortam basariyla olusturuldu.
) else (
    echo Sanal ortam hazir.
)
echo.

echo [3/4] Gereksinimler denetleniyor ve kuruluyor...
call .\venv\Scripts\activate.bat
echo Pip guncelleniyor (varsa) biraz zaman alabilir...
python -m pip install --upgrade pip >nul 2>&1
echo Kutuphaneler kuruluyor... (Zaten kurulu olanlar hizlica gecilecektir)
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [HATA] Kutuphaneler kurulurken bir sorun olustu! Lutfen internet baglantinizi kontrol edip tekrar deneyin.
    echo Veya baslat.bat i Yonetici modunda acmayi deneyin.
    pause
    exit /b
)
echo Tum gereksinimler eksiksiz.
echo.

echo [4/4] Uygulama baslatiliyor...
echo Arka planda tarayici 3 saniye icinde acilacak... 
echo.
echo =======================================================
echo DIKKAT: SUNUCU ACIK KALDIGI SURECE BU PENCEREYI KAPATMAYIN!
echo Uygulamayi durdurmak istediginizde bu pencereyi kapatabilirsiniz.
echo =======================================================
echo.

:: Tarayıcıyı arka planda gecikmeli olarak aç
start "" cmd /c "timeout /t 3 >nul && start http://localhost:8000"

:: Uygulamayı çalıştır
python app.py

pause
