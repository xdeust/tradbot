import sys
from fastapi.testclient import TestClient
from main import app

print("=== TRADBOT PRO E2E VERIFICATION TEST ===")
with TestClient(app) as client:
    # 1. Root / UI
    r = client.get("/")
    assert r.status_code == 200, f"Root failed: {r.status_code}"
    print("[PASS] 1. GET / -> Index HTML served")

    # 2. Static Assets
    r_css = client.get("/style.css")
    assert r_css.status_code == 200, f"CSS failed: {r_css.status_code}"
    r_js = client.get("/app.js")
    assert r_js.status_code == 200, f"JS failed: {r_js.status_code}"
    r_lw = client.get("/lightweight-charts.js")
    assert r_lw.status_code == 200, f"LW Charts failed: {r_lw.status_code}"
    print("[PASS] 2. Static Assets (style.css, app.js, lightweight-charts.js) served")

    # 3. Heartbeat
    r_hb = client.get("/api/heartbeat")
    assert r_hb.status_code == 200
    print("[PASS] 3. GET /api/heartbeat ->", r_hb.json()["server_time"])

    # 4. Autocomplete
    r_ac = client.get("/api/autocomplete?q=THY")
    assert r_ac.status_code == 200
    assert len(r_ac.json()) > 0
    print("[PASS] 4. GET /api/autocomplete ->", r_ac.json()[0]["symbol"], r_ac.json()[0]["name"])

    # 5. Dashboard Init
    r_dash = client.get("/api/dashboard_init")
    assert r_dash.status_code == 200
    dash_data = r_dash.json()
    assert dash_data["status"] == "success"
    print(f"[PASS] 5. GET /api/dashboard_init -> Analyzed: {dash_data.get('total_analyzed')}")

    # 6. Deep Analyze
    r_ana = client.get("/api/analyze?symbol=THYAO")
    assert r_ana.status_code == 200
    ana_data = r_ana.json()
    assert "summary" in ana_data
    assert "ai_committee" in ana_data
    assert "trade_desk" in ana_data
    assert "akd" in ana_data
    assert "lstm_projection" in ana_data
    print(f"[PASS] 6. GET /api/analyze?symbol=THYAO -> Price: {ana_data['price']}, AI: {ana_data['ai_committee']['final_verdict']}, TP1: {ana_data['trade_desk']['tp1']}")

    # 7. Varant Simulator
    r_var = client.get("/api/varant_simulator?symbol=THYAO&price=300&target=315&issuer=%C4%B0%C5%9F%20Yat%C4%B1r%C4%B1m")
    assert r_var.status_code == 200
    var_data = r_var.json()
    assert len(var_data["warrants"]) > 0
    print(f"[PASS] 7. GET /api/varant_simulator -> {len(var_data['warrants'])} warrants generated with Greeks")

    # 8. Chart Data
    r_chart = client.get("/api/chart_data?symbol=THYAO&interval=1d")
    assert r_chart.status_code == 200
    chart_data = r_chart.json()
    assert len(chart_data["candles"]) > 0
    print(f"[PASS] 8. GET /api/chart_data -> {len(chart_data['candles'])} candles loaded for TradingView")

    # 9. Brokerage AKD
    r_brok = client.get("/api/brokerage/THYAO")
    assert r_brok.status_code == 200
    print(f"[PASS] 9. GET /api/brokerage/THYAO -> {len(r_brok.json()['buyers'])} buyers, {len(r_brok.json()['sellers'])} sellers")

    # 10. News Global & Ticker
    r_ng = client.get("/api/news/global")
    assert r_ng.status_code == 200
    r_nt = client.get("/api/news/ticker/THYAO")
    assert r_nt.status_code == 200
    print(f"[PASS] 10. GET /api/news -> Global ({len(r_ng.json()['news'])}), Ticker ({len(r_nt.json()['news'])})")

    # 11. KPI & Simulation
    r_win = client.get("/api/winrate_stats")
    assert r_win.status_code == 200
    r_tav = client.get("/api/tavan_history")
    assert r_tav.status_code == 200
    r_sim = client.get("/api/simulation/live_orders")
    assert r_sim.status_code == 200
    r_pnl = client.get("/api/simulation/daily_pnl")
    assert r_pnl.status_code == 200
    print("[PASS] 11. KPI, Tavan History, Live Orders, Daily PnL all OK")

print("\n=== [SUCCESS] ALL 11 END-TO-END TESTS PASSED SUCCESSFULLY! ===")
