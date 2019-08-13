from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
# from flask_cache import Cache
import pymysql
pymysql.install_as_MySQLdb()
#惰性加载
csrf=CSRFProtect()
models=SQLAlchemy()
# cache=Cache(config={"CACHE_TYPE":"simple"})
def create_app(config_name):
    app=Flask(__name__)#创建app实例
    app.config.from_object("settings.DebugConfig")#app的配置文件
    # app.run()#默认是开启的
    csrf.init_app(app)#惰性加载csrf
    # cache.init_app(app)
    models.init_app(app)
    from .main import main_blueprint
    app.register_blueprint(main_blueprint)#注册蓝图
    return app