import urllib.request
import json
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID   = os.environ.get("CHAT_ID")

SAHAM = {
    "ANTM": {"harga_beli": 3700, "lot": 6},
    "ICBP": {"harga_beli": 8175, "lot": 3},
}

def ambil_harga(simbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{simbol}.JK?interval=1d&range=1d"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            return data["chart"]["result"][0]["meta"]["regularMarketPrice"]
    except:
        return None

def kirim(pesan):
    url  = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = json.dumps({
        "chat_id": CHAT_ID,
        "text": pesan,
        "parse_mode": "HTML"
    }).encode()
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json"}
    )
    urllib.request.urlopen(req, timeout=10)

laporan = "📊 <b>CEK HARGA SAHAM SYARIAH</b>\n━━━━━━━━━━━━━━\n"

for nama, cfg in SAHAM.items():
    harga = ambil_harga(nama)
    if not harga:
        laporan += f"❓ {nama}: gagal ambil harga\n"
        continue
    pct = ((harga - cfg["harga_beli"]) / cfg["harga_beli"]) * 100
    pnl = (harga - cfg["harga_beli"]) * cfg["lot"] * 100
    tp  = cfg["harga_beli"] * 1.12
    cl  = cfg["harga_beli"] * 0.93
    if harga >= tp:
        status = "🟢 TAKE PROFIT!"
    elif harga <= cl:
        status = "🔴 CUT LOSS!"
    else:
        status = "🟡 HOLD"
    laporan += (
        f"\n{status} <b>{nama}</b>\n"
        f"Harga : Rp {harga:,.0f}\n"
        f"P/L   : {pct:+.1f}% | Rp {pnl:+,.0f}\n"
        f"TP    : Rp {tp:,.0f} | CL: Rp {cl:,.0f}\n"
    )

laporan += "\n━━━━━━━━━━━━━━\nBismillah 🤲"
kirim(laporan)
print("Terkirim!")
