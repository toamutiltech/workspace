from flask import render_template, url_for, flash, redirect
from workspace import app
from workspace.forms import RegistrationForm, LoginForm
from workspace.models import User, Post



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/location")
def location():
    return render_template('location.html', title='Location')

@app.route("/space")
def space():
    return render_template('space.html', title='Space')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/contact")
def contact():
    return render_template('contact.html', title='Contact')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
