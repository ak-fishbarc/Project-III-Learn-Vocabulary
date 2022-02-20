from vocab import app
from vocab import db
from vocab.models import User, VocabSet
from flask import flash, render_template, request, redirect, url_for
from vocab.forms import SetForm, LoginForm, RegistrationForm
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', title='Learn Vocabulary')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', title="Sign In", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    wordsets = user.word_sets.all()
    return render_template('user.html', user=user, wordsets=wordsets)


@app.route('/create_set', methods=['GET', 'POST'])
@login_required
def create_set():
    form = SetForm()
    new_set = VocabSet(name=form.name.data, words=form.words.data, words2=form.words2.data, creator=current_user)
    db.session.add(new_set)
    db.session.commit()
    return render_template('create_set.html', form=form)


@app.route('/memory', methods=['GET', 'POST'])
@login_required
def memory():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    wordsets = user.word_sets.all()
    words = {}
    translation = {}
    for sets in wordsets:
        if sets.words is not None and sets.words2 is not None:
            words[sets.name] = sets.words.split(',')
            translation[sets.name] = sets.words2.split(',')
    return render_template('memory.html', wordsets=wordsets)


@app.route('/to_card', methods=['GET', 'POST'])
@login_required
def to_card():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    wordsets = user.word_sets.all()
    words = {}
    translation = {}
    for sets in wordsets:
        if sets.words is not None and sets.words2 is not None:
            words = sets.words.split(',')
            translation = sets.words2.split(',')
    set = {'words': words, 'translation': translation}
    return set


