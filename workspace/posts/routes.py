from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from workspace import db, bcrypt
from workspace.models import User, Post
from workspace.posts.forms import PostForm
from workspace.posts.utils import save_picture

posts = Blueprint('posts', __name__)

#Route to submit the post form and redirect back to create post
@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.image.data:
            image_file = save_picture(form.image.data)
            
        post = Post(title=form.title.data, description=form.description.data, size=form.size.data, location=form.location.data, country=form.country.data, image = image_file, price=form.price.data, space_type=form.space_type.data, availability=form.availability.data, facility=form.facility.data, contact=form.contact.data,  author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')

#Route to view space post by the ID
@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

#Route to edit space post by the ID
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')

#Route to delete space post by the ID
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

@posts.route('/post/search', methods=['GET'])
def search():
    selected_country = request.args.get('country')
    if selected_country:
        posts = Post.query.filter_by(country=selected_country).all()
    else:
        posts = []
    return render_template('search_results.html', posts=posts)

