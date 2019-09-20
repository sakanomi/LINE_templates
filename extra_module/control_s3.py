import boto3
from botocore.config import Config

import configparser
from io import BytesIO, StringIO
from PIL import Image

import pandas as pd

#設定ファイルの読み込み
cfg = configparser.ConfigParser()
cfg.read('config.ini')

#S3の設定
region = cfg["S3"]["REGION"]
accesskey = cfg["S3"]["ACCESS"]
secretkey = cfg["S3"]["SECRET"]
bucket_name = cfg["S3"]["BUCKET"]

def to_img_s3(keypath, img):#keyはS3の保存するファイルパス
    s3 = boto3.client('s3', aws_access_key_id=accesskey, aws_secret_access_key=secretkey, region_name=region)
    img.thumbnail((900, 1200), Image.ANTIALIAS)
    out = BytesIO()
    img.save(out, "PNG")

    ls =  s3.list_objects(Bucket=bucket_name, Prefix="line_picture", Delimiter='/')

    s3.put_object(Bucket=bucket_name, Key=keypath, Body=out.getvalue())
    url = "https://"+bucket_name+".s3-"+region+".amazonaws.com/"+keypath
    return url

def read_csv_s3(keypath):
    s3 = boto3.client('s3', aws_access_key_id=accesskey, aws_secret_access_key=secretkey, region_name=region)
    obj = s3.get_object(Bucket=bucket_name, Key=keypath)
    csv = pd.read_csv(obj['Body'], index_col=0)
    return csv

def put_to_csv(db, user_id):#申請者のCSVの保存とURLのリターン
    keypath = "data_csv/personal_csv/"+user_id+".csv"
    df = pd.read_sql(sql=cfg["SQL"]["SELECT_WHERE"] + user_id + "';", con=db.engine)
    out2 = StringIO()
    df.to_csv(out2, encoding='utf_8_sig')
    s3 = boto3.client('s3', aws_access_key_id=accesskey, aws_secret_access_key=secretkey, region_name=region)
    s3.put_object(Bucket=bucket_name, Key=keypath, Body=out2.getvalue().encode("utf-8_sig"))
    url = "https://"+bucket_name+".s3-"+region+".amazonaws.com/"+keypath
    return url

def to_csv_s3(keypath, dataframe):
    # データベースからデータをとる
    out2 = StringIO()
    dataframe.to_csv(out2, encoding='utf_8_sig')
    s3 = boto3.client('s3', aws_access_key_id=accesskey, aws_secret_access_key=secretkey, region_name=region)
    s3.put_object(Bucket=bucket_name, Key=keypath, Body=out2.getvalue().encode("utf-8_sig"))

