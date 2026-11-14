"""Lists the Gemini models your key can use and times a tiny request on each.
Run: python pick_model.py"""
import os, time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(timeout=20_000),   # 20 s per model
)

SKIP = ("image", "tts", "live", "audio", "embedding", "robotics", "computer",
        "veo", "imagen", "aqa", "learnlm", "gemma", "native", "preview-")
names = []
try:
    for m in client.models.list():
        name = m.name.replace("models/", "")
        actions = getattr(m, "supported_actions", None) or []
        if "generateContent" not in actions and actions:
            continue
        low = name.lower()
        if "gemini" in low and ("flash" in low or "lite" in low) and not any(s in low for s in SKIP):
            names.append(name)
except Exception as e:
    print("Could not list models:", type(e).__name__, str(e)[:200])

names = sorted(set(names))
print("Flash-type models found:", names, flush=True)

results = []
for name in names[:8]:
    t = time.time()
    try:
        r = client.models.generate_content(model=name, contents="Say hello in 3 words")
        dt = time.time() - t
        print(f"OK     {name}: {dt:.1f}s -> {(r.text or '').strip()[:40]!r}", flush=True)
        results.append((dt, name))
    except Exception as e:
        print(f"FAILED {name}: {time.time()-t:.1f}s {type(e).__name__} {str(e)[:90]}", flush=True)

results.sort()
print("\nFASTEST WORKING:", [n for _, n in results[:3]] or "none")
print("Put one in .env as GEMINI_MODEL=<name>")
