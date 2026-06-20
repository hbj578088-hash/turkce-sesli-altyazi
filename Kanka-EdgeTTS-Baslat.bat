@echo off
setlocal
title Kanka Edge TTS Baslat
set "ROOT=%USERPROFILE%\Downloads\Kanka-XTTS"
set "VENV=%ROOT%\.venv"
cd /d "%ROOT%"
if not exist "%VENV%\Scripts\activate.bat" (
  echo [HATA] Kurulum bulunamadi. Once Kanka-XTTS-Kurulum.bat calistir.
  pause
  exit /b 1
)
call "%VENV%\Scripts\activate.bat"
echo [Kanka] Edge Turkish Neural TTS sunucusu basliyor: http://127.0.0.1:7866
echo [Not] Bu ses klonlama degil; kaliteli ucretsiz Turkce neural sestir.
python edge_tts_server.py
pause
