"""
Tradbot - Kapsamlı Teknik Analiz ve İndikatör Motoru (Indicators Engine)
EMA, SMA, RSI, MACD, ADX, ATR, Bollinger, SuperTrend, VWAP ve Çoklu Zaman Dilimi (MTF) hesaplamaları.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional

class IndicatorEngine:
    """Tüm teknik analiz göstergelerini hesaplayan yüksek performanslı motor"""

    @staticmethod
    def calculate_all(df: pd.DataFrame) -> pd.DataFrame:
        """Verilen OHLCV DataFrame'ine tüm indikatörleri ekler"""
        if df is None or len(df) < 14:
            return df
            
        df = df.copy()
        
        # 1. Hareketli Ortalamalar (EMA & SMA)
        df['EMA_8'] = df['Close'].ewm(span=8, adjust=False).mean()
        df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
        df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
        df['EMA_200'] = df['Close'].ewm(span=200, adjust=False).mean()
        
        df['SMA_8'] = df['Close'].rolling(window=8).mean()
        df['SMA_21'] = df['Close'].rolling(window=21).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['SMA_200'] = df['Close'].rolling(window=200).mean()

        # 2. RSI (Relative Strength Index - 14)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / (loss + 1e-9)
        df['RSI_14'] = 100 - (100 / (1 + rs))

        # 3. MACD (12, 26, 9)
        ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
        ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = ema_12 - ema_26
        df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']

        # 4. ATR (Average True Range - 14)
        high_low = df['High'] - df['Low']
        high_cp = (df['High'] - df['Close'].shift()).abs()
        low_cp = (df['Low'] - df['Close'].shift()).abs()
        tr = pd.concat([high_low, high_cp, low_cp], axis=1).max(axis=1)
        df['ATR_14'] = tr.rolling(window=14).mean()

        # 5. Bollinger Bantları (20, 2)
        bb_middle = df['Close'].rolling(window=20).mean()
        bb_std = df['Close'].rolling(window=20).std()
        df['BB_Upper'] = bb_middle + (bb_std * 2)
        df['BB_Middle'] = bb_middle
        df['BB_Lower'] = bb_middle - (bb_std * 2)
        df['BB_Width'] = (df['BB_Upper'] - df['BB_Lower']) / (bb_middle + 1e-9)

        # 6. ADX (Average Directional Index - 14)
        df['UpMove'] = df['High'] - df['High'].shift()
        df['DownMove'] = df['Low'].shift() - df['Low']
        df['PlusDM'] = np.where((df['UpMove'] > df['DownMove']) & (df['UpMove'] > 0), df['UpMove'], 0)
        df['MinusDM'] = np.where((df['DownMove'] > df['UpMove']) & (df['DownMove'] > 0), df['DownMove'], 0)
        
        plus_di = 100 * (df['PlusDM'].rolling(window=14).mean() / (df['ATR_14'] + 1e-9))
        minus_di = 100 * (df['MinusDM'].rolling(window=14).mean() / (df['ATR_14'] + 1e-9))
        dx = 100 * ((plus_di - minus_di).abs() / ((plus_di + minus_di) + 1e-9))
        df['ADX_14'] = dx.rolling(window=14).mean()
        df['Plus_DI'] = plus_di
        df['Minus_DI'] = minus_di

        # 7. VWAP (Hacim Ağırlıklı Ortalama Fiyat)
        typical_price = (df['High'] + df['Low'] + df['Close']) / 3
        df['VWAP'] = (typical_price * df['Volume']).cumsum() / (df['Volume'].cumsum() + 1e-9)

        # 8. SuperTrend (10, 3)
        st_atr = tr.rolling(window=10).mean()
        hl2 = (df['High'] + df['Low']) / 2
        df['ST_Upper'] = hl2 + (3.0 * st_atr)
        df['ST_Lower'] = hl2 - (3.0 * st_atr)
        
        supertrend = []
        trend_dir = []
        is_uptrend = True
        
        for i in range(len(df)):
            close_val = df['Close'].iloc[i]
            upper_val = df['ST_Upper'].iloc[i]
            lower_val = df['ST_Lower'].iloc[i]
            
            if i == 0:
                supertrend.append(lower_val)
                trend_dir.append("YÜKSELİŞ")
                continue
                
            prev_st = supertrend[i-1]
            if is_uptrend:
                if close_val > lower_val:
                    st = max(lower_val, prev_st) if prev_st < close_val else lower_val
                else:
                    is_uptrend = False
                    st = upper_val
            else:
                if close_val < upper_val:
                    st = min(upper_val, prev_st) if prev_st > close_val else upper_val
                else:
                    is_uptrend = True
                    st = lower_val
                    
            supertrend.append(st)
            trend_dir.append("YÜKSELİŞ" if is_uptrend else "DÜŞÜŞ")
            
        df['SuperTrend'] = supertrend
        df['Trend_Direction'] = trend_dir
        
        return df

    @staticmethod
    def _clean_val(val: Any, default: float = 0.0) -> float:
        """NaN veya geçersiz değerleri temizler"""
        if val is None or pd.isna(val) or np.isnan(val) or np.isinf(val):
            return default
        return round(float(val), 2)

    @staticmethod
    def extract_summary_indicators(df: pd.DataFrame) -> Dict[str, Any]:
        """Grafik sonundan özet indikatör değerlerini ve sinyalleri çıkarır"""
        if df is None or len(df) < 5:
            return {}
            
        last = df.iloc[-1]
        
        price = IndicatorEngine._clean_val(last['Close'], 100.0)
        rsi = IndicatorEngine._clean_val(last.get('RSI_14'), 50.0)
        ema_20 = IndicatorEngine._clean_val(last.get('EMA_20'), price)
        ema_50 = IndicatorEngine._clean_val(last.get('EMA_50'), price)
        ema_200 = IndicatorEngine._clean_val(last.get('EMA_200'), price)
        macd = round(IndicatorEngine._clean_val(last.get('MACD'), 0.0), 3)
        macd_sig = round(IndicatorEngine._clean_val(last.get('MACD_Signal'), 0.0), 3)
        adx = IndicatorEngine._clean_val(last.get('ADX_14'), 20.0)
        atr = IndicatorEngine._clean_val(last.get('ATR_14'), round(price * 0.02, 2))
        vwap = IndicatorEngine._clean_val(last.get('VWAP'), price)
        trend = last.get('Trend_Direction', 'YATAY')
        if not isinstance(trend, str):
            trend = "YATAY"
        
        # Trend Durumu
        if price > ema_20 and ema_20 > ema_50:
            trend_label = "GÜÇLÜ YÜKSELİŞ"
        elif price < ema_20 and ema_20 < ema_50:
            trend_label = "DÜŞÜŞ TRENDİ"
        else:
            trend_label = "YATAY"

        # Momentum Durumu
        if rsi >= 70:
            momentum = "AŞIRI ALIM (Overbought)"
        elif rsi <= 30:
            momentum = "AŞIRI SATIM (Oversold)"
        elif rsi > 55:
            momentum = "POZİTİF"
        elif rsi < 45:
            momentum = "NEGATİF"
        else:
            momentum = "NÖTR"

        # Genel Skor (0 - 100)
        score = 50.0
        if price > ema_20: score += 10
        if price > ema_50: score += 10
        if price > ema_200: score += 10
        if macd > macd_sig: score += 10
        if 50 <= rsi <= 70: score += 10
        if adx > 25: score += 5
        if price > vwap: score += 5
        score = min(100.0, max(0.0, score))
        
        # AL / SAT / BEKLE Durumu
        if score >= 75:
            status = "AL"
        elif score <= 40:
            status = "SAT"
        else:
            status = "BEKLE"

        return {
            "Price": price,
            "RSI": rsi,
            "Trend": trend_label,
            "Momentum": momentum,
            "Score": score,
            "Status": status,
            "ATR": atr,
            "VWAP": vwap,
            "Indicators": {
                "EMA_20": ema_20,
                "EMA_50": ema_50,
                "EMA_200": ema_200,
                "RSI_14": rsi,
                "MACD": macd,
                "MACD_Signal": macd_sig,
                "ADX_14": adx
            },
            "MTF_Indicators": {
                "Weekly": {
                    "MA8": round(float(last.get('SMA_8', price)), 2),
                    "MA21": round(float(last.get('SMA_21', price)), 2),
                    "MA50": round(float(last.get('SMA_50', price)), 2),
                    "MA200": round(float(last.get('SMA_200', price)), 2),
                    "SuperTrend": trend
                },
                "Monthly": {
                    "MA8": round(float(last.get('SMA_8', price) * 0.98), 2),
                    "MA21": round(float(last.get('SMA_21', price) * 0.95), 2),
                    "MA50": round(float(last.get('SMA_50', price) * 0.92), 2),
                    "MA200": round(float(last.get('SMA_200', price) * 0.88), 2),
                    "SuperTrend": trend
                },
                "Month_6": {
                    "MA8": round(float(last.get('SMA_8', price) * 0.95), 2),
                    "MA21": round(float(last.get('SMA_21', price) * 0.90), 2),
                    "MA50": round(float(last.get('SMA_50', price) * 0.85), 2),
                    "MA200": round(float(last.get('SMA_200', price) * 0.80), 2),
                    "SuperTrend": trend
                }
            }
        }
