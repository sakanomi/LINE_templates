#LINEで必要なモジュール
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, PostbackEvent, ButtonsTemplate, PostbackTemplateAction, TemplateSendMessage, FollowEvent
    , LocationSendMessage, LocationMessage, ImagemapSendMessage, MessageTemplateAction, ConfirmTemplate, DatetimePickerAction, DatetimePickerTemplateAction
    , ImageMessage, ImageSendMessage, FlexSendMessage, BoxComponent, TextComponent, BubbleContainer, ButtonComponent,MessageAction
    , CarouselContainer, URIAction, ImageComponent, PostbackAction, CameraAction, CameraRollAction, QuickReplyButton, QuickReply
)

#画像系で扱うモジュール
from io import BytesIO

import pandas as pd

#CSVの読み取りとカテゴリごとの読み取り
df = pd.read_csv("./talk_module/image_talk.csv", index_col="KEY")

def talk(key, talk_number):
    text = df.loc[key][talk_number]
    return text

def image_post(line_bot_api, event):
    message_id = event.message.id
    message_content = line_bot_api.get_message_content(message_id)
    image = BytesIO(message_content.content)
    user_id = event.source.user_id
    reply_token = event.reply_token