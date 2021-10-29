from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from os import path, environ, getcwd
from flask_login import LoginManager, UserMixin
import datetime
from . import apis, security
import time
from sqlalchemy.sql import func
from sqlalchemy.orm import column_property
from dotenv import load_dotenv
load_dotenv()
db = SQLAlchemy()
class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.Text, nullable=False)
  likes = db.relationship("PostLike", backref="post", passive_deletes=True)
  date_created = db.Column(db.DateTime(timezone=True), default=apis.now())
  author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
  comments = db.relationship("Comment", backref="post", passive_deletes=True)
class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(150), unique=True)
  username = db.Column(db.String(150), unique=True)
  password = db.Column(db.String(150), unique=False)
  dev = db.Column(db.Boolean)
  date_created = db.Column(db.DateTime(timezone=True), default=apis.now())
  posts = db.relationship('Post', backref='user', passive_deletes=True)
  gravatar = db.Column(db.String(150), unique=True)
  likes = db.relationship("PostLike", backref="user", passive_deletes=True)
  comments = db.relationship('Comment', backref="user", passive_deletes=True)
class Comment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.String(150))
  author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
  cpost = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
class PostLike(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
  lpost = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"))
DB_NAME = 'database.db'
def create_app():
  app = Flask(__name__)
  environ['SECRET_KEY'] = security.newkey()
  app.config['SECRET_KEY'] = environ['SECRET_KEY']
  app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['REMEMBER_COOKIE_DURATION'] = datetime.timedelta(weeks=5)
  db.init_app(app)
  create_database(app)
  from .views import views
  from .auth import auth
  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')
  import os
  login_manager = LoginManager()
  login_manager.login_view = "auth.signin"
  login_manager.login_message = "You need to be logged in!"
  login_manager.login_message_category = 'danger'
  login_manager.init_app(app)
  @login_manager.user_loader
  def load_user(id):
    return User.query.get(int(id))
  @app.route("/css/<filen>")
  def css(filen):
      return send_from_directory(os.path.join(app.root_path, 'static/css'), filen, mimetype='text/css')
  @app.route('/favicon.ico')
  def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
  return app
def create_database(app):
  db.create_all(app=app)
