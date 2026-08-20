"""
Tradbot - Black-Scholes Varant Fiyatlama ve Greeks Simülatörü (Varant Engine)
Call/Put Fiyatı, Delta, Gamma, Theta (Zaman Erimesi), Vega, Gearing (Kaldıraç) ve Başabaş Hesaplayıcı.
İş Yatırım, Ak Yatırım, Garanti BBVA ve Ahlatcı Yatırım ihraççı simülasyonları.
"""

import math
import numpy as np
from scipy.stats import norm
from typing import Dict, List, Any, Optional
from core.symbols import clean_symbol, WARRANT_ISSUERS

class VarantEngine:
    """Black-Scholes Varant ve Greeks Hesaplama Motoru"""

    @staticmethod
    def black_scholes_call(S: float, K: float, T: float, r: float, sigma: float, multiplier: float = 1.0) -> float:
        """Call Varant Fiyatı"""
        if T <= 0 or S <= 0 or K <= 0 or sigma <= 0:
            return max(0.0, (S - K) * multiplier)
        
        d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        price = (S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)) * multiplier
        return max(0.01, round(price, 3))

    @staticmethod
    def black_scholes_put(S: float, K: float, T: float, r: float, sigma: float, multiplier: float = 1.0) -> float:
        """Put Varant Fiyatı"""
        if T <= 0 or S <= 0 or K <= 0 or sigma <= 0:
            return max(0.0, (K - S) * multiplier)
            
        d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        price = (K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)) * multiplier
        return max(0.01, round(price, 3))

    @staticmethod
    def calculate_greeks(S: float, K: float, T: float, r: float, sigma: float, varant_type: str = "CALL", multiplier: float = 1.0) -> Dict[str, float]:
        """Tüm Greeks parametrelerini hesaplar"""
        if T <= 0.001:
            T = 0.001
        if S <= 0: S = 1.0
        if K <= 0: K = 1.0
        if sigma <= 0: sigma = 0.30

        d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        
        pdf_d1 = norm.pdf(d1)
        
        if varant_type.upper() == "CALL":
            delta = norm.cdf(d1) * multiplier
            theta = (-(S * pdf_d1 * sigma) / (2 * math.sqrt(T)) - r * K * math.exp(-r * T) * norm.cdf(d2)) / 365 * multiplier
            warrant_price = VarantEngine.black_scholes_call(S, K, T, r, sigma, multiplier)
            breakeven = round(K + (warrant_price / multiplier), 2)
        else:
            delta = (norm.cdf(d1) - 1.0) * multiplier
            theta = (-(S * pdf_d1 * sigma) / (2 * math.sqrt(T)) + r * K * math.exp(-r * T) * norm.cdf(-d2)) / 365 * multiplier
            warrant_price = VarantEngine.black_scholes_put(S, K, T, r, sigma, multiplier)
            breakeven = round(K - (warrant_price / multiplier), 2)

        gamma = (pdf_d1 / (S * sigma * math.sqrt(T))) * multiplier
        vega = (S * math.sqrt(T) * pdf_d1) / 100 * multiplier
        
        # Etkin Kaldıraç (Gearing)
        if warrant_price > 0:
            effective_gearing = abs(delta) * (S / warrant_price)
        else:
            effective_gearing = 1.0

        return {
            "warrant_price": round(warrant_price, 2),
            "delta": round(delta, 3),
            "gamma": round(gamma, 4),
            "theta_daily": round(theta, 4),
            "vega": round(vega, 4),
            "effective_gearing": round(effective_gearing, 2),
            "breakeven": breakeven
        }

    @staticmethod
    def simulate_warrants_for_stock(symbol: str, spot_price: float, target_price: Optional[float] = None, issuer: str = "İş Yatırım") -> Dict[str, Any]:
        """
        Seçilen hisse için 4 farklı kullanım fiyatı (ITM, ATM, OTM) ve vadede Call/Put varant listesi oluşturur.
        Hedef fiyata ulaşıldığındaki kâr/zarar senaryosunu hesaplar.
        """
        clean_sym = clean_symbol(symbol)
        if not target_price or target_price <= 0:
            target_price = round(spot_price * 1.05, 2)  # Varsayılan %5 hedef
            
        pct_diff = round(((target_price - spot_price) / spot_price) * 100, 2)
        
        # Faiz oranı (TCMB / Piyasa faizi: %45) ve Volatilite (%35)
        r = 0.45
        sigma = 0.38
        days_to_expiry = 45
        T = days_to_expiry / 365.0
        
        # Çarpan (Hisse fiyatına göre ayarlanır)
        multiplier = 0.1 if spot_price > 100 else 0.5 if spot_price > 30 else 1.0
        
        # İhraççı kod ön ekleri
        prefix_map = {
            "İş Yatırım": "IY",
            "Ak Yatırım": "AK",
            "Garanti BBVA": "GB",
            "Ahlatcı Yatırım": "AH"
        }
        pfx = prefix_map.get(issuer, "IY")
        
        # Kullanım fiyatı varyasyonları
        strikes = [
            {"label": "Karda (ITM)", "k": round(spot_price * 0.92, 1)},
            {"label": "Başa Baş (ATM)", "k": round(spot_price, 1)},
            {"label": "Zararda (OTM)", "k": round(spot_price * 1.06, 1)},
            {"label": "Derin OTM", "k": round(spot_price * 1.14, 1)},
        ]
        
        warrants = []
        for idx, s in enumerate(strikes):
            K = s["k"]
            # Call Varant
            call_code = f"{clean_sym[:3]}{pfx}A{idx+1}"
            call_greeks = VarantEngine.calculate_greeks(spot_price, K, T, r, sigma, "CALL", multiplier)
            # Hedef fiyatta beklenen yeni varant fiyatı
            call_future_price = VarantEngine.black_scholes_call(target_price, K, max(0.01, (days_to_expiry - 3)/365.0), r, sigma, multiplier)
            call_pnl_pct = round(((call_future_price - call_greeks["warrant_price"]) / (call_greeks["warrant_price"] + 1e-6)) * 100, 1)
            
            warrants.append({
                "code": call_code,
                "type": "ALIM (CALL)",
                "strike": K,
                "status": s["label"],
                "price": call_greeks["warrant_price"],
                "target_price": round(call_future_price, 2),
                "expected_pnl_pct": call_pnl_pct,
                "delta": call_greeks["delta"],
                "theta": call_greeks["theta_daily"],
                "gearing": call_greeks["effective_gearing"],
                "breakeven": call_greeks["breakeven"],
                "days_left": days_to_expiry,
                "issuer": issuer,
                "multiplier": multiplier
            })
            
            # Put Varant
            put_code = f"{clean_sym[:3]}{pfx}P{idx+1}"
            put_greeks = VarantEngine.calculate_greeks(spot_price, K, T, r, sigma, "PUT", multiplier)
            # Put için hedef fiyat tam tersi yön
            put_target_price = round(spot_price * (1 - (pct_diff/100)), 2)
            put_future_price = VarantEngine.black_scholes_put(put_target_price, K, max(0.01, (days_to_expiry - 3)/365.0), r, sigma, multiplier)
            put_pnl_pct = round(((put_future_price - put_greeks["warrant_price"]) / (put_greeks["warrant_price"] + 1e-6)) * 100, 1)

            warrants.append({
                "code": put_code,
                "type": "SATIM (PUT)",
                "strike": K,
                "status": s["label"],
                "price": put_greeks["warrant_price"],
                "target_price": round(put_future_price, 2),
                "expected_pnl_pct": put_pnl_pct,
                "delta": put_greeks["delta"],
                "theta": put_greeks["theta_daily"],
                "gearing": put_greeks["effective_gearing"],
                "breakeven": put_greeks["breakeven"],
                "days_left": days_to_expiry,
                "issuer": issuer,
                "multiplier": multiplier
            })

        return {
            "status": "success",
            "symbol": clean_sym,
            "current_price": spot_price,
            "target_price": target_price,
            "price_diff_pct": pct_diff,
            "issuer": issuer,
            "warrants": warrants
        }
