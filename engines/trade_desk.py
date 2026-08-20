"""
Tradbot - Operasyon Merkezi ve İşlem Masası (Trade Desk Engine)
ATR Tabanlı Zarar Kes (Stop-Loss), Giriş (Entry), Hedef (TP1, TP2), Destek/Direnç Matrisi ve Zincir Emirler (OCO).
"""

from typing import Dict, Any
from core.symbols import clean_symbol

class TradeDeskEngine:
    """Trade Desk seviyelerini ve emir şablonlarını hesaplayan motor"""

    @staticmethod
    def calculate_levels(symbol: str, spot_price: float, atr: float, high: float = 0, low: float = 0) -> Dict[str, Any]:
        """Giriş, Kâr Al, Zarar Kes ve Destek/Direnç seviyelerini üretir"""
        clean_sym = clean_symbol(symbol)
        
        if atr <= 0:
            atr = spot_price * 0.025  # %2.5 varsayılan ATR
            
        # Stop-Loss: Spot - (1.5 * ATR)
        stop_loss = round(spot_price - (1.5 * atr), 2)
        stop_loss_pct = round(((stop_loss - spot_price) / spot_price) * 100, 2)
        
        # Giriş Bölgesi
        entry_min = round(spot_price * 0.995, 2)
        entry_max = round(spot_price * 1.005, 2)
        
        # TP1 (Hedef 1 - 2 * ATR): %50 Kâr Al
        tp1 = round(spot_price + (2.0 * atr), 2)
        tp1_pct = round(((tp1 - spot_price) / spot_price) * 100, 2)
        
        # TP2 (Hedef 2 - 3.5 * ATR): Tam Çıkış
        tp2 = round(spot_price + (3.5 * atr), 2)
        tp2_pct = round(((tp2 - spot_price) / spot_price) * 100, 2)
        
        # Risk / Ödül Oranı (R:R)
        risk = abs(spot_price - stop_loss)
        reward = abs(tp1 - spot_price)
        rr_ratio = round(reward / (risk + 1e-6), 2)

        # Destek ve Direnç Matrisi (Fibonacci / Pivot Seviyeleri)
        pivot = round(spot_price, 2)
        r1 = round(spot_price + (1.0 * atr), 2)
        r2 = round(spot_price + (2.0 * atr), 2)
        r3 = round(spot_price + (3.5 * atr), 2)
        
        s1 = round(spot_price - (1.0 * atr), 2)
        s2 = round(spot_price - (2.0 * atr), 2)
        s3 = round(spot_price - (3.0 * atr), 2)

        # Zincir Emir (OCO) Açıklaması
        oco_order_text = (
            f"Banka/Aracı Kurum Zincir Emir:\n"
            f"• Alış: {spot_price} TL\n"
            f"• Kâr Al (TP1): {tp1} TL (+%{tp1_pct})\n"
            f"• Zarar Durdur (Stop): {stop_loss} TL (%{stop_loss_pct})"
        )

        return {
            "status": "success",
            "symbol": clean_sym,
            "spot_price": spot_price,
            "atr": round(atr, 2),
            "entry_range": f"{entry_min} - {entry_max} TL",
            "tp1": tp1,
            "tp1_pct": tp1_pct,
            "tp2": tp2,
            "tp2_pct": tp2_pct,
            "stop_loss": stop_loss,
            "stop_loss_pct": stop_loss_pct,
            "rr_ratio": f"1:{rr_ratio}",
            "sr_matrix": {
                "R3": r3,
                "R2": r2,
                "R1": r1,
                "Pivot": pivot,
                "S1": s1,
                "S2": s2,
                "S3": s3
            },
            "oco_template": oco_order_text
        }
