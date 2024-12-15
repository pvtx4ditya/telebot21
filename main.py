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
    bot.send_message(message.chat.id, "Send any message containing a link with 'tera' in it, and I'll download the video for you!")

def process_link(message, link):
    try:
        resp = download_terabox_video("https://terabox.hnn.workers.dev", link, None).replace(" ", "")
        bot.send_message(message.chat.id, "Downloading your video...")
        print(resp)
        download_file(resp, name="video.mp4")
        time.sleep(2)
        with open("video.mp4", "rb") as vid:
            bot.send_video(message.chat.id, vid)
    except Exception as e:
        bot.send_message(message.chat.id, f"Failed to process the link: {str(e)}")

@bot.message_handler(content_types=['text'])
def handle_message(message):
    # Check if the message contains a link with "tera"
    if "tera" in message.text.lower():
        link = message.text.strip()
        process_link(message, link)
    else:
        bot.send_message(message.chat.id, "No valid 'tera' link found in your message.")

while True:
    try:
        bot.polling()
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        time.sleep(5)
