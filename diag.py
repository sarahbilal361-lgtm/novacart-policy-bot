"""Finds out which part of the bot is slow. Run: python diag.py"""
import os, time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(timeout=30_000),   # 30 s per test
)

import bot  # reuses POLICIES, SYSTEM, TOOLS from your bot.py

def run(label, **kw):
    print(f"\n--- {label} ---", flush=True)
    t = time.time()
    try:
        r = client.models.generate_content(model=MODEL, **kw)
        print(f"OK in {time.time()-t:.1f}s: {(r.text or '')[:150]!r}", flush=True)
    except Exception as e:
        print(f"FAILED after {time.time()-t:.1f}s: {type(e).__name__}: {str(e)[:200]}", flush=True)

print("Model:", MODEL, flush=True)
q = "Do you ship to Canada?"
run("A: tiny question, no policies, no tools", contents="Say hello in 3 words")
run("B: policies, no tools",
    contents=f"POLICY FILES:\n{bot.POLICIES}\n\nCUSTOMER QUESTION:\n{q}",
    config=types.GenerateContentConfig(system_instruction=bot.SYSTEM, temperature=0))
run("C: policies + calculator tools",
    contents=f"POLICY FILES:\n{bot.POLICIES}\n\nCUSTOMER QUESTION:\n{q}",
    config=types.GenerateContentConfig(system_instruction=bot.SYSTEM, temperature=0, tools=bot.TOOLS))
print("\nDone.")
