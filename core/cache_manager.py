"""
Tradbot - Bellek İçi Önbellek ve Arka Plan Senkronizasyon Yöneticisi (Cache Manager)
Terminalin anlık ve gecikmesiz çalışması için verileri RAM'de tutar ve periyodik günceller.
"""

import time
import json
import os
import threading
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger("CacheManager")

class CacheManager:
    """Tüm sistem verilerini önbelleğe alan ve asenkron güncelleyen sınıf"""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(CacheManager, cls).__new__(cls)
                cls._instance._init_cache()
            return cls._instance

    def _init_cache(self):
        self.cache: Dict[str, Any] = {
            "dashboard_data": {},
            "stocks_analysis": {},
            "warrants": {},
            "chart_data": {},
            "news_global": [],
            "news_ticker": {},
            "brokerage_sim": {},
            "simulation_orders": [],
            "simulation_pnl": {},
            "winrate_stats": {},
            "last_updated": None,
            "total_analyzed": 0,
            "is_scanning": False
        }
        self.cache_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        os.makedirs(self.cache_dir, exist_ok=True)
        self.backup_file = os.path.join(self.cache_dir, "cache_backup.json")
        self._load_from_disk()

    def get(self, key: str, default: Any = None) -> Any:
        """Önbellekten veri oku"""
        with self._lock:
            return self.cache.get(key, default)

    def set(self, key: str, value: Any):
        """Önbelleğe veri yaz"""
        with self._lock:
            self.cache[key] = value

    def get_stock_analysis(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Hisse özel analizini önbellekten oku"""
        with self._lock:
            return self.cache["stocks_analysis"].get(symbol.upper())

    def set_stock_analysis(self, symbol: str, analysis: Dict[str, Any]):
        """Hisse analizini önbelleğe kaydet"""
        with self._lock:
            self.cache["stocks_analysis"][symbol.upper()] = analysis

    def get_chart_data(self, symbol: str, interval: str) -> Optional[list]:
        """Grafik verisini önbellekten oku"""
        key = f"{symbol.upper()}_{interval}"
        with self._lock:
            return self.cache["chart_data"].get(key)

    def set_chart_data(self, symbol: str, interval: str, data: list):
        """Grafik verisini önbelleğe kaydet"""
        key = f"{symbol.upper()}_{interval}"
        with self._lock:
            self.cache["chart_data"][key] = data

    def save_to_disk(self):
        """Önbelleğin kritik özetini diske kaydeder (yedekleme)"""
        try:
            with self._lock:
                save_data = {
                    "dashboard_data": self.cache.get("dashboard_data", {}),
                    "winrate_stats": self.cache.get("winrate_stats", {}),
                    "simulation_orders": self.cache.get("simulation_orders", []),
                    "simulation_pnl": self.cache.get("simulation_pnl", {}),
                    "last_updated": self.cache.get("last_updated"),
                    "total_analyzed": self.cache.get("total_analyzed", 0)
                }
                with open(self.backup_file, "w", encoding="utf-8") as f:
                    json.dump(save_data, f, ensure_ascii=False, indent=2)
            logger.info("Önbellek diske yedeklendi.")
        except Exception as e:
            logger.error(f"Önbellek diske kaydedilirken hata: {e}")

    def _load_from_disk(self):
        """Başlangıçta diskteki son önbellek yedeğini yükler"""
        if os.path.exists(self.backup_file):
            try:
                with open(self.backup_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.cache.update(data)
                logger.info(f"Disk yedeğinden önbellek yüklendi (Son güncelleme: {self.cache.get('last_updated')})")
            except Exception as e:
                logger.error(f"Önbellek diskten yüklenirken hata: {e}")

# Global Cache Singleton
cache = CacheManager()
