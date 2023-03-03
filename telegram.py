import requests as rq

from params import  TELEGRAM_BOT_ID, TELEGRAM_CHAT_ID, TELEGRAM_URL


def send_message(message):
  response = rq.post(
      f'{TELEGRAM_URL}{TELEGRAM_BOT_ID}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&parse_mode=Markdown&text={message}')

  return response
