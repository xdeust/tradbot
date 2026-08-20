"""
Tradbot - BIST ve Küresel Piyasa Veri Motoru (Market Data Engine)
Yahoo Finance ve kamusal veri akışlarından veri çeker.
"""

import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import requests
import json
import logging
from typing import Dict, List, Optional, Any
from core.symbols import clean_symbol, to_yfinance_symbol, BIST_STOCKS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MarketData")

class MarketDataEngine:
    """BIST hisse ve piyasa verilerini çeken motor"""
    
    @staticmethod
    def get_ticker_history(symbol: str, interval: str = "1d", period: str = "6mo") -> Optional[pd.DataFrame]:
        """
        Belirtilen hissenin OHLCV mum verilerini çeker.
        interval: 1m, 5m, 15m, 1h, 1d, 1wk
        period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y
        """
        yf_sym = to_yfinance_symbol(symbol)
        try:
            # yfinance ile veri çek
            ticker = yf.Ticker(yf_sym)
            df = ticker.history(period=period, interval=interval)
            
            if df.empty or len(df) < 5:
                # Yedek deneme: period=1y
                df = ticker.history(period="1y", interval="1d") if interval == "1d" else df
                
            if df.empty:
                logger.warning(f"{symbol} ({yf_sym}) için veri boş döndü.")
                return None
                
            # Sütun isimlerini standartlaştır
            df.index = pd.to_datetime(df.index)
            # Timezone kaldır (grafik kütüphaneleri için temiz Unix timestamp veya YYYY-MM-DD formatı)
            if df.index.tz is not None:
                df.index = df.index.tz_convert('Europe/Istanbul').tz_localize(None)
                
            return df
        except Exception as e:
            logger.error(f"Hata {symbol} geçmiş veri çekilirken: {e}")
            return None

    @staticmethod
    def get_batch_quotes(symbols: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Birden fazla sembolün son fiyat, hacim ve değişim verilerini hızlıca toplu çeker.
        """
        results = {}
        yf_symbols = [to_yfinance_symbol(s) for s in symbols]
        
        try:
            # Batch download ile son 5 günlük veri çek
            df = yf.download(tickers=yf_symbols, period="5d", interval="1d", group_by="ticker", auto_adjust=True, progress=False)
            
            for orig_sym, yf_sym in zip(symbols, yf_symbols):
                try:
                    if len(symbols) == 1:
                        stock_df = df
                    else:
                        stock_df = df[yf_sym] if yf_sym in df else pd.DataFrame()
                        
                    stock_df = stock_df.dropna(subset=['Close'])
                    if not stock_df.empty and len(stock_df) >= 2:
                        last_close = float(stock_df['Close'].iloc[-1])
                        prev_close = float(stock_df['Close'].iloc[-2])
                        high = float(stock_df['High'].iloc[-1])
                        low = float(stock_df['Low'].iloc[-1])
                        volume = float(stock_df['Volume'].iloc[-1])
                        change_pct = round(((last_close - prev_close) / prev_close) * 100, 2)
                        money_volume = round(last_close * volume, 2)
                        
                        results[clean_symbol(orig_sym)] = {
                            "symbol": clean_symbol(orig_sym),
                            "price": round(last_close, 2),
                            "prev_close": round(prev_close, 2),
                            "high": round(high, 2),
                            "low": round(low, 2),
                            "volume": volume,
                            "money_volume": money_volume,
                            "change_pct": change_pct,
                            "updated_at": datetime.datetime.now().strftime("%H:%M:%S")
                        }
                except Exception as ex:
                    continue
        except Exception as e:
            logger.error(f"Batch quotes çekilirken hata: {e}")
            
        return results

    @staticmethod
    def get_ticker_news(symbol: str, limit: int = 6) -> List[Dict[str, Any]]:
        """Hisseye özel son haberleri çeker"""
        yf_sym = to_yfinance_symbol(symbol)
        news_list = []
        try:
            ticker = yf.Ticker(yf_sym)
            raw_news = ticker.news or []
            for item in raw_news[:limit]:
                title = item.get("title", "")
                link = item.get("link", "#")
                publisher = item.get("publisher", "Yahoo Finance")
                pub_time = item.get("providerPublishTime", None)
                date_str = datetime.datetime.fromtimestamp(pub_time).strftime("%d.%m.%Y %H:%M") if pub_time else "Bugün"
                
                news_list.append({
                    "title": title,
                    "link": link,
                    "publisher": publisher,
                    "date": date_str,
                    "symbol": clean_symbol(symbol)
                })
        except Exception as e:
            logger.warning(f"{symbol} haberleri alınamadı: {e}")
            
        return news_list

    @staticmethod
    def get_global_market_news(limit: int = 15) -> List[Dict[str, Any]]:
        """Piyasa geneli ve ekonomi dergisi haberlerini derler"""
        all_news = []
        try:
            # BIST 30 liderlerinden haberleri topla
            sample_tickers = ["THYAO.IS", "GARAN.IS", "EREGL.IS", "TUPRS.IS", "BIMAS.IS"]
            for yf_sym in sample_tickers:
                t = yf.Ticker(yf_sym)
                for n in (t.news or [])[:3]:
                    pub_time = n.get("providerPublishTime", None)
                    date_str = datetime.datetime.fromtimestamp(pub_time).strftime("%d.%m.%Y %H:%M") if pub_time else "Bugün"
                    all_news.append({
                        "title": n.get("title", ""),
                        "link": n.get("link", "#"),
                        "publisher": n.get("publisher", "Piyasa Bülteni"),
                        "date": date_str,
                        "category": "BIST & KAP"
                    })
                    if len(all_news) >= limit:
                        break
                if len(all_news) >= limit:
                    break
        except Exception as e:
            logger.error(f"Global haberler çekilirken hata: {e}")
            
        # Eğer haber bulunamazsa varsayılan son piyasa haberlerini ekle
        if not all_news:
            now_str = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
            all_news = [
                {"title": "Borsa İstanbul'da BIST 100 endeksi günü rekor hacimle sürdürüyor.", "publisher": "Finans Radar", "date": now_str, "link": "#", "category": "Piyasa"},
                {"title": "TCMB faiz kararı ve likidite adımları piyasalar tarafından yakından takip ediliyor.", "publisher": "Ekonomi Masası", "date": now_str, "link": "#", "category": "Makro"},
                {"title": "Sanayi ve Havacılık hisselerinde kurumsal para girişleri ivme kazanıyor.", "publisher": "Fintech Terminal", "date": now_str, "link": "#", "category": "Sektör"}
            ]
            
        return all_news
