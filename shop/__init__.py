from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#import flask_whooshalchemy as wa

app = Flask(__name__)
app.config['SECRET_KEY']='b1579ff0423933e5e14bf29b7ad2b17a43a879601c559200'

app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://c1886394:Mustafa-123@csmysql.cs.cf.ac.uk:3306/c1886394'

#app.config['WHOOSH_BASE'] = 'whoosh'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from shop import routes
