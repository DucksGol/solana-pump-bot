# main.py

import asyncio
from solana_utils import buy_token, sell_token
from ai_filter import should_buy
from telegram_bot import run_telegram_bot
import logging
import time

logging.basicConfig(level=logging.INFO)

async def monitor_new_tokens():
    async with connect("wss://api.mainnet-beta.solana.com") as websocket:
        await websocket.account_subscribe(PublicKey("pump pubkey"))  # заменить на правильный фильтр
        while True:
            resp = await websocket.recv()
            mint_address = extract_mint(resp)
            if mint_address and should_buy(mint_address):
                profit = await trade_token(mint_address)
                if profit > 0:
                    log_trade(mint_address, profit)

def extract_mint(data):
    # реализация извлечения mint адреса
    return "TOKEN_MINT"

async def trade_token(mint):
    buy_token(mint)
    time.sleep(30)  # ждём роста
    profit = sell_token(mint)
    return profit

def log_trade(mint, profit):
    with open("logs/trades.log", "a") as f:
        f.write(f"{mint} | Profit: {profit}\n")

if __name__ == "__main__":
    asyncio.run(monitor_new_tokens())
    run_telegram_bot()
