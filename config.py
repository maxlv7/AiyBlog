import os

'''程序的配置文件'''

# 程序的绝对文件位置
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    pass



# 基类 Config 中包含通用配置，子类分别定义专用的配置。如果需要，你还可添加其他配置类。
class DevelopmentConfig(Config):

    SECRET_KEY = os.environ.get('SECRET_KEY') or "hard"
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or \
    'mysql+pymysql://root:root@127.0.0.1:3306/aiyblog'
    # 'sqlite:///' + os.path.join(basedir, "AiyBlog.db")



class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("PRO_DATA_BASE_URL") or \
          'sqlite:///' + os.path.join(basedir,"AiyBlog.db") or \
           'mysql+pymysql://root:root@127.0.0.1:3306/aiyblog'

config = {
    "development":DevelopmentConfig,
    "production":ProductionConfig
}

if __name__ == '__main__':
    print('sqlite:///' + os.path.join(basedir,"AiyBlog.db"))