# coding:utf-8
from flask import Flask, request, abort
import configparser
from flask_sqlalchemy import SQLAlchemy
from linebot import (LineBotApi, WebhookHandler)

#LINEで必要なモジュール
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, PostbackEvent, ButtonsTemplate, PostbackTemplateAction, TemplateSendMessage, FollowEvent
    , LocationSendMessage, LocationMessage, ImagemapSendMessage, MessageTemplateAction, ConfirmTemplate, DatetimePickerAction, DatetimePickerTemplateAction
    , ImageMessage, ImageSendMessage, FlexSendMessage, BoxComponent, TextComponent, BubbleContainer, ButtonComponent,MessageAction
    , CarouselContainer, URIAction, ImageComponent, PostbackAction, CameraAction, CameraRollAction, QuickReplyButton, QuickReply
)
from linebot.exceptions import (
    InvalidSignatureError
)

#LINEcontentからモジュールをインポート
from line_content.Follow_content import follow_post
from line_content.Image_content import image_post
from line_content.Message_content import message_post
from line_content.Postback_content import postback_post


app = Flask(__name__)

#設定ファイルの読み込み
cfg = configparser.ConfigParser()
cfg.read("config.ini")

#データベースの設定
url = cfg["SQL"]["URL"]
app.config["SQLALCHEMY_DATABASE_URL"] = url
db = SQLAlchemy(app)

#LINEの設定
chansec = cfg["LINE"]["SECRET"]
acctoken = cfg["LINE"]["TOKEN"]
line_bot_api = LineBotApi(acctoken)
handler = WebhookHandler(chansec)

#オウム返しを有効にするかどうか１が有効
ORM_tester = 1


"""--------------------------------          データベースの定義           ----------------------------"""
class lineuser(db.Model):#一般ユーザー用データベース
    __tablename__ = "lineuser"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    user_id = db.Column(db.String(80), primary_key=True)
    step = db.Column(db.Integer)
    retention = db.Column(db.String(255))
    requested_at = db.Column(db.DateTime)

    def __init__(self, user_id, step, retention, requested_at):
        self.user_id = user_id
        self.step = step
        self.retention = retention
        self.requested_at = requested_at

    def __repr__(self):
        return '<lineuser %r>' % self.user_id

class administrator(db.Model):#管理者用データベース
    __tablename__ = "administrator"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    admin_id = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(255))
    adminstatus = db.Column(db.String(255))
    to_user = db.Column(db.String(255))
    page_options = db.Column(db.Integer)

    def __init__(self, admin_id, password, adminstatus, to_user, page_options):
        self.admin_id = admin_id
        self.password = password
        self.adminstatus = adminstatus
        self.to_user = to_user
        self.page_options = page_options

    def __repr__(self):
        return '<administrator %r>' % self.admin_id

class user_message(db.Model):
    __tablename__ = "user_message"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    user_id = db.Column(db.String(80))
    to_user_id = db.Column(db.String(80))
    message = db.Column(db.String(255))
    response = db.Column(db.String(255))
    message_status = db.Column(db.String(255))
    requested_at = db.Column(db.DateTime)

    def __init__(self, user_id, to_user_id, message, response, message_status, requested_at):
        self.user_id = user_id
        self.to_user_id = to_user_id
        self.message = message
        self.response = response
        self.message_status = message_status
        self.requested_at = requested_at

    def __repr__(self):
        return '<user_message %r>' % self.user_id
"""----------------------------------------------------------------------------------------------------"""


"""--------------------------------          MessagingAPIの処理           ----------------------------"""
#LINEからのPOSTを受け取る箇所
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(FollowEvent)
def on_follow(event):
    result_follow = follow_post(line_bot_api, event)

@handler.add(MessageEvent, message=TextMessage)
def on_message(event):
    if ORM_tester == 1:
        txt = event.message.text
        user_id = event.source.user_id
        reply_token = event.reply_token
        line_bot_api.reply_message(reply_token, TextSendMessage(text=txt))
    else:
        result_message = message_post(line_bot_api, event)

@handler.add(PostbackEvent)
def on_postback(event):
    result_postback = postback_post(line_bot_api, event)

@handler.add(MessageEvent, message=ImageMessage)
def Image_message(event):
    result_image = image_post(line_bot_api, event)

"""----------------------------------------------------------------------------------------------------"""



"""---------------------------         データベースの照合・処理等          ----------------------------"""
def database_send(table, user_id, value, option1=None, option2=None, option3=None):
    if db.session.query(table).filter(table.user_id == user_id).count():
        user = db.session.query(table).filter_by(user_id=user_id).first()

        #ここにDB処理を入れる（例：user.status = "none"）

        db.session.add(user)
        db.session.commit()
    else:
        line_bot_api.push_message(to=user_id, messages=TextSendMessage(text="指定されたテーブル名・もしくはテーブル名に指定のユーザーがいませんでした。"))
"""----------------------------------------------------------------------------------------------------"""



"""---------------------------       　　　  エクストラ処理     　　　     ----------------------------"""
def extra_manage(select, key, value):
    pass
"""----------------------------------------------------------------------------------------------------"""


if __name__ == "__main__":
    app.run(port=80)

