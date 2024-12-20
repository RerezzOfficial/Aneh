
import MetaTrader5 as mt5
import pandas as pd
import numpy as np

Pengaturan akun FBS
akun = "Nomor Akun Anda"
password = "Kata Sandi Anda"
server = "FBS-Real"

Pengaturan symbol dan timeframe
symbol = "EURUSD"
timeframe = mt5.TIMEFRAME_M1

Fungsi analisis teknikal
def analisis_teknikal():
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 100)
    df = pd.DataFrame(rates)
    
    # Moving Average
    df['MA_50'] = df['close'].rolling(window=50).mean()
    df['MA_200'] = df['close'].rolling(window=200).mean()
    
    # RSI
    delta = df['close'].diff()
    gain, loss = delta.copy(), delta.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = abs(loss).rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Kondisi beli
    if df['MA_50'].iloc[-1] > df['MA_200'].iloc[-1] and df['RSI'].iloc[-1] < 30:
        return True
    else:
        return False

Fungsi membeli
def beli():
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": 0.1,
        "type": mt5.OP_BUY,
        "price": mt5.symbol_info_tick(symbol).bid,
        "deviation": 20,
        "magic": 234000,
        "comment": "Robot Trading",
        "type_time": mt5.TIME_GTC
    }
    result = mt5.order_send(request)
    print("Order beli berhasil")

Fungsi menjual
def jual():
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": 0.1,
        "type": mt5.OP_SELL,
        "price": mt5.symbol_info_tick(symbol).ask,
        "deviation": 20,
        "magic": 234000,
        "comment": "Robot Trading",
        "type_time": mt5.TIME_GTC
    }
    result = mt5.order_send(request)
    print("Order jual berhasil")

Eksekusi trade
def eksekusi_trade():
    if analisis_teknikal():
        beli()
    else:
        jual()

Jalankan robot trading
mt5.initialize()
mt5.login(akun, password, server)
while True:
    eksekusi_trade()
    time.sleep(60)
