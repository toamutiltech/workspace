from flask import render_template, request, Blueprint
from workspace.models import Post

main = Blueprint('main', __name__)
"""
This is the first page loaded by the browser,
It load with the space post available in the database 
it and redirect to home page when Home is click
"""
@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
	#Route to redirect to about page when about is click or enter into the browser address
    return render_template('about.html', title='About')


@main.route("/contact")
def contact():
	#Route to redirect to Contact page when contact is click or enter into the browser address
    return render_template('contact.html', title='Contact')
