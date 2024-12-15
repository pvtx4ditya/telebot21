import telebot
import time
import os
from convert import download_terabox_video
from keep_alive import keep_alive

keep_alive()

def download_file(url, name="video.mp4"):
    os.system(f"wget {url}")
    temp_name = url.split("/")[-1]
    os.system(f"mv {temp_name} {name}")

def process_link_and_send_video(bot, chat_id, link):
    try:
        link = link.replace(" ", "")
        resp = download_terabox_video("https://terabox.hnn.workers.dev", link, None).replace(" ", "")
        bot.send_message(chat_id, "Downloading your video...")
        download_file(resp, name="video.mp4")
        time.sleep(2)
        with open("video.mp4", "rb") as vid:
            bot.send_video(chat_id, vid)
    except Exception as e:
        bot.send_message(chat_id, f"Error: {str(e)}")

TOKEN = os.environ['Token']
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Send a link in the format: /link [url]")

@bot.message_handler(commands=["link"])
def link(message):
    link = message.text.split(" ", 1)[-1].strip()
    process_link_and_send_video(bot, message.chat.id, link)

@bot.message_handler(content_types=['text'])
def check_forwarded(message):
    process_link_and_send_video(bot, message.chat.id, message.text)

while True:
    try:
        bot.polling()
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        time.sleep(5)
