import yfinance as yf
import logging, os
import asyncio, telegram, time, pytz
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
botToken = os.environ.get('token')
chatId = os.environ.get('main_chat_id')

def getData():
    tickerList = ["SCHD", "QQQM", "BRK-A", "IXJ", "SMH"]
    data = []

    for t in tickerList:
        ticker = yf.Ticker(t)
        df = ticker.history(period='5d', interval='1d', prepost=False)

        lastDayClosePrice = df.iloc[3, 3]
        TodayClosePrice = df.iloc[4, 3]
        change = round(TodayClosePrice - lastDayClosePrice, 2)
        changeP = round((TodayClosePrice - lastDayClosePrice) / lastDayClosePrice * 100 , 2)
        data.append([t, round(TodayClosePrice, 2), change, changeP])
    return data

async def send_message(bot):
    msg = ""    
    data = getData()

    for d in data:
        if d[2] >= 0:
            msg += "🔴 {} : {}$ 🔺{}$ ({}%)\n".format(d[0], d[1], d[2], d[3])
        else:
            msg += "🔵 {} : {}$ 🔻{}$ ({}%)\n".format(d[0], d[1], d[2], d[3])
        
    await bot.send_message(chatId,msg)

async def main():
    print("starting service...")

    timeZone = pytz.timezone('Asia/Seoul')

    now = datetime.now(timeZone)
    target = now.replace(hour=6, minute=0, second=0, microsecond=0)
    
    if now >= target:
        target += timedelta(days=1)
    timeRemaining = target - now
    secondsRemaining = timeRemaining.total_seconds()

    bot = telegram.Bot(token = botToken)
    await send_message(bot)
    
    time.sleep(secondsRemaining)
    while True:
        await send_message(bot)
        time.sleep(86400)

if __name__ == "__main__":
    asyncio.run(main())


