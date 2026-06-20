import asyncio
import tempfile
from pathlib import Path

import edge_tts
from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI(title="Kanka Edge Turkish Neural TTS")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEFAULT_VOICE = "tr-TR-EmelNeural"

@app.get("/health")
def health():
    return {"ok": True, "engine": "edge-tts", "voice": DEFAULT_VOICE, "note": "not voice cloning; high quality Turkish neural voices"}

@app.get("/voices")
async def voices():
    all_voices = await edge_tts.list_voices()
    tr = [v for v in all_voices if str(v.get("Locale", "")).lower().startswith("tr")]
    return {"voices": tr}

@app.post("/translate")
def translate(
    text: str = Form(...),
    source: str = Form("auto"),
    target: str = Form("tr"),
):
    text = (text or "").strip()
    if not text:
        raise HTTPException(400, "empty text")
    try:
        detected = source
        if source == "auto":
            try:
                detected = detect(text[:2000])
            except LangDetectException:
                detected = "auto"
        # GoogleTranslator has request-size limits; split long subtitles safely.
        chunks = []
        current = ""
        max_chunk = 2800
        for para in text.split("\n"):
            if len(para) > max_chunk:
                if current:
                    chunks.append(current)
                    current = ""
                for i in range(0, len(para), max_chunk):
                    chunks.append(para[i:i+max_chunk])
                continue
            if len(current) + len(para) + 1 > max_chunk:
                chunks.append(current)
                current = para
            else:
                current = para if not current else current + "\n" + para
        if current:
            chunks.append(current)
        translator = GoogleTranslator(source="auto" if source == "auto" else source, target=target or "tr")
        translated_parts = []
        total = len(chunks)
        for idx, c in enumerate(chunks, 1):
            if c.strip():
                translated_parts.append(translator.translate(c))
            else:
                translated_parts.append(c)
        return {"ok": True, "source": detected, "target": target or "tr", "chunks": total, "translated": "\n".join(translated_parts)}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/tts")
async def tts(
    text: str = Form(...),
    voice: str = Form(DEFAULT_VOICE),
    rate: str = Form("+0%"),
    pitch: str = Form("+0Hz"),
):
    text = (text or "").strip()
    if not text:
        raise HTTPException(400, "empty text")
    if len(text) > 1000:
        text = text[:1000]
    out = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    out.close()
    try:
        communicate = edge_tts.Communicate(text=text, voice=voice or DEFAULT_VOICE, rate=rate or "+0%", pitch=pitch or "+0Hz")
        await communicate.save(out.name)
        return FileResponse(out.name, media_type="audio/mpeg", filename="kanka_edge_tts.mp3")
    except Exception as e:
        raise HTTPException(500, str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=7866)
