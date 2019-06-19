import secrets
import os
from PIL import Image
from flask import url_for, redirect, flash, render_template, request, abort
from antisocial_media.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from antisocial_media.models import Post, User
from antisocial_media import app, db, bcrypt
from flask_login import login_user, current_user, login_required, logout_user


@app.route("/")

@app.route("/layout")
def layout():
    users = User.query.all()
    return render_template('layout.html',users=users)

@app.route("/home")
def home():
    posts = Post.query.all()[::-1]
    users = User.query.all()
    return render_template('home.html',posts=posts,users=users)

@app.route("/register",methods=['GET','POST'])
def register():
    users = User.query.all()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    #Check Form Values for Accuracy and Create Account if All Checks out.
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        #Integrity Check to Make Sure User Name is Not Already in Use.
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form,users=users)

@app.route("/login",methods=['GET','POST'])
def login():
    users = User.query.all()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            #Redirect to Requested page if not yet logged in when requested
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Failed. Please check Username and Password','danger')
    return render_template('login.html',title='Login',form=form,users=users)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    #Use Pillow Functions to resize Images
    output_size=(125, 125)
    new_img = Image.open(form_picture)
    new_img.thumbnail(output_size)
    new_img.save(picture_path)

    return picture_fn

@app.route("/account",methods=['GET','POST'])
@login_required
def account():
    users = User.query.all()
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account Update Successful!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    hr_violations = current_user.hr_violations
    return render_template('account.html',title='Account',image_file=image_file,form=form,users=users)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    users = User.query.all()
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post',users=users)


@app.route("/post/<int:post_id>/delete", methods=['GET','POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
       abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/post/<int:post_id>/add", methods=['GET','POST'])
@login_required
def add_violation(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author == current_user:
        abort(403)
    post.author.hr_violations += 1
    db.session.commit()
    flash('Point has been added! ', 'success')
    return redirect(url_for('home'))
