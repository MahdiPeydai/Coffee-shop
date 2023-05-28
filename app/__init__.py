from flask import Flask
from app.asset import Asset
import pymysql.cursors

# first time
pymysql.install_as_MySQLdb()


app = Flask(__name__)
Asset(app)
app.config.from_pyfile('../config.py')


db = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB'],
    cursorclass=pymysql.cursors.DictCursor
)
curs = db.cursor()

from .routs.home import home
app.register_blueprint(home)

from .routs.shop import shop
app.register_blueprint(shop)
