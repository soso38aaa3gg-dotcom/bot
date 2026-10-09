import os
import yfinance as yf
import matplotlib.pyplot as plt
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلا! البوت شغال ✅\nارسل /price AAPL أو /chart AAPL")

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("اكتب: /price AAPL")
        return
    symbol = context.args[0].upper()
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        if data.empty:
            await update.message.reply_text("الرمز غير موجود")
            return
        price_val = data['Close'].iloc[-1]
        await update.message.reply_text(f"{symbol} سعره: ${price_val:.2f}")
    except Exception as e:
        await update.message.reply_text(f"خطأ: {e}")

async def chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("اكتب: /chart AAPL")
        return
    symbol = context.args[0].upper()
    try:
        data = yf.download(symbol, period="1mo", interval="1d")
        plt.figure()
        plt.plot(data['Close'])
        plt.title(f"{symbol}")
        plt.savefig("chart.png")
        plt.close()
        await update.message.reply_photo(photo=open("chart.png","rb"), caption=f"شارت {symbol} لآخر شهر")
    except Exception as e:
        await update.message.reply_text(f"خطأ: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("price", price))
app.add_handler(CommandHandler("chart", chart))
app.run_polling()
