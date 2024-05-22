import telebot
import time
import os
from convert import download_terabox_video
from keep_alive import keep_alive

keep_alive()

def download_file(url):
    os.system(f"wget {url}")
    temp_name = url.split("/")[-1]
    os.system(f"cp {temp_name} {temp_name}.mp4")
    os.remove(temp_name)


TOKEN = os.environ["Token"]
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Send Link in format /link [url]")


@bot.message_handler(commands=["link"])
def link(message):
    link = message.text.split("https://")[-1].split("/s/")[-1]
    print(link)
    resp = download_terabox_video("https://terabox.hnn.workers.dev", link, None).replace(" ", "")
    bot.send_message(message.chat.id, resp)
    download_file(resp)
    time.sleep(2)
    with open(f"{resp.split("/")[-1]}.mp4", "rb") as vid:
      bot.send_video(message.chat.id, vid)
    os.remove(f"{resp.split("/")[-1]}.mp4")


@bot.message_handler(content_types=['text'])
def check_forwarded(message):
    link = message.text.split("https://")[-1].split("/s/")[-1]
    print(link)
    resp = download_terabox_video("https://terabox.hnn.workers.dev", link, None).replace(" ", "")
    bot.send_message(message.chat.id, resp)
    download_file(resp)
    time.sleep(2)
    with open(f"{resp.split("/")[-1]}.mp4", "rb") as vid:
      bot.send_video(message.chat.id, vid)
    os.remove(f"{resp.split("/")[-1]}.mp4")


while True:
    try:
        bot.polling()
    except:
        time.sleep(5)
