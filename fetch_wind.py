#!/usr/bin/env python3
"""
fetch_wind.py
由 GitHub Actions 在雲端定時執行，抓取天文台十分鐘風速 CSV，
轉存為 wind_data.json，供 index.html 同源讀取（無 CORS 問題）。

本機測試用法:
  python fetch_wind.py          # 執行一次
  python fetch_wind.py --loop   # 每 5 分鐘自動更新
"""
import csv, io, json, sys, time, urllib.request

HKO_WIND_CSV = "https://data.weather.gov.hk/weatherAPI/hko_data/regional-weather/latest_10min_wind.csv"
OUTPUT_FILE  = "wind_data.json"

def fetch_once():
    req = urllib.request.Request(HKO_WIND_CSV, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        raw = resp.read().decode("utf-8", errors="ignore")
    records = []
    for line in raw.strip().split("\n")[1:]:
        cols = [c.strip().strip('"') for c in line.split(",")]
        if len(cols) >= 5:
            records.append({
                "station":   cols[1],
                "direction": cols[2],
                "speed":     cols[3],
                "gust":      cols[4],
            })
    payload = {"updated_at": time.strftime("%Y-%m-%d %H:%M:%S"), "records": records}
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"[OK] {payload['updated_at']} → {len(records)} 筆資料寫入 {OUTPUT_FILE}")

if __name__ == "__main__":
    if "--loop" in sys.argv:
        while True:
            try: fetch_once()
            except Exception as e: print(f"[ERROR] {e}")
            time.sleep(300)
    else:
        fetch_once()
