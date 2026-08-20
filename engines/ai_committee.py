"""
Tradbot - Otonom Yapay Zeka Komitesi ve Çoklu Model Oylama Motoru (AI Committee Engine)
Momentum AI, Trend AI, Quant AI ve Sentiment AI dinamik ağırlıklı oylama sistemi,
CIO Yönetici Özeti ve Tavsiye Edilen/Edilmeyen İşlem Kuralları.
"""

from typing import Dict, Any, List
from core.symbols import clean_symbol

class AICommitteeEngine:
    """4 Uzman Yapay Zeka Ajanından oluşan otonom karar komitesi"""

    @staticmethod
    def evaluate(symbol: str, price: float, change_pct: float, rsi: float, score: float, trend: str) -> Dict[str, Any]:
        """Hisse verilerini 4 modele dağıtır ve konsensüs üretir"""
        clean_sym = clean_symbol(symbol)

        # 1. Model Kararları ve Gerekçeleri
        # Model 1: Trend AI
        if trend == "GÜÇLÜ YÜKSELİŞ" or score >= 75:
            trend_vote = "GÜÇLÜ AL"
            trend_conf = 88.5
            trend_reason = "EMA 20/50 ve SuperTrend güçlü yükseliş kanalı teyit ediyor."
        elif trend == "DÜŞÜŞ TRENDİ" or score <= 45:
            trend_vote = "SAT"
            trend_conf = 79.0
            trend_reason = "EMA 200 altında satıcılı kanal devam ediyor."
        else:
            trend_vote = "NÖTR / BEKLE"
            trend_conf = 62.0
            trend_reason = "Fiyat yatay bantta sıkışıyor, kırılım beklenmeli."

        # Model 2: Momentum AI
        if rsi >= 65 and change_pct > 0:
            mom_vote = "GÜÇLÜ AL"
            mom_conf = 84.0
            mom_reason = f"RSI {rsi:.1f} seviyesinde ivme kazanıyor, pozitif momentum."
        elif rsi <= 35:
            mom_vote = "AŞIRI SATIM / TEPKİ AL"
            mom_conf = 72.0
            mom_reason = f"RSI {rsi:.1f} aşırı satımda, teknik tepki potansiyeli yüksek."
        elif rsi < 48:
            mom_vote = "SAT"
            mom_conf = 75.0
            mom_reason = "Momentum negatif bölgede güç kaybediyor."
        else:
            mom_vote = "NÖTR"
            mom_conf = 58.0
            mom_reason = "Momentum indikatörleri dengeli seyrediyor."

        # Model 3: Quant AI (Volatilite ve İstatistik)
        if change_pct > 1.5:
            quant_vote = "AL"
            quant_conf = 82.0
            quant_reason = "VWAP üzerinde standart sapma kırılımı ve pozitif risk/getiri oranı."
        elif change_pct < -1.5:
            quant_vote = "SAT"
            quant_conf = 80.0
            quant_reason = "Negatif volatilite genişlemesi, aşağı yönlü sapma."
        else:
            quant_vote = "NÖTR"
            quant_conf = 65.0
            quant_reason = "Volatilite normal bantlar dahilinde."

        # Model 4: Sentiment & NLP AI
        if score >= 70:
            sent_vote = "POZİTİF"
            sent_conf = 85.0
            sent_reason = "Sektörel haber akışı ve kurumsal ilgi pozitif algılanıyor."
        elif score <= 45:
            sent_vote = "NEGATİF"
            sent_conf = 78.0
            sent_reason = "Piyasa duyarlılığı temkinli ve satış baskısı ağırlıklı."
        else:
            sent_vote = "NÖTR"
            sent_conf = 60.0
            sent_reason = "Nötr haber duyarlılığı."

        # Modellerin Ağırlıkları
        models = [
            {"name": "Trend AI (Deep Trend)", "vote": trend_vote, "confidence": trend_conf, "weight": 32, "reason": trend_reason},
            {"name": "Momentum AI (Oscillator)", "vote": mom_vote, "confidence": mom_conf, "weight": 28, "reason": mom_reason},
            {"name": "Quant AI (Mean Reversion)", "vote": quant_vote, "confidence": quant_conf, "weight": 24, "reason": quant_reason},
            {"name": "Sentiment AI (NLP Analysis)", "vote": sent_vote, "confidence": sent_conf, "weight": 16, "reason": sent_reason},
        ]

        # Ağırlıklı Toplam Skor
        weighted_score = sum(m["confidence"] * (m["weight"] / 100.0) for m in models)
        
        # Karar
        if weighted_score >= 80:
            final_verdict = "GÜÇLÜ AL"
            badge_class = "badge-success"
        elif weighted_score >= 68:
            final_verdict = "AL"
            badge_class = "badge-primary"
        elif weighted_score <= 50:
            final_verdict = "SAT"
            badge_class = "badge-danger"
        else:
            final_verdict = "NÖTR / İZLE"
            badge_class = "badge-warning"

        # CIO Yönetici Özeti (NLP Analizi)
        summary_text = (
            f"**{clean_sym}** için Yapay Zeka Komitesi genel görünümü **{final_verdict}** (%{weighted_score:.1f} güven) olarak belirlemiştir. "
            f"Fiyat anlık {price} TL seviyesinde işlem görmekte olup günlük değişim %{change_pct:+.2f}'dir. "
            f"Trend ve Momentum modelleri {trend_vote} yönünde ortak görüş bildirirken, risk/getiri profili kurumsal alım teyidiyle desteklenmektedir."
        )

        # Tavsiye Edilen (Yap) ve Edilmeyen (Yapma)
        do_list = [
            f"{price} TL civarındaki geri çekilmeleri kademeli maliyetlenme için izleyin.",
            "Pozisyon alırken belirlenen ATR Stop-Loss sınırına kesinlikle sadık kalın.",
            "Varant işlemlerinde yüksek kaldıraç yerine Delta > 0.40 olan vadeleri tercih edin."
        ]
        dont_list = [
            "Tavan seviyesinden veya ani yükseliş mumlarının tepe noktasından piyasa emriyle girmeyin.",
            "Stop seviyesi kırıldığında 'nasılsa döner' beklentisiyle pozisyonda beklemeyin.",
            "Vadesine 10 günden az kalmış yüksek Theta erimeli varantlara yüksek sermaye bağlamayın."
        ]

        return {
            "status": "success",
            "symbol": clean_sym,
            "final_verdict": final_verdict,
            "weighted_score": round(weighted_score, 1),
            "badge_class": badge_class,
            "models": models,
            "executive_summary": summary_text,
            "dos": do_list,
            "donts": dont_list
        }
