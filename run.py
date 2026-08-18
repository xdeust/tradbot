"""
Tradbot Pro - Başlatıcı Script
Kullanım: python run.py
"""

import os
import sys
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"\n=======================================================")
    print(f"🚀 TRADBOT PRO | FINTECH TERMINAL BAŞLATILIYOR...")
    print(f"📡 Sunucu Adresi: http://localhost:{port}")
    print(f"📖 API Dokümantasyonu: http://localhost:{port}/docs")
    print(f"=======================================================\n")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
