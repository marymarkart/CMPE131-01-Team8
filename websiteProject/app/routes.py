from unicodedata import name
from flask_login import current_user
from .models import LoginForm, ProfileForm
from app import myapp_obj, db

from flask import render_template, request, flash, redirect, session, url_for
from flask_wtf import FlaskForm

from flask import current_app as app, render_template, request, redirect, flash, url_for

from .models import User, Post
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_manager, login_required, logout_user, login_user


#should have all our routes, login, logout, create account, etc in this file
@myapp_obj.route('/')
def splashPage():
    return render_template("home.html")

@myapp_obj.route('/sign-up', methods=['GET', 'POST'])
def createAccount():
    if request.method == 'POST':
        email = request.form.get('email') #set variables equal to the form response for 'email', same for name and password1
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2') 
        #flash("account created", category = "success")
        user = User.query.filter_by(email=email).first()
        if user: #if user already exists with this email, need to use another email
            flash("User with this email already exists!", category = "error")
        elif password1 != password2:
            flash("Passwords must match", category = "error")
        else:
            user = User(email = email, name = name, password1 = generate_password_hash(password1, method = 'sha256')) 
            #creates new user with email, name, password, maybe add date_time from class to see when created
            db.session.add(user) #add this created user to our database using this command, then commit 
            db.session.commit()
            #data = request.form //uncommenting out these two lines will print the form data from user input in terminal
            #print(data)
            flash('Account created!', category='success')#message on screen should notify us that account has been created, if not, this is not correct
            #after creating account, we should make sure we login user as well
            return redirect(url_for('splashPage'))
    return render_template("sign_up.html")

@myapp_obj.route('/delete-account', methods=['GET', 'POST'])
@login_required
def deleteAccount():
    if request.method == 'POST':#once users press the submit button, with the correct email and password, we can delete the account
        email = request.form.get('email')
        #not sure if name will be needed, duplicate emails are not allowed, so good way to check
        #using this email, we should find the user associated and delete from database
        user = User.query.filter_by(email=email).first()
        print(current_user)
        print(user)
        if current_user == user:
            db.session.delete(user)
            db.session.commit()
            flash('Account deleted!', category = 'success')
            return redirect(url_for('splashPage'))
        else: #if we have login required, the only thing that could be wrong is incorrect email,
            #if we didnt have login_required, its possible that user is not logged in and tries to delete account,
            #without it, this error message below would flash no matter what, as current_user doesnt have value
            flash("Incorrect email", category = 'error')
    return render_template("delete_account.html")
#for add to cart functionality, we need two different things
#1. all items should have an add to cart button in their html page, which is added under listing.html
#2. Once this button is pressed under the listing, it should be added to the cart. 
@myapp_obj.route('/addToCart', methods=['GET', 'POST'])
def addToCart():
    #id = request.form.get('id')
    #name = request.form.get('desc')
    #service = Post.query.filter_by(id=id).first()
    #if id and name and request.method=="POST":
        #itemArray = {}
    return render_template("cart.html")

@myapp_obj.route('/cart')
def viewCart():
    #if 'ShoppingCart' not in session:
        #return redirect(request.referrer) #redirect to most recent webpage
    return render_template("cart.html")


@myapp_obj.route('/profile')
#@login_required
def profile():
    form = ProfileForm()
    return render_template("/profile.html", form=form)

@myapp_obj.route('/login', methods=['GET','POST'])
def login():
    # checks if user is already logged in, redirects to homepage
    #if current_user.is_authenticated:
    #    return redirect(url_for('/'))
    form = LoginForm()
    # checks if user puts in correct info
    if form.validate_on_submit():
        print("World")
        user = User.query.filter_by(name=form.name.data).first()
        print(user)
        # if user puts wrong info, show error message
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('login'))
        login_user(user)
        flash('You are logged in')
        return redirect(url_for('splashPage'))
    return render_template("/login.html", title = 'Sign in', form=form)


"""
@myapp_obj.route('/login', methods=['GET', 'POST'])
def login():
    current_form = LoginForm()
    if form.validate_on_submit ():
        flash('Login requested for user{}, remember_me={}' .format(form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template("login.html", title='Login in', form=current_form)
"""

#the page to add a new listing
@myapp_obj.route('/new-listing', methods=["GET", "POST"])
#@login_required
def new_listing():
    if request.method == "POST":
        desc = request.form.get("desc")
        body = request.form.get("body")
        post = Post(desc=desc, body=body)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for(".display", post_id=post.id))
    return render_template("new_listing.html")

#directs the user to a listing
@myapp_obj.get('/listing/<int:post_id>')
def display(post_id):
    post = Post.query.filter_by(id=post_id).one()
    #if request.method == "POST": #if we get a post request in these methods, it will be for add to cart, and we want to commit the item to the cart database
        #return redirect(url_for("addToCart")) #temp filler
    return render_template("listing.html", post=post)

@myapp_obj.route('/logout')
#@login_required
def logout():
    logout_user()
    flash('You have logged yourself out')
    return redirect(url_for('splashPage'))



@myapp_obj.route('/discover')
def discover():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    
    return render_template("discover.html", posts=posts)


@myapp_obj.route('/history')
@login_required
def history():
    return render_template("history.html")

