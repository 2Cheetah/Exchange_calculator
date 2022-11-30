#!/usr/bin/python
from aiogram import Bot, Dispatcher, executor, types
from get_google_exchange_rates import get_exchange_rate_from_google_finance
from keys import API_TOKEN
import re


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
@dp.message_handler(commands=['start']) 
async def send_welcome(message: types.Message):
   await message.reply("""
Send a pair of currencies to get exchange rate from Google Finance. For instance: 'usd rub' or 'btc usdt'.
Another option is to use the bot as an exchange calculator. Try typing '105.33 usdt btc'.
   """)


@dp.message_handler()
async def exchange_rate(message: types.Message):
   exchange_amount = re.findall(r"\d+\.?,?\d*", message.text)
   currency_list = re.findall(r"[a-zA-Z]{4}|[a-zA-Z]{3}", message.text)
   try:
      cur1 = currency_list[0].upper()
      cur2 = currency_list[1].upper()
      await message.answer(f"Trying to fetch exchange rate for a pair {cur1}-{cur2} from Google Finance")
      try:
         exchange_rate = get_exchange_rate_from_google_finance(cur1, cur2)
         reply = f"Exchange rate for {cur1}-{cur2} is {exchange_rate}"
         await message.answer(reply)
         if exchange_amount:
            await message.answer(f"{exchange_amount[0].replace(',','.')} of {cur1} = {float(exchange_amount[0].replace(',','.'))*exchange_rate} of {cur2}")
      except:
         await message.answer(f"Can't process provided data \"{message.text}\"")
   except IndexError:
      await message.answer(f"Can't process provided data \"{message.text}\"")


if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)
