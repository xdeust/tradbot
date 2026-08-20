import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"\n=======================================================")
    print(f"TRADBOT PRO | FINTECH TERMINAL BASLATILIYOR...")
    print(f"Sunucu Adresi: http://0.0.0.0:{port}")
    print(f"API Dokumantasyonu: http://0.0.0.0:{port}/docs")
    print(f"=======================================================\n")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
