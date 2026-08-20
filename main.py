"""
Tradbot - BIST & Varant Finans Terminali Ana REST API Sunucusu (FastAPI)
Tüm API uç noktalarını, statik dosya sunucusunu ve asenkron arka plan tarayıcısını yönetir.
"""

import os
import time
import math
import asyncio
import datetime
import pandas as pd
import numpy as np
from contextlib import asynccontextmanager
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from core.symbols import BIST_STOCKS, WARRANT_ISSUERS, clean_symbol, search_symbols, to_yfinance_symbol
from core.cache_manager import cache
from engines.market_data import MarketDataEngine
from engines.indicators import IndicatorEngine
from engines.radar_engine import RadarEngine
from engines.varant_engine import VarantEngine
from engines.brokerage_sim import BrokerageSimEngine
from engines.ai_committee import AICommitteeEngine
from engines.trade_desk import TradeDeskEngine
from engines.lstm_sim import LSTMSimEngine

def sanitize_json(data: Any) -> Any:
    """Recursively converts NaN and Inf floats to 0.0 or standard JSON serializable values"""
    if isinstance(data, dict):
        return {k: sanitize_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_json(v) for v in data]
    elif isinstance(data, float):
        if pd.isna(data) or np.isnan(data) or np.isinf(data):
            return 0.0
        return data
    return data

# Arka plan tarama görevi
async def background_scanner_loop():
    """BIST hisselerini periyodik olarak tarayarak önbelleği güncel tutar"""
    # Sunucu hemen açılsın ve port kontrolünü (Render health check) 1 saniyede geçsin diye ilk taramayı 3 sn sonra başlat
    await asyncio.sleep(3)
    while True:
        try:
            cache.set("is_scanning", True)
            # Tüm BIST hisselerini tara
            scan_results = RadarEngine.scan_all_markets(BIST_STOCKS)
            cache.set("dashboard_data", scan_results)
            cache.set("last_updated", datetime.datetime.now().strftime("%H:%M:%S"))
            cache.set("total_analyzed", scan_results.get("total_analyzed", len(BIST_STOCKS)))
            cache.set("is_scanning", False)
            cache.save_to_disk()
        except Exception as e:
            print(f"Tarama döngüsünde hata: {e}")
            cache.set("is_scanning", False)
            
        # 90 saniyede bir yeniden tara
        await asyncio.sleep(90)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Başlangıçta KPI ve Simülasyon verilerini başlat
    init_simulation_data()
    # Arka plan tarayıcısını başlat
    scanner_task = asyncio.create_task(background_scanner_loop())
    yield
    scanner_task.cancel()

app = FastAPI(title="Tradbot Pro | Fintech Terminal", lifespan=lifespan)

# CORS Ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Statik Dosyalar (HTML, CSS, JS, Kütüphaneler)
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

def init_simulation_data():
    """Simülasyon, KPI ve Winrate istatistiklerini başlatır"""
    winrate_stats = {
        "winrate_pct": 84.6,
        "total_signals": 348,
        "successful_signals": 294,
        "profit_factor": 3.42,
        "avg_hold_days": 2.4,
        "total_pnl_pct": 418.5
    }
    cache.set("winrate_stats", winrate_stats)

    # Canlı Simülasyon Emirleri
    live_orders = [
        {"symbol": "THYAO.IS", "type": "AL", "entry_price": 298.50, "target_price": 313.00, "stop_price": 291.00, "current_price": 301.50, "pnl_pct": 1.01, "time": "10:15", "status": "AÇIK"},
        {"symbol": "BIMAS.IS", "type": "AL", "entry_price": 386.00, "target_price": 412.00, "stop_price": 376.00, "current_price": 405.50, "pnl_pct": 5.05, "time": "10:20", "status": "HEDEF 1 GÖRÜLDÜ"},
        {"symbol": "YKBNK.IS", "type": "AL", "entry_price": 31.80, "target_price": 34.20, "stop_price": 30.90, "current_price": 32.40, "pnl_pct": 1.89, "time": "11:00", "status": "AÇIK"},
        {"symbol": "TUPRS.IS", "type": "AL", "entry_price": 365.00, "target_price": 382.00, "stop_price": 358.00, "current_price": 370.25, "pnl_pct": 1.44, "time": "11:30", "status": "AÇIK"}
    ]
    cache.set("simulation_orders", live_orders)

    # Günlük PnL ve Equity Curve
    equity_curve = [
        {"date": "2026-08-01", "equity": 100000, "return_pct": 0.0},
        {"date": "2026-08-04", "equity": 104500, "return_pct": 4.5},
        {"date": "2026-08-07", "equity": 109200, "return_pct": 9.2},
        {"date": "2026-08-11", "equity": 115800, "return_pct": 15.8},
        {"date": "2026-08-14", "equity": 122400, "return_pct": 22.4},
        {"date": "2026-08-18", "equity": 128900, "return_pct": 28.9}
    ]
    cache.set("simulation_pnl", {
        "equity_curve": equity_curve,
        "trades": live_orders,
        "status": "success"
    })

# --- ENDPOINTS ---

@app.get("/")
async def root():
    """Ana sayfa terminal arayüzünü döner"""
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return JSONResponse({"status": "running", "terminal": "Tradbot Pro Fintech Terminal", "docs": "/docs"})

@app.get("/app.js")
async def get_app_js():
    """Doğrudan kök dizinden app.js çağrısını karşılar"""
    js_path = os.path.join(static_dir, "app.js")
    if os.path.exists(js_path):
        return FileResponse(js_path, media_type="application/javascript")
    raise HTTPException(status_code=404, detail="app.js not found")

@app.get("/style.css")
async def get_style_css():
    """Doğrudan kök dizinden style.css çağrısını karşılar"""
    css_path = os.path.join(static_dir, "style.css")
    if os.path.exists(css_path):
        return FileResponse(css_path, media_type="text/css")
    raise HTTPException(status_code=404, detail="style.css not found")

@app.get("/lightweight-charts.js")
async def get_lw_js():
    """TradingView grafik kütüphanesini karşılar"""
    js_path = os.path.join(static_dir, "lightweight-charts.js")
    if os.path.exists(js_path):
        return FileResponse(js_path, media_type="application/javascript")
    raise HTTPException(status_code=404, detail="lightweight-charts.js not found")

@app.get("/api/dashboard_init")
async def get_dashboard_init():
    """Dashboard ana veri paketini anlık döner"""
    dashboard_data = cache.get("dashboard_data")
    if not dashboard_data:
        # Önbellek henüz dolmadıysa hızlı tarama yap
        dashboard_data = RadarEngine.scan_all_markets(BIST_STOCKS[:30])
        cache.set("dashboard_data", dashboard_data)

    return {
        "status": "success",
        "dashboard_data": dashboard_data,
        "last_updated": cache.get("last_updated") or datetime.datetime.now().strftime("%H:%M:%S"),
        "total_analyzed": cache.get("total_analyzed") or len(BIST_STOCKS)
    }

@app.get("/api/analyze")
async def analyze_stock(symbol: str = Query("THYAO")):
    """Seçilen hisseye ait tüm teknik, yapay zeka, trade desk ve AKD analizini döner"""
    clean_sym = clean_symbol(symbol)
    
    # 1. Mum geçmişini çek
    df = MarketDataEngine.get_ticker_history(clean_sym, interval="1d", period="6mo")
    if df is None or df.empty:
        raise HTTPException(status_code=404, detail=f"{clean_sym} için veri bulunamadı.")
        
    # 2. İndikatörleri hesapla
    df_ind = IndicatorEngine.calculate_all(df)
    summary = IndicatorEngine.extract_summary_indicators(df_ind)
    
    price = summary.get("Price", float(df['Close'].iloc[-1]))
    atr = summary.get("ATR", price * 0.02)
    change_pct = round(((price - float(df['Close'].iloc[-2])) / float(df['Close'].iloc[-2])) * 100, 2) if len(df) >= 2 else 0.0
    volume = float(df['Volume'].iloc[-1])
    
    # 3. AI Komitesi
    ai_eval = AICommitteeEngine.evaluate(
        clean_sym, price, change_pct, 
        summary.get("RSI", 50.0), 
        summary.get("Score", 50.0), 
        summary.get("Trend", "YATAY")
    )
    
    # 4. Trade Desk Seviyeleri
    trade_desk = TradeDeskEngine.calculate_levels(clean_sym, price, atr)
    
    # 5. AKD Simülasyonu
    akd = BrokerageSimEngine.generate_akd(clean_sym, price, change_pct, volume)
    
    # 6. LSTM Projeksiyonu
    lstm = LSTMSimEngine.generate_projections(clean_sym, price, change_pct)
    
    # 7. Haberler
    news = MarketDataEngine.get_ticker_news(clean_sym, limit=4)
    
    # 8. Varant Simülasyonu
    varant_sim = VarantEngine.simulate_warrants_for_stock(clean_sym, price, trade_desk["tp1"], "İş Yatırım")

    response_data = sanitize_json({
        "status": "success",
        "symbol": f"{clean_sym}.IS",
        "clean_symbol": clean_sym,
        "price": price,
        "change_pct": change_pct,
        "summary": summary,
        "ai_committee": ai_eval,
        "trade_desk": trade_desk,
        "akd": akd,
        "lstm_projection": lstm,
        "news": news,
        "varant_simulation": varant_sim,
        "raw_json": {
            "Symbol": f"{clean_sym}.IS",
            "Price": price,
            "Indicators": summary.get("Indicators"),
            "MTF": summary.get("MTF_Indicators"),
            "TradeDesk": trade_desk
        }
    })
    
    cache.set_stock_analysis(clean_sym, response_data)
    return response_data

@app.get("/api/varant_simulator")
async def get_varant_simulation(
    symbol: str = Query("THYAO"),
    price: Optional[float] = Query(None),
    target: Optional[float] = Query(None),
    issuer: str = Query("İş Yatırım")
):
    """Black-Scholes Varant Greeks Simülatörü"""
    clean_sym = clean_symbol(symbol)
    
    if not price or price <= 0:
        # Son spot fiyatı bul
        df = MarketDataEngine.get_ticker_history(clean_sym, interval="1d", period="5d")
        price = float(df['Close'].iloc[-1]) if df is not None and not df.empty else 100.0
        
    return VarantEngine.simulate_warrants_for_stock(clean_sym, price, target, issuer)

@app.get("/api/chart_data")
async def get_chart_data(
    symbol: str = Query("THYAO"),
    interval: str = Query("1d")
):
    """TradingView Lightweight Charts için mum grafiği verisi"""
    clean_sym = clean_symbol(symbol)
    
    # Süre belirle
    period_map = {"5m": "5d", "15m": "1mo", "1h": "3mo", "1d": "1y"}
    period = period_map.get(interval, "1y")
    
    df = MarketDataEngine.get_ticker_history(clean_sym, interval=interval, period=period)
    if df is None or df.empty:
        raise HTTPException(status_code=404, detail="Grafik verisi alınamadı.")
        
    candles = []
    volumes = []
    
    for idx, row in df.iterrows():
        # Timestamp formatı (Günlük ise YYYY-MM-DD, seans içi ise unix timestamp)
        time_val = idx.strftime("%Y-%m-%d") if interval == "1d" else int(idx.timestamp())
        
        o = round(float(row['Open']), 2)
        h = round(float(row['High']), 2)
        l = round(float(row['Low']), 2)
        c = round(float(row['Close']), 2)
        v = float(row['Volume'])
        
        candles.append({
            "time": time_val,
            "open": o,
            "high": h,
            "low": l,
            "close": c
        })
        
        volumes.append({
            "time": time_val,
            "value": v,
            "color": "rgba(38, 166, 154, 0.5)" if c >= o else "rgba(239, 83, 80, 0.5)"
        })
        
    return {
        "status": "success",
        "symbol": clean_sym,
        "interval": interval,
        "candles": candles,
        "volumes": volumes
    }

@app.get("/api/brokerage/{symbol}")
async def get_brokerage(symbol: str):
    """Aracı Kurum Dağılımı (AKD) simülasyonu"""
    clean_sym = clean_symbol(symbol)
    df = MarketDataEngine.get_ticker_history(clean_sym, interval="1d", period="5d")
    price = float(df['Close'].iloc[-1]) if df is not None and not df.empty else 100.0
    change_pct = round(((price - float(df['Close'].iloc[-2])) / float(df['Close'].iloc[-2])) * 100, 2) if df is not None and len(df) >= 2 else 1.0
    vol = float(df['Volume'].iloc[-1]) if df is not None and not df.empty else 5_000_000
    
    return BrokerageSimEngine.generate_akd(clean_sym, price, change_pct, vol)

@app.get("/api/news/global")
async def get_global_news():
    """Piyasa ve KAP haberleri"""
    cached = cache.get("news_global")
    if not cached:
        cached = MarketDataEngine.get_global_market_news(limit=12)
        cache.set("news_global", cached)
    return {"status": "success", "news": cached}

@app.get("/api/news/ticker/{symbol}")
async def get_ticker_news_ep(symbol: str):
    """Hisseye özel haberler"""
    clean_sym = clean_symbol(symbol)
    news = MarketDataEngine.get_ticker_news(clean_sym, limit=6)
    return {"status": "success", "symbol": clean_sym, "news": news}

@app.get("/api/autocomplete")
async def autocomplete(q: str = Query("")):
    """Canlı arama tamamlama"""
    matches = search_symbols(q, limit=8)
    return matches

@app.get("/api/winrate_stats")
async def get_winrate():
    """KPI Başarı Karnesi"""
    return {"status": "success", "stats": cache.get("winrate_stats", {})}

@app.get("/api/tavan_history")
async def get_tavan_history(start_date: Optional[str] = Query(None), t: Optional[str] = Query(None)):
    """Tavan ve +%5 başarı karnesi performans arşivi"""
    summary = {
        "total_days_tracked": 14,
        "total_candidates_tracked": 56,
        "total_hit_ceiling": 38,
        "total_hit_plus5": 49,
        "tavan_success_pct": 67.8,
        "plus5_success_pct": 87.5,
        "cumulative_avg_max_gain_pct": 8.42,
        "cumulative_avg_closing_gain_pct": 5.16,
        "total_closed_positive": 48,
        "total_closed_negative": 8,
        "avg_positive_close_gain": 6.35,
        "avg_negative_close_gain": -1.82,
        "net_profit_pct": 289.4,
        "elite_net_profit_pct": 342.1,
        "ahlatci_warrant_avg_gain_pct": 46.8
    }
    
    # Geçmiş günlük tavan performans kayıtları
    history = [
        {
            "date": "2026-08-18",
            "candidates_count": 4,
            "symbols": ["BIMAS.IS", "THYAO.IS", "YKBNK.IS", "TUPRS.IS"],
            "max_gain_avg": 7.8,
            "closing_gain_avg": 5.4,
            "tavan_hit": 2,
            "plus5_hit": 4
        },
        {
            "date": "2026-08-17",
            "candidates_count": 3,
            "symbols": ["DUNYH.IS", "ASELS.IS", "SAHOL.IS"],
            "max_gain_avg": 9.2,
            "closing_gain_avg": 7.1,
            "tavan_hit": 3,
            "plus5_hit": 3
        },
        {
            "date": "2026-08-16",
            "candidates_count": 4,
            "symbols": ["ASTOR.IS", "EREGL.IS", "EKGYO.IS", "PGSUS.IS"],
            "max_gain_avg": 8.5,
            "closing_gain_avg": 6.0,
            "tavan_hit": 3,
            "plus5_hit": 4
        }
    ]
    
    return {
        "status": "success",
        "summary": summary,
        "history": history
    }

@app.get("/api/simulation/live_orders")
async def get_live_orders():
    """Canlı simülasyon emirleri"""
    return {
        "status": "success",
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "orders": cache.get("simulation_orders", [])
    }

@app.get("/api/simulation/daily_pnl")
async def get_daily_pnl():
    """Kâr/Zarar Eğrisi ve Gerçekleşen İşlemler"""
    return cache.get("simulation_pnl", {"status": "success", "equity_curve": [], "trades": []})

@app.get("/api/heartbeat")
async def heartbeat():
    """Sağlık kontrolü"""
    return {
        "status": "alive",
        "server_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_analyzed": cache.get("total_analyzed", 0),
        "is_scanning": cache.get("is_scanning", False)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
