from flask import Blueprint, render_template, redirect, flash, request, url_for, Markup
import datetime
from flask_login import current_user, login_required, fresh_login_required
from sqlalchemy.sql import func
from markdown import markdown as mkdn
from . import User, db, Post
from . import apis
markdown = lambda x: apis.parsedown(Markup(mkdn(x)))

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
    posts = Post.query.all()
    posts.reverse()
    return render_template("home.html",
                           user=current_user,
                           posts=posts,
                           suser=current_user,
                           num=len)


@views.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        text = markdown(request.form.get('body'))
        if not text:
            flash('Text Cannot be empty!', 'danger')
        else:
            text = str(text)
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post Created!', 'success')
            return redirect(url_for('views.home'))
    return render_template('create_post.html', user=current_user)


@views.route('/profile')
@login_required
def viewmyposts():
    return render_template('home.html',
                           user=current_user,
                           suser=current_user,
                           posts=current_user.posts,
                           num=len)


@views.route('/user')
@views.route('/user/<uid>')
def user(uid):
    suser = User.query.filter_by(id=uid).first()
    if suser != None:
        return render_template('home.html',
                               user=current_user,
                               posts=suser.posts,
                               suser=suser,
                               numpost=len(suser.posts))
    else:
        flash('that user id doesnt exist!', 'danger')
        return redirect(url_for('views.home'))


@views.route('/delete/<postid>')
@login_required
def delpost(postid):
    post = Post.query.filter_by(id=postid).first()
    if not post:
        flash('Post doesn\'t exist.', 'danger')
    elif current_user.id != post.user.id:
        flash('That isn\'t your post.', 'danger')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Deleted post!', 'success')
    return redirect(url_for('views.home'))
@views.route('/report/<postid>')
def report(postid):
    post = Post.query.filter_by(id=postid).first()
    inn = apis.report(post.text)
    if inn:
      db.session.delete(post)
      flash('Post reported!', 'info')
    return redirect(url_for('views.home'))