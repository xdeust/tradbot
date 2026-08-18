# 🚀 TRADBOT PRO | FINTECH TERMINAL

Borsa İstanbul (BIST) hisseleri, Tavan Radarı, 1 Saatlik Swing & Momentum filtreleri, Aracı Kurum Dağılımı (AKD) Simülasyonu, 4 Ajanlı Otonom Yapay Zeka Komitesi ve Black-Scholes Greeks Varant Simülatörünü bir arada sunan profesyonel finans terminali.

---

## 🌟 Özellikler ve Modüller

1. **🚀 Tavan Radarı (Pro Radar):**
   - Anti-Trap Kalkanı (VWAP üzeri kurumsal alım teyidi).
   - AR-GE Laboratuvarı ve Hacim Şiddeti ölçümü.
2. **📊 1 Saatlik Swing & UZAK DUR Taraması:**
   - 5/5 Puanlama kuralı (EMA, MACD, RSI, ADX, Momentum).
   - Sert düşüş ve bozulma uyarıları.
3. **🏦 Simüle AKD & Smart Money (Emir Akışı):**
   - Bank of America, İş Yatırım, Yapı Kredi, Garanti BBVA vb. kurumların alış/satış dağılımı.
   - 3 Temel Kanıt ve 4 Adımlı Taktik İşlem Planı.
4. **🤖 Otonom Yapay Zeka Komitesi:**
   - Trend AI, Momentum AI, Quant AI ve Sentiment AI modelleriyle oylama ve CIO NLP Yönetici Özeti.
5. **🎯 Trade Desk (Operasyon Masası):**
   - ATR tabanlı Giriş (Entry), Kâr Al (TP1/TP2), Zarar Kes (Stop-Loss) ve Destek/Direnç Seviyeleri.
6. **⚡ Altın Varant & Greeks Simülatörü:**
   - Black-Scholes Modeli (Delta, Gamma, Theta zaman erimesi, Vega, Gearing kaldıraç, Başabaş).
   - İş Yatırım, Ak Yatırım, Garanti BBVA ve Ahlatcı Yatırım ihraççı simülasyonları.
7. **📈 Canlı Grafik Motoru:**
   - TradingView Lightweight Charts & ApexCharts entegrasyonu.
8. **🏆 Şeffaf KPI & Simülasyon Motoru:**
   - Sinyal başarı karnesi, kâr/zarar eğrisi (Equity Curve) ve canlı simülasyon emirleri.

---

## 💻 Yerel Kurulum ve Çalıştırma

### 1. Gereksinimleri Yükleyin
```bash
pip install -r requirements.txt
```

### 2. Uygulamayı Başlatın
```bash
python run.py
```
*(Windows kullanıcıları doğrudan `start_tradbot.bat` dosyasına çift tıklayarak da başlatabilir.)*

### 3. Tarayıcınızda Açın
* **Terminal Arayüzü:** [http://localhost:8000](http://localhost:8000)
* **Swagger API Dokümantasyonu:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ☁️ Render.com Üzerine Ücretsiz Canlıya Alma (Deploy)

1. Bu projeyi **GitHub** deponuza yükleyin (Push edin).
2. [Render.com](https://render.com) adresine gidin ve **New Web Service** butonuna tıklayın.
3. GitHub deponuzu bağlayın.
4. Render ayarlarında:
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python run.py`
5. **Deploy Web Service** butonuna tıklayın. Birkaç dakika içinde siteniz `https://tradbot-pro.onrender.com` gibi canlı bir adreste yayına girecektir!

---

## 📁 Proje Klasör Mimarisi

```
tradbot/
├── core/
│   ├── symbols.py          # BIST & Varant sembol havuzu ve arama
│   └── cache_manager.py    # RAM önbellek ve asenkron tarayıcı
├── engines/
│   ├── market_data.py      # Yahoo Finance BIST veri çekici
│   ├── indicators.py       # EMA, RSI, MACD, ADX, SuperTrend, VWAP
│   ├── radar_engine.py     # Tavan radarı & Swing tarama motoru
│   ├── varant_engine.py    # Black-Scholes Greeks varant motoru
│   ├── brokerage_sim.py    # AKD & Smart Money simülatörü
│   ├── ai_committee.py     # 4 Ajanlı Yapay Zeka Komitesi
│   ├── trade_desk.py       # Destek/Direnç, TP, ATR Stop-Loss
│   └── lstm_sim.py         # LSTM derin öğrenme tahmin eğrileri
├── static/
│   ├── index.html          # Modern Dark Fintech Terminal Arayüzü
│   ├── style.css           # Terminal CSS stilleri & neon efektler
│   ├── app.js              # Dinamik UI & grafik kontrolcüsü
│   └── lightweight-charts.js # TradingView grafik kütüphanesi
├── data/
│   └── cache_backup.json   # Disk önbellek yedeği
├── main.py                 # FastAPI REST API Sunucusu
├── run.py                  # Kolay başlatıcı script
├── start_tradbot.bat       # Windows tek tık başlatıcı
├── requirements.txt        # Python kütüphane bağımlılıkları
├── Dockerfile              # Docker konteyner yapılandırması
├── render.yaml             # Render.com otomatik deploy konfigürasyonu
└── test_e2e.py             # Uçtan uca doğrulama testleri
```
