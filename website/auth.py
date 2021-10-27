from flask import Blueprint, render_template, redirect, url_for, request, flash, make_response
from . import db, User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import apis
from sqlalchemy.sql import func
auth = Blueprint('auth', __name__)

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
  if request.method == 'POST':
    password = str(request.form.get("pw"))
    email = request.form.get("email")
    user = User.query.filter_by(email=email).first()
    user.gravatar = apis.genergrav(user.email)
    db.session.commit()
    if user != None:
      if check_password_hash(user.password, password):
        flash('Signed in', "success")
        respo = make_response(redirect(url_for('views.home')))
        login_user(user, remember=True)
        return respo
      else:
        flash('Incorrect Password!', 'danger')
    else:
      flash('Email doesnt exist!', 'danger')
  return render_template('signin.html', user=current_user)
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'POST':
    email = request.form.get("email")
    password = request.form.get("pw")
    password2 = request.form.get("pw2")
    username = request.form.get("username")
    email_exits = User.query.filter_by(email=email).first()
    username_exits = User.query.filter_by(username=username).first()
    if email_exits:
      flash('Email Already exists!', 'danger')
    elif username_exits:
      flash('Username already exits!', 'danger')
    elif password != password2:
      flash('Passwords don\'t match!', 'danger')
    elif len(username) < 2:
      flash('Username must be at least 3 characters', 'danger')
    elif len(password) < 7:
      flash('Password must be at least 8 characters', 'error')
    else:
      new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'), gravatar=apis.genergrav(email))
      db.session.add(new_user)
      db.session.commit()
      login_user(new_user, remember=True)
      flash('User Created!', 'success')
      return redirect(url_for('views.home'))
  return render_template('signup.html', user=current_user)
@auth.route('/signout')
@login_required
def signout():
  logout_user()
  flash('User signed out', 'success')
  return redirect(url_for('auth.signin'))
@auth.route('/admin')
@login_required
def admin():
  if current_user.id == 1:
    flash('dev mode entered!', 'success')
    return render_template('dev.html', user=current_user)
  else:
    flash('you are not a developer!', 'error')
    return redirect(url_for('views.home'))