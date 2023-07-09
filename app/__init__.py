from flask import Flask
from app.asset import Asset
from app.model import db
from flask_migrate import Migrate

app = Flask(__name__)

Asset(app)

app.config.from_pyfile('../config.py')

db.init_app(app)
migrate = Migrate(app, db)

from app.routes import routes
app.register_blueprint(routes)
