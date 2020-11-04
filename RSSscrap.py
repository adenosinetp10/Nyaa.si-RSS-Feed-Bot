import requests
import random
import time
import os
import lxml
from telegram import ParseMode,Update
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

url = 'https://nyaa.si/?page=rss'
CHANNEL_ID = -1001340269031


def start(update:Update, context):
    if CHANNEL_ID != update.effective_chat.id:
        pass
    else:
        nyaa_id1 = ""
        iterCount = 1
        while True:
            print("--------------------")
            print("Iteration(s) : {}".format(iterCount))
            print("--------------------")
            print("Implementation of Random Requests...")
            randomSleep = random.randint(5,6)
            time.sleep(randomSleep)
            print("Request Sleep time : {}".format(randomSleep))
            r = requests.get(url)
            print("Nyaa.si URL Loaded...")
            soup = BeautifulSoup(r.content,features='xml')
            all_title = soup.findAll("title")
            all_download = soup.findAll("link")
            all_view = soup.findAll("guid",{"isPermaLink":"true"})
            all_hash = soup.findAll("nyaa:infoHash")
            all_date = soup.findAll("pubDate")
            all_size = soup.findAll("nyaa:size")
            all_category = soup.findAll("nyaa:category")
            print("Scrapping...")
            spec_title = all_title[1].text
            spec_download = all_download[2].text
            spec_view = all_view[0].text
            spec_date = all_date[0].text
            spec_size = all_size[0].text
            spec_category = all_category[0].text
            spec_hash = all_hash[0].text
            nyaa_id = nyaa_id1
            print("Finishing up...")
            print("End of Iteration : {}".format(iterCount))
            iterCount+=1
            print("Scrapped Data Loaded to Variables...")
            if (nyaa_id!=spec_view):
                nyaa_id = spec_view
                nyaa_id1 = nyaa_id
                print("Finishing up...")
                print("End of Iteration : {}".format(iterCount))
                iterCount+=1
                keyboard = [
                [
                InlineKeyboardButton("More Info",url = str(spec_view)),
                InlineKeyboardButton("Download\nTorrent",url = str(spec_download))]
                            ]
                reply_markup1 = InlineKeyboardMarkup(keyboard)

                update.effective_message.reply_text("<b>Name : <pre>%s</pre></b>\n<b>Category :</b> <pre>%s</pre>\n<b>Size :</b> <pre>%s</pre>\n<b>Publish Date :</b> <pre>%s</pre>\n<b>Magnet Link :</b> <pre>magnet:?xt=urn:btih:%s</pre>"%(spec_title, spec_category, spec_size, spec_date.replace("-0000","GMT"),spec_hash),parse_mode = 'HTML', reply_markup = reply_markup1,quote = False)     
            
    
def bruh(update:Update,context):
    if CHANNEL_ID != update.effective_chat.id:
        pass
    else:
        if update.effective_message.text=='test':
            update.effective_message.reply_text("Test Result : TRUE ",quote=False)
        else:
            return  
          
       
            

def main():
    bot_token=os.environ.get("BOT_TOKEN","")
    updater = Updater(bot_token , use_context = True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.sticker,start,run_async = True))
    dp.add_handler(MessageHandler(Filters.text,bruh,run_async = True))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
