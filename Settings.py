import configparser

cfg = configparser.ConfigParser()
cfg['DEFAULT'] = {
    'debug': True
}
cfg['S3'] = {
    "REGION": ""
    , 'ACCESS': ""
    , 'SECRET': ""
    , "BUCKET": ""
}

cfg['LINE'] = {
    'SECRET': ""
    , 'TOKEN': ""
}

cfg["SQL"] = {
    "URL": ""
}
cfg["EMAIL"] = {
    "FROM": ""
    , "PASS": ""
    , "TO1": ""
    , "TO2": ""
}
cfg["SAMPLE"] = {
    "URL1": ""
    , "URL2": ""
    , "URL3": ""
    , "URL4": ""
}
with open('config.ini', 'w') as config_file:
    cfg.write(config_file)