#LINEで必要なモジュール
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, PostbackEvent, ButtonsTemplate, PostbackTemplateAction, TemplateSendMessage, FollowEvent
    , LocationSendMessage, LocationMessage, ImagemapSendMessage, MessageTemplateAction, ConfirmTemplate, DatetimePickerAction, DatetimePickerTemplateAction
    , ImageMessage, ImageSendMessage, FlexSendMessage, BoxComponent, TextComponent, BubbleContainer, ButtonComponent,MessageAction
    , CarouselContainer, URIAction, ImageComponent, PostbackAction, CameraAction, CameraRollAction, QuickReplyButton, QuickReply
)

import pandas as pd

#CSVの読み取りとカテゴリごとの読み取り
df = pd.read_csv("./talk_module/postback_talk.csv", index_col="KEY")

def talk(key, talk_number):
    text = df.loc[key][talk_number]
    return text

def postback_post(event):
    user_id = event.source.user_id
    reply_token = event.reply_token
    postback_msg = event.postback.data
    params = event.postback.params