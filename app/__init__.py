from flask import Flask, render_template
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
