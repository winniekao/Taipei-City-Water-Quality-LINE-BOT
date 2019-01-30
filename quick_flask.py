from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, LocationMessage
)
import subprocess
import threading
import pickle
import codecs
import math
app = Flask(__name__)


line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

#def get_taipei_data():
#    subprocess.call(['python3','./test.py'])
#    timer = threading.Timer(900, get_taipei_data)
#    timer.start()



@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    print("user_id=", user_id)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    subprocess.call(['python3','./test.py'])
    all_stop = pickle.load(codecs.open('./all_stop.p','rb'))
    lat = event.message.latitude
    long = event.message.longitude
    dist_dic = {}
    for value in all_stop:
        stop_lat = float(all_stop[value]['latitude'])
        stop_long = float(all_stop[value]['longitude'])
        dict_la = math.pow(lat-stop_lat,2)
        dict_long = math.pow(long-stop_long,2)
        total_dist = math.pow(dict_la+dict_long,0.5)
        dist_dic[value] = total_dist
    near_stop = min(dist_dic, key=dist_dic.get)
    message = '最近的水時監測站為'+near_stop+'\n'
    message += '資料日期時間'+all_stop[near_stop]['update_date']+' '+all_stop[near_stop]['update_time']+'\n'
    message += '經度'+all_stop[near_stop]['longitude']+'\n'
    message += '緯度'+all_stop[near_stop]['latitude']+'\n'
    message += '濁度(NTU)'+all_stop[near_stop]['qua_cntu']+'\n'
    message += '餘氯(mg/L)'+all_stop[near_stop]['qua_cl']+'\n'
    message += '酸度(pH)'+all_stop[near_stop]['qua_ph']
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text= message))


if __name__ == "__main__":
#    timer = threading.Timer(900,get_taipei_data)
#    timer.start()
    app.run()

