import pymysql

def connection():
    config = pymysql.connect (
            user = 'root',
           password = '',
           host = 'localhost',
           database =  'arx',
            )
    a = config.cursor()
    return a, config


