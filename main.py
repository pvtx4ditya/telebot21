import telebot
import time
import os
from convert import download_terabox_video
from keep_alive import keep_alive

keep_alive()

def download_file(url, name="video.mp4"):
  os.system(f"wget {url}")
  temp_name = url.split("/")[-1]
  os.system(f"cp {temp_name} {name}")
  os.remove(temp_name)


TOKEN = os.environ['Token']
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
  bot.send_message(message.chat.id, "Send Link in format /link [url]")


@bot.message_handler(commands=["link"])
def link(message):
  link = message.text.split(" ")[-1].replace(" ", "")
  resp = download_terabox_video("https://terabox.hnn.workers.dev", link,
                                None).replace(" ", "")
  bot.send_message(message.chat.id, resp)
  print(resp)
  download_file(resp, name="video.mp4")
  time.sleep(2)
  vid = open("video.mp4", "rb")
  bot.send_video(message.chat.id, vid)


@bot.message_handler(content_types=['text'])
def check_forwarded(message):
  try:
      link = message.text.replace(" ", "")
      resp = download_terabox_video("https://terabox.hnn.workers.dev", link,
                                    None).replace(" ", "")
      bot.send_message(message.chat.id, resp)
      print(resp)
      download_file(resp, name="video.mp4")
      time.sleep(2)
      vid = open("video.mp4", "rb")
      bot.send_video(message.chat.id, vid)
  except:
      bot.send_message(message.chat.id, "NO URL FOUND")


while True:
    try:
        bot.polling()
    except:
        time.sleep(5)
