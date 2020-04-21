from flask import Flask, session, redirect, render_template 
from flask import request, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
from werkzeug.exceptions import Unauthorized


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def show_register_form():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        registerd = User.register(username, password)
        user = User(username=username, password=registerd.password, email=email, first_name=first_name, last_name=last_name)
        db.session.add(user)
        db.session.commit()
        session["username"] = user.username

        return redirect(url_for('show_secret', username=user.username))
    else:     
        return render_template('register_user.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def show_login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username  # keep logged in
            return redirect(url_for('show_secret', username=user.username))
        else:
             form.username.errors = ["Bad name/password"]

    return render_template('login.html', form=form)

@app.route('/users/<username>')
def show_secret(username):
    if 'username' not in session:
        flash('You must be logged in to view')
        return redirect(url_for('home'))
    else: 
        username = session['username']
        user = User.query.get_or_404(username)
        return render_template('user_detail.html', user=user)

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('home')) 

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    if 'username' not in session:
        flash('You must be logged in to view')
        return redirect(url_for('home'))
    else: 
        username = session['username']
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('home'))          


# Feed Back forms
@app.route('/feedback/<username>/add', methods=['GET', 'POST'])
def add_feedback(username):
    if 'username' not in session:
        flash('You must be logged in to view')
        return redirect(url_for('home'))
    else:     
        username = session['username']
        form = FeedbackForm()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            new_feedback = Feedback(title=title, content=content, username=username)
            db.session.add(new_feedback)
            db.session.commit()

            return redirect(url_for('show_secret', username=username))
        else:  
            return render_template('feedback_form.html', form=form, username=username)

@app.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])  
def edit_feedback(feedback_id):
    if 'username' not in session:
        flash('You must be logged in to view')
        return redirect(url_for('home'))
    else:     
        fb = Feedback.query.get_or_404(feedback_id)
        form = FeedbackForm(obj=fb)
        if form.validate_on_submit():
            fb.title = form.title.data
            fb.content = form.content.data
            db.session.commit()
            return redirect(url_for('show_secret', username=fb.username))
        else:     
            return render_template('edit_feedback.html', form=form) 

@app.route('/feedback/<feedback_id>/delete', methods=['POST'])  
def delete_feedback(feedback_id):
    if 'username' not in session:
        flash('You must be logged in to view')
        return redirect(url_for('home'))
    else:
        fb = Feedback.query.get_or_404(feedback_id)
        db.session.delete(fb)
        db.session.commit()
        return redirect(url_for('show_secret', username=fb.username))
      