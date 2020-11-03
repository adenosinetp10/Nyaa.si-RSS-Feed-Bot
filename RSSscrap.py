import requests
import time
import os
import lxml
from telegram import ParseMode
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

url = 'https://nyaa.si/?page=rss'
ADMIN_ID = 900986950


def start(update, context):
    user = update.message.from_user
    userID = user['id']
    if userID != ADMIN_ID:
        pass
    else:
        nyaa_id1=""
        while True:
            time.sleep(5)
            r = requests.get(url)
            soup = BeautifulSoup(r.content,features='xml')
            all_title = soup.findAll("title")
            all_download = soup.findAll("link")
            all_view = soup.findAll("guid",{"isPermaLink":"true"})
            all_hash = soup.findAll("nyaa:infoHash")
            all_date = soup.findAll("pubDate")
            all_size = soup.findAll("nyaa:size")
            all_category = soup.findAll("nyaa:category")
            spec_title = all_title[1].text
            spec_download = all_download[2].text
            spec_view = all_view[0].text
            spec_date = all_date[0].text
            spec_size = all_size[0].text
            spec_category = all_category[0].text
            spec_hash = all_hash[0].text
            nyaa_id = nyaa_id1
            if (nyaa_id!=spec_view):
                nyaa_id = spec_view
                nyaa_id1 = nyaa_id
                keyboard = [
                [
                InlineKeyboardButton("More Info",url = str(spec_view)),
                InlineKeyboardButton("Download\nTorrent",url = str(spec_download))]
                            ]
                reply_markup1 = InlineKeyboardMarkup(keyboard)

                update.message.reply_text("<b>Name : <pre>%s</pre></b>\n<b>Category :</b> <pre>%s</pre>\n<b>Size :</b> <pre>%s</pre>\n<b>Publish Date :</b> <pre>%s</pre>\n<b>Magnet Link :</b> <pre>magnet:?xt=urn:btih:%s</pre>"%(spec_title, spec_category, spec_size, spec_date.replace("-0000","GMT"),spec_hash),parse_mode = 'HTML', reply_markup = reply_markup1)
            return
    
def test(update,context):
    user = update.message.from_user
    text = update.message.text
    userID = user['id']
    if text == 'test':
        if userID != ADMIN_ID:
            update.message.reply_text("Auth Denied.")
            pass
        else:
            update.message.reply_text("Authorized.")
            return

def main():
    bot_token=os.environ.get("BOT_TOKEN","")
    updater = Updater(bot_token , use_context = True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',start,run_async = True))
    dp.add_handler(MessageHandler(Filters.text,test,run_async = True))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
