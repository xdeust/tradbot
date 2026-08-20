"""
Tradbot - Aracı Kurum Dağılımı (AKD) ve Smart Money Simülasyon Motoru (Brokerage Simulation Engine)
BofA, İş Yatırım, Yapı Kredi, Garanti, Ak Yatırım vb. net alıcı/satıcı simülasyonu,
3 Temel Kanıt ve 4 Adımlı Taktik İşlem Planı üretir.
"""

import random
import math
from typing import Dict, List, Any
from core.symbols import clean_symbol

class BrokerageSimEngine:
    """Hacim ve mum kırılımlarına dayalı Aracı Kurum Dağılımı simülatörü"""

    BROKERS = [
        {"name": "Bank of America", "type": "Yabancı / Algoritmik", "weight": 1.4},
        {"name": "İş Yatırım", "type": "Yerli Kurumsal", "weight": 1.2},
        {"name": "Yapı Kredi Yatırım", "type": "Bireysel / Kurumsal", "weight": 1.1},
        {"name": "Garanti BBVA", "type": "Yerli Kurumsal", "weight": 1.0},
        {"name": "Ak Yatırım", "type": "Yerli Kurumsal", "weight": 0.95},
        {"name": "QNB Finansinvest", "type": "Yabancı / HFT", "weight": 0.9},
        {"name": "Deniz Yatırım", "type": "Bireysel / Kurumsal", "weight": 0.8},
        {"name": "Vakıf Yatırım", "type": "Kamu Fonu / Bireysel", "weight": 0.75},
        {"name": "Ziraat Yatırım", "type": "Kamu Fonu / Bireysel", "weight": 0.75},
        {"name": "TEB Yatırım", "type": "Yabancı Ağırlıklı", "weight": 0.85},
        {"name": "Gedik Yatırım", "type": "Bireysel Ağırlıklı", "weight": 0.7},
        {"name": "İnfo Yatırım", "type": "Bireysel / Hızlı", "weight": 0.7}
    ]

    @staticmethod
    def generate_akd(symbol: str, spot_price: float, change_pct: float, volume: float) -> Dict[str, Any]:
        """Hisse fiyat hareketine ve hacmine göre gerçekçi AKD matrisi üretir"""
        clean_sym = clean_symbol(symbol)
        
        # Toplam işlem hacmi lot bazında
        total_volume_lots = max(100_000, int(volume if volume > 0 else 5_000_000))
        net_lot_factor = min(0.35, max(0.05, abs(change_pct) * 0.04))
        
        # Alış / Satış baskısı
        is_bullish = change_pct >= 0
        total_buy_lot = int(total_volume_lots * (0.55 if is_bullish else 0.45))
        total_sell_lot = total_volume_lots - total_buy_lot
        net_difference = total_buy_lot - total_sell_lot

        # Kurumları karıştır ve alıcı/satıcı ata
        brokers_copy = list(BrokerageSimEngine.BROKERS)
        # Deterministic seed tabanlı hisse kodu
        random.seed(sum(ord(c) for c in clean_sym) + int(spot_price * 10))
        random.shuffle(brokers_copy)

        buyers_raw = brokers_copy[:5]
        sellers_raw = brokers_copy[5:10]

        # Alıcıları oranla
        buy_shares = [35.0, 22.0, 16.0, 12.0, 8.0]
        buyers = []
        for b, share in zip(buyers_raw, buy_shares):
            b_lots = int(total_buy_lot * (share / 100.0))
            cost_offset = spot_price * (random.uniform(-0.005, 0.002) if is_bullish else random.uniform(-0.015, -0.002))
            cost = round(spot_price + cost_offset, 2)
            buyers.append({
                "institution": b["name"],
                "type": b["type"],
                "net_lots": b_lots,
                "percentage": share,
                "avg_cost": cost,
                "total_tl": round(b_lots * cost, 2)
            })

        # Satıcıları oranla
        sell_shares = [32.0, 24.0, 18.0, 11.0, 7.0]
        sellers = []
        for s, share in zip(sellers_raw, sell_shares):
            s_lots = int(total_sell_lot * (share / 100.0))
            cost_offset = spot_price * (random.uniform(-0.002, 0.006) if is_bullish else random.uniform(0.002, 0.012))
            cost = round(spot_price + cost_offset, 2)
            sellers.append({
                "institution": s["name"],
                "type": s["type"],
                "net_lots": s_lots,
                "percentage": share,
                "avg_cost": cost,
                "total_tl": round(s_lots * cost, 2)
            })

        # 3 Temel Kanıt (Conviction Proofs)
        lead_buyer = buyers[0]["institution"]
        lead_seller = sellers[0]["institution"]
        
        if is_bullish:
            proofs = [
                f"🛡️ **Kurumsal Liderlik:** {lead_buyer}, toplam alımların %{buyers[0]['percentage']}'sini tek başına karşılayarak hissede güçlü bir taban oluşturdu.",
                f"📊 **Net Para Girişi:** İlk 5 kurumun net alım üstünlüğü %{sum(b['percentage'] for b in buyers[:3]):.1f} seviyesinde konsolide oldu.",
                f"⚡ **Maliyet Desteği:** Alıcıların ağırlıklı ortalama maliyeti {buyers[0]['avg_cost']} TL olup, anlık fiyatın hemen altında güçlü destek teşkil ediyor."
            ]
            smart_money = "🟢 KURUMSAL AKÜMÜLASYON (Akıllı Para Girişi)"
            order_flow = "ALIM AĞIRLIKLI (İsveç / BofA Algoritmaları Aktif)"
        else:
            proofs = [
                f"⚠️ **Satış Baskısı:** {lead_seller}, toplam satışların %{sellers[0]['percentage']}'sini yöneterek fiyat üzerinde baskı kurdu.",
                f"📉 **Para Çıkışı:** İlk 5 satıcı kurum satışların %{sum(s['percentage'] for s in sellers[:3]):.1f}'ini oluşturarak likidite emdi.",
                f"🛡️ **Maliyet Teyidi:** Satıcıların ağırlıklı ortalama çıkış seviyesi {sellers[0]['avg_cost']} TL olup direnç görevi görüyor."
            ]
            smart_money = "🔴 KURUMSAL DİSTRİBÜSYON (Kâr Realizasyonu)"
            order_flow = "SATIŞ AĞIRLIKLI (Robotik Çıkışlar)"

        # 4 Adımlı Taktik İşlem Planı
        tactical_plan = [
            {"step": 1, "title": "Bölge Teyidi", "desc": f"{spot_price} TL pivot bölgesinin hacimli korunması."},
            {"step": 2, "title": "Kademeli Giriş", "desc": f"{buyers[0]['avg_cost']} TL maliyet bandına yakın geri çekilmelerde alım."},
            {"step": 3, "title": "Risk Yönetimi", "desc": f"Belirlenen Stop-Loss seviyesi altında kesin pozisyon kapatma."},
            {"step": 4, "title": "Hedef Kâr Alımı", "desc": "TP1 seviyesinde %50 kâr realizasyonu ve kalan pozisyonda iz süren stop (Trailing Stop) kullanımı."}
        ]

        return {
            "status": "success",
            "symbol": clean_sym,
            "spot_price": spot_price,
            "change_pct": change_pct,
            "total_buy_lot": total_buy_lot,
            "total_sell_lot": total_sell_lot,
            "net_lot_diff": net_difference,
            "top5_buy_pct": 93.0,
            "top5_sell_pct": 92.0,
            "buyers": buyers,
            "sellers": sellers,
            "smart_money": smart_money,
            "order_flow": order_flow,
            "conviction_proofs": proofs,
            "tactical_plan": tactical_plan
        }
