"""
Tradbot - BIST ve Varant Sembol Tanımlamaları ve Arama Yardımcıları
"""

# BIST Hisse Senetleri ve Şirket Ünvanları Listesi
BIST_STOCKS = [
    # BIST 30 & Major Stocks
    {"symbol": "THYAO", "name": "Türk Hava Yolları", "sector": "Ulaştırma", "has_warrant": True},
    {"symbol": "EREGL", "name": "Ereğli Demir Çelik", "sector": "Demir Çelik", "has_warrant": True},
    {"symbol": "GARAN", "name": "Garanti Bankası", "sector": "Bankacılık", "has_warrant": True},
    {"symbol": "AKBNK", "name": "Akbank", "sector": "Bankacılık", "has_warrant": True},
    {"symbol": "ISCTR", "name": "İş Bankası (C)", "sector": "Bankacılık", "has_warrant": True},
    {"symbol": "YKBNK", "name": "Yapı ve Kredi Bankası", "sector": "Bankacılık", "has_warrant": True},
    {"symbol": "TUPRS", "name": "Tüpraş", "sector": "Petrol & Kimya", "has_warrant": True},
    {"symbol": "ASELS", "name": "Aselsan", "sector": "Savunma & Teknoloji", "has_warrant": True},
    {"symbol": "BIMAS", "name": "BİM Mağazalar", "sector": "Perakende", "has_warrant": True},
    {"symbol": "SAHOL", "name": "Sabancı Holding", "sector": "Holding", "has_warrant": True},
    {"symbol": "KCHOL", "name": "Koç Holding", "sector": "Holding", "has_warrant": True},
    {"symbol": "PGSUS", "name": "Pegasus Hava Taşımacılığı", "sector": "Ulaştırma", "has_warrant": True},
    {"symbol": "FROTO", "name": "Ford Otosan", "sector": "Otomotiv", "has_warrant": True},
    {"symbol": "TOASO", "name": "Tofaş Oto Fabrikaları", "sector": "Otomotiv", "has_warrant": True},
    {"symbol": "SISE", "name": "Şişecam", "sector": "Cam & Sanayi", "has_warrant": True},
    {"symbol": "PETKM", "name": "Petkim", "sector": "Petrokimya", "has_warrant": True},
    {"symbol": "KOZAL", "name": "Koza Altın", "sector": "Madencilik", "has_warrant": True},
    {"symbol": "EKGYO", "name": "Emlak Konut GYO", "sector": "GYO", "has_warrant": True},
    {"symbol": "TCELL", "name": "Turkcell", "sector": "Telekomünikasyon", "has_warrant": True},
    {"symbol": "TTKOM", "name": "Türk Telekom", "sector": "Telekomünikasyon", "has_warrant": True},
    {"symbol": "ASTOR", "name": "Astor Enerji", "sector": "Enerji", "has_warrant": True},
    {"symbol": "SASA", "name": "Sasa Polyester", "sector": "Kimya & Tekstil", "has_warrant": True},
    {"symbol": "HEKTS", "name": "Hektaş", "sector": "Tarım & Kimya", "has_warrant": True},
    {"symbol": "ENKAI", "name": "Enka İnşaat", "sector": "İnşaat & Taahhüt", "has_warrant": True},
    {"symbol": "ALARK", "name": "Alarko Holding", "sector": "Holding & Enerji", "has_warrant": True},
    {"symbol": "KONTR", "name": "Kontrolmatik Teknoloji", "sector": "Enerji & Teknoloji", "has_warrant": True},
    {"symbol": "EUPWR", "name": "Europower Enerji", "sector": "Enerji", "has_warrant": True},
    {"symbol": "GESAN", "name": "Girişim Elektrik", "sector": "Enerji", "has_warrant": True},
    {"symbol": "GUBRF", "name": "Gübre Fabrikaları", "sector": "Gübre & Kimya", "has_warrant": True},
    {"symbol": "ODAS", "name": "Odaş Elektrik", "sector": "Enerji & Maden", "has_warrant": True},
    {"symbol": "CWENE", "name": "CW Enerji", "sector": "Güneş Enerjisi", "has_warrant": True},
    {"symbol": "MIATK", "name": "Mia Teknoloji", "sector": "Yazılım & Bilişim", "has_warrant": True},
    {"symbol": "REEDR", "name": "Reeder Teknoloji", "sector": "Teknoloji", "has_warrant": True},
    {"symbol": "TABGD", "name": "TAB Gıda", "sector": "Gıda & Restoran", "has_warrant": True},
    {"symbol": "SDTTR", "name": "SDT Uzay ve Savunma", "sector": "Savunma", "has_warrant": True},
    {"symbol": "SOKM", "name": "Şok Marketler", "sector": "Perakende", "has_warrant": True},
    {"symbol": "MGROS", "name": "Migros Ticaret", "sector": "Perakende", "has_warrant": True},
    {"symbol": "CCOLA", "name": "Coca-Cola İçecek", "sector": "İçecek", "has_warrant": True},
    {"symbol": "AEFES", "name": "Anadolu Efes", "sector": "İçecek", "has_warrant": True},
    {"symbol": "DOHOL", "name": "Doğan Holding", "sector": "Holding", "has_warrant": True},
    {"symbol": "ARCLK", "name": "Arçelik", "sector": "Dayanıklı Tüketim", "has_warrant": True},
    {"symbol": "BRISA", "name": "Brisa", "sector": "Otomotiv Yan Sanayi", "has_warrant": False},
    {"symbol": "KORDS", "name": "Kordsa Teknik Tekstil", "sector": "Tekstil & Sanayi", "has_warrant": False},
    {"symbol": "MAVI", "name": "Mavi Giyim", "sector": "Tekstil & Perakende", "has_warrant": False},
    {"symbol": "TKFEN", "name": "Tekfen Holding", "sector": "Taahhüt & Tarım", "has_warrant": True},
    {"symbol": "VESTL", "name": "Vestel Elektronik", "sector": "Dayanıklı Tüketim", "has_warrant": False},
    {"symbol": "VESBE", "name": "Vestel Beyaz Eşya", "sector": "Dayanıklı Tüketim", "has_warrant": False},
    {"symbol": "BSOKE", "name": "Batısöke Çimento", "sector": "Çimento", "has_warrant": False},
    {"symbol": "BTCIM", "name": "Batıçim Çimento", "sector": "Çimento", "has_warrant": False},
    {"symbol": "CIMSA", "name": "Çimsa", "sector": "Çimento", "has_warrant": False},
    {"symbol": "AKCNS", "name": "Akçansa", "sector": "Çimento", "has_warrant": False},
    {"symbol": "OYAKC", "name": "Oyak Çimento", "sector": "Çimento", "has_warrant": True},
    {"symbol": "ISGYO", "name": "İş GYO", "sector": "GYO", "has_warrant": False},
    {"symbol": "TRGYO", "name": "Torunlar GYO", "sector": "GYO", "has_warrant": False},
    {"symbol": "KZBGY", "name": "Kızılbük GYO", "sector": "GYO", "has_warrant": False},
    {"symbol": "SNGYO", "name": "Sinpaş GYO", "sector": "GYO", "has_warrant": False},
    {"symbol": "KLGYO", "name": "Kiler GYO", "sector": "GYO", "has_warrant": False},
    {"symbol": "VAKBN", "name": "Vakıfbank", "sector": "Bankacılık", "has_warrant": True},
    {"symbol": "HALKB", "name": "Halkbank", "sector": "Bankacılık", "has_warrant": True},
    {"symbol": "TSKB", "name": "TSKB", "sector": "Bankacılık", "has_warrant": False},
    {"symbol": "ALBRK", "name": "Albaraka Türk", "sector": "Bankacılık", "has_warrant": False},
    {"symbol": "SKBNK", "name": "Şekerbank", "sector": "Bankacılık", "has_warrant": False},
    {"symbol": "KOZAA", "name": "Koza Madencilik", "sector": "Madencilik", "has_warrant": True},
    {"symbol": "IPEKE", "name": "İpek Doğal Enerji", "sector": "Madencilik & Enerji", "has_warrant": False},
    {"symbol": "CANTE", "name": "Çan2 Termik", "sector": "Enerji", "has_warrant": False},
    {"symbol": "BRSAN", "name": "Borusan Birleşik Boru", "sector": "Boru & Çelik", "has_warrant": True},
    {"symbol": "KCAER", "name": "Kocaer Çelik", "sector": "Çelik", "has_warrant": False},
    {"symbol": "QUAGR", "name": "Qua Granite", "sector": "Yapı Malzemeleri", "has_warrant": False},
    {"symbol": "ALFAS", "name": "Alfa Solar Enerji", "sector": "Güneş Enerjisi", "has_warrant": False},
    {"symbol": "KOPOL", "name": "Koza Polyester", "sector": "Kimya", "has_warrant": False},
    {"symbol": "AGROT", "name": "Agrotech Yüksek Teknoloji", "sector": "Teknoloji & Tarım", "has_warrant": False},
    {"symbol": "KLYSN", "name": "Kalyon Güneş", "sector": "Enerji", "has_warrant": False},
    {"symbol": "TAVHL", "name": "TAV Havalimanları", "sector": "Havacılık", "has_warrant": True},
    {"symbol": "DOAS", "name": "Doğuş Otomotiv", "sector": "Otomotiv Ticaret", "has_warrant": True},
    {"symbol": "TTRAK", "name": "Türk Traktör", "sector": "Otomotiv", "has_warrant": True},
    {"symbol": "OTKAR", "name": "Otokar", "sector": "Otomotiv & Savunma", "has_warrant": False},
    {"symbol": "AKFYE", "name": "Akfen Yenilenebilir Enerji", "sector": "Enerji", "has_warrant": False},
    {"symbol": "ZOREN", "name": "Zorlu Enerji", "sector": "Enerji", "has_warrant": False},
    {"symbol": "AYDEM", "name": "Aydem Enerji", "sector": "Enerji", "has_warrant": False},
    {"symbol": "GWIND", "name": "Galata Wind Enerji", "sector": "Rüzgar Enerjisi", "has_warrant": False},
    {"symbol": "GENIL", "name": "Gen İlaç", "sector": "İlaç & Sağlık", "has_warrant": False},
    {"symbol": "ECILC", "name": "Eczacıbaşı İlaç", "sector": "İlaç & Sağlık", "has_warrant": False},
    {"symbol": "DEVA", "name": "Deva Holding", "sector": "İlaç", "has_warrant": False},
    {"symbol": "SELEC", "name": "Selçuk Ecza Deposu", "sector": "Sağlık Dağıtım", "has_warrant": False},
    {"symbol": "EGEEN", "name": "Ege Endüstri", "sector": "Otomotiv Parça", "has_warrant": False},
    {"symbol": "KONYA", "name": "Konya Çimento", "sector": "Çimento", "has_warrant": False},
    {"symbol": "GOLTS", "name": "Göltaş Çimento", "sector": "Çimento", "has_warrant": False},
    {"symbol": "BOBET", "name": "Boğaziçi Beton", "sector": "Hazır Beton", "has_warrant": False},
    {"symbol": "ISMEN", "name": "İş Yatırım Menkul Değerler", "sector": "Aracı Kurum", "has_warrant": False},
    {"symbol": "OSMEN", "name": "Osmanlı Menkul", "sector": "Aracı Kurum", "has_warrant": False},
    {"symbol": "INFO", "name": "İnfo Yatırım", "sector": "Aracı Kurum", "has_warrant": False},
    {"symbol": "GEDIK", "name": "Gedik Yatırım", "sector": "Aracı Kurum", "has_warrant": False},
    {"symbol": "GLYHO", "name": "Global Yatırım Holding", "sector": "Holding & Liman", "has_warrant": False},
    {"symbol": "AGHOL", "name": "Anadolu Grubu Holding", "sector": "Holding", "has_warrant": False},
    {"symbol": "BERA", "name": "Bera Holding", "sector": "Holding", "has_warrant": False},
    {"symbol": "KMPUR", "name": "Kimteks Poliüretan", "sector": "Kimya", "has_warrant": False},
    {"symbol": "KARTN", "name": "Kartonsan", "sector": "Ambalaj & Kağıt", "has_warrant": False},
    {"symbol": "TURSG", "name": "Türkiye Sigorta", "sector": "Sigortacılık", "has_warrant": False},
    {"symbol": "ANSGR", "name": "Anadolu Sigorta", "sector": "Sigortacılık", "has_warrant": False},
    {"symbol": "AKGRT", "name": "Aksigorta", "sector": "Sigortacılık", "has_warrant": False},
    {"symbol": "AGESA", "name": "Agesa Hayat ve Emeklilik", "sector": "Bireysel Emeklilik", "has_warrant": False},
]

# Varant İhraççıları
WARRANT_ISSUERS = [
    "İş Yatırım",
    "Ak Yatırım",
    "Garanti BBVA",
    "Ahlatcı Yatırım"
]

# Varant Dayanak Varlıkları (Hisse, Endeks ve Emtia)
WARRANT_UNDERLYINGS = [
    {"symbol": "THYAO", "name": "Türk Hava Yolları", "type": "Hisse", "default_target_pct": 5.0},
    {"symbol": "EREGL", "name": "Ereğli Demir Çelik", "type": "Hisse", "default_target_pct": 4.5},
    {"symbol": "GARAN", "name": "Garanti Bankası", "type": "Hisse", "default_target_pct": 4.0},
    {"symbol": "AKBNK", "name": "Akbank", "type": "Hisse", "default_target_pct": 4.0},
    {"symbol": "ISCTR", "name": "İş Bankası (C)", "type": "Hisse", "default_target_pct": 4.0},
    {"symbol": "YKBNK", "name": "Yapı Kredi", "type": "Hisse", "default_target_pct": 4.5},
    {"symbol": "TUPRS", "name": "Tüpraş", "type": "Hisse", "default_target_pct": 3.5},
    {"symbol": "ASELS", "name": "Aselsan", "type": "Hisse", "default_target_pct": 5.0},
    {"symbol": "BIMAS", "name": "BİM Mağazalar", "type": "Hisse", "default_target_pct": 3.5},
    {"symbol": "SAHOL", "name": "Sabancı Holding", "type": "Hisse", "default_target_pct": 4.0},
    {"symbol": "KCHOL", "name": "Koç Holding", "type": "Hisse", "default_target_pct": 3.5},
    {"symbol": "PGSUS", "name": "Pegasus", "type": "Hisse", "default_target_pct": 5.5},
    {"symbol": "FROTO", "name": "Ford Otosan", "type": "Hisse", "default_target_pct": 4.0},
    {"symbol": "TOASO", "name": "Tofaş", "type": "Hisse", "default_target_pct": 4.5},
    {"symbol": "SISE", "name": "Şişecam", "type": "Hisse", "default_target_pct": 4.0},
    {"symbol": "PETKM", "name": "Petkim", "type": "Hisse", "default_target_pct": 5.0},
    {"symbol": "KOZAL", "name": "Koza Altın", "type": "Hisse", "default_target_pct": 5.0},
    {"symbol": "EKGYO", "name": "Emlak Konut", "type": "Hisse", "default_target_pct": 6.0},
    {"symbol": "TCELL", "name": "Turkcell", "type": "Hisse", "default_target_pct": 3.5},
    {"symbol": "TTKOM", "name": "Türk Telekom", "type": "Hisse", "default_target_pct": 4.0},
    {"symbol": "ASTOR", "name": "Astor Enerji", "type": "Hisse", "default_target_pct": 6.5},
    {"symbol": "SASA", "name": "Sasa Polyester", "type": "Hisse", "default_target_pct": 6.0},
    {"symbol": "HEKTS", "name": "Hektaş", "type": "Hisse", "default_target_pct": 6.0},
    {"symbol": "XU030", "name": "BIST 30 Endeksi", "type": "Endeks", "default_target_pct": 2.5},
    {"symbol": "ONSALTIN", "name": "Ons Altın (XAU/USD)", "type": "Emtia", "default_target_pct": 2.0},
    {"symbol": "BRENT", "name": "Brent Petrol", "type": "Emtia", "default_target_pct": 3.0},
    {"symbol": "DAX", "name": "DAX 40 Endeksi", "type": "Yabancı Endeks", "default_target_pct": 2.0},
    {"symbol": "SPX", "name": "S&P 500 Endeksi", "type": "Yabancı Endeks", "default_target_pct": 1.5},
]

def clean_symbol(sym: str) -> str:
    """Sembolü temizler ve büyük harfe çevirir (örn. thyao.is -> THYAO)"""
    if not sym:
        return ""
    sym = sym.strip().upper()
    if sym.endswith(".IS"):
        sym = sym[:-3]
    return sym

def to_yfinance_symbol(sym: str) -> str:
    """Temiz sembolü Yahoo Finance formatına çevirir (örn. THYAO -> THYAO.IS)"""
    clean = clean_symbol(sym)
    if clean in ["XU030", "XU100"]:
        return "^" + clean
    if clean == "ONSALTIN":
        return "GC=F"
    if clean == "BRENT":
        return "BZ=F"
    if clean == "DAX":
        return "^GDAXI"
    if clean == "SPX":
        return "^GSPC"
    return f"{clean}.IS"

def search_symbols(query: str, limit: int = 10) -> list:
    """Arama sorgusuna göre eşleşen hisseleri filtreler"""
    if not query:
        return BIST_STOCKS[:limit]
    
    q = query.strip().upper()
    matches = []
    for item in BIST_STOCKS:
        if q in item["symbol"].upper() or q in item["name"].upper() or q in item["sector"].upper():
            matches.append(item)
            if len(matches) >= limit:
                break
    return matches
