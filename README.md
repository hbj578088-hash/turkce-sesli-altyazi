# Türkçe Sesli Altyazı

Video + ASS/SRT altyazı + Türkçe sesli okuma için ücretsiz yerel araç.

## Özellikler

- ASS/SRT altyazı yükleme
- Zaman damgalarını koruyarak Türkçeye çeviri
- Video zamanı gelince altyazı satırını otomatik okutma
- Ücretsiz Türkçe Edge neural sesleri:
  - Emel Neural - kadın
  - Ahmet Neural - erkek
- Tarayıcı/Windows TTS yedek modu
- Tamamen yerel HTML arayüzü

> Not: Çeviri ve Edge-TTS internet bağlantısı kullanabilir. Video ve altyazı dosyaları tarayıcıda yerel kalır.

## Kurulum

Python 3.11 önerilir.

```bash
pip install -r requirements.txt
python edge_tts_server.py
```

Windows için:

```bat
Kanka-EdgeTTS-Baslat.bat
```

Sonra `index.html` dosyasını Edge/Chrome ile aç.

## Kullanım

1. `edge_tts_server.py` sunucusunu başlat.
2. `index.html` dosyasını aç.
3. `Zamanlı Çeviri` sekmesinde orijinal `.ass` veya `.srt` altyazıyı Türkçeye çevir.
4. `Video okutucuya aktar` butonuna bas.
5. Video dosyasını yükle.
6. `Video ile senkron okut` butonuna bas.

## Önemli

Düz metin çevirisi video senkron için yeterli değildir; zaman damgası kaybolur. Senkron okuma için `.ass` veya `.srt` altyazı kullan.

