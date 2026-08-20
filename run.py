import os
import sys

# Proje ana dizinini Python path'ine ekle
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

# Render/Linux uyumlulugu: __init__.py dosyalarini otomatik olustur
# GitHub web upload bazen bos dosyalari atliyor
for pkg_dir in ["core", "engines"]:
    pkg_path = os.path.join(CURRENT_DIR, pkg_dir)
    init_file = os.path.join(pkg_path, "__init__.py")
    if os.path.isdir(pkg_path) and not os.path.exists(init_file):
        with open(init_file, "w") as f:
            f.write(f"# {pkg_dir} package\n")
        print(f"[STARTUP] Created missing {pkg_dir}/__init__.py")

import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"\n=======================================================")
    print(f"TRADBOT PRO | FINTECH TERMINAL BASLATILIYOR...")
    print(f"Sunucu Adresi: http://0.0.0.0:{port}")
    print(f"API Dokumantasyonu: http://0.0.0.0:{port}/docs")
    print(f"=======================================================\n")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
