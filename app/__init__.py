from flask import Flask
from app.asset import Asset
from app.model import db, Permission
from flask_migrate import Migrate

# # first time
# pymysql.install_as_MySQLdb()

app = Flask(__name__)
Asset(app)
app.config.from_pyfile('../config.py')

db.init_app(app)
migrate = Migrate(app, db)


# db = pymysql.connect(
#     host=app.config['MYSQL_HOST'],
#     user=app.config['MYSQL_USER'],
#     password=app.config['MYSQL_PASSWORD'],
#     database=app.config['MYSQL_DB'],
#     cursorclass=pymysql.cursors.DictCursor
# )
# curs = db.cursor()

from app.routes import routes
app.register_blueprint(routes)
