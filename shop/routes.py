import os
from flask import render_template, url_for, request, redirect, flash, session
from shop import app, db
from shop.models import Author, Book, User
from shop.forms import RegistrationForm, LoginForm, CheckoutForm
from flask_login import login_user, current_user, logout_user, login_required
#import flask_whooshalchemy as wa

@app.route("/")
@app.route("/home")

def home():
    books = Book.query.all()
    return render_template('home.html', books=books, title="the bookstore")

@app.route("/home2")
def sortA():
    books = Book.query.order_by('price')
    return render_template('home.html', books=books, title="the bookstore")

@app.route("/home3")
def sortTitle():
    books = Book.query.order_by('title')
    return render_template('home.html', books=books, title="the bookstore")


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/book/<int:book_id>")
def book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book.html', title=book.title, book=book)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created. You can log in.")
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

    
@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash("You are now logged in")
            return redirect(url_for('home'))
        flash('Invalid username or password.')
    return render_template('login.html', title='Login Page', form=form)

@app.route("/logout")
def logout():
    logout_user()
    session.clear()
    flash("You have logged out")
    return redirect(url_for('home'))


@app.route("/add_to_cart/<int:book_id>")
def add_to_cart(book_id):
    if "cart" not in session:
        session['cart']=[]
        
    session['cart'].append(book_id)
    
    flash('Added to shopping cart')
    return redirect("/cart")




@app.route("/wishlist", methods=["GET","POST"])
def wishlist_display():
    if "wishlist" not in session:
        flash("Your wishlist is empty")
        return render_template("wishlist.html", display_wishlist={}, total=0)
    else:
        items = session["wishlist"]
        wishlist = {}

        total_price = 0
        total_quantity = 0
        for item in items:
            book = Book.query.get_or_404(item)
            total_price += book.price
            if book.id in wishlist:
                wishlist[book.id]["quantity"] += 1
            else:
                wishlist[book.id] = {"quantity":1, "title":book.title, "price":book.price}
            total_quantity = sum(item['quantity'] for item in wishlist.values())
        return render_template("wishlist.html", title='Your Wishlist', display_wishlist = wishlist, total = total_price, total_quantity = total_quantity)
    return render_template('wishlist.html')


@app.route("/cart", methods=["GET","POST"])
def cart_display():
    if "cart" not in session:
        flash("Your shopping cart is empty")
        return render_template("cart.html", display_cart={}, total=0)
    else:
        items = session["cart"]
        cart = {}

        total_price = 0
        total_quantity = 0
        for item in items:
            book = Book.query.get_or_404(item)
            total_price += book.price
            if book.id in cart:
                cart[book.id]["quantity"] += 1
            else:
                cart[book.id] = {"quantity":1, "title":book.title, "price":book.price}
            total_quantity = sum(item['quantity'] for item in cart.values())
        return render_template("cart.html", title='Your Shopping Cart', display_cart = cart, total = total_price, total_quantity = total_quantity)
    return render_template('cart.html')

@app.route("/add_to_wishlist/<int:book_id>")
def add_to_wishlist(book_id):
    if "wishlist" not in session:
        session['wishlist']=[]
        
    session['wishlist'].append(book_id)
    
    flash('Added to wishlist')
    return redirect("/wishlist")


@app.route("/delete_book/<int:book_id>", methods=['POST'])
def delete_book(book_id):
    if "cart" not in session:
        session["cart"] = []
    session["cart"].remove(book_id)
                                 
    flash("The book has been removed from your shopping cart!")
    session.modified = True
                                 
    return redirect("/cart")

@app.route("/delete_wishlist/<int:book_id>", methods=['POST'])
def delete_wishlist(book_id):
    if "wishlist" not in session:
        session["wishlist"] = []
    session["wishlist"].remove(book_id)
                                 
    flash("The book has been removed from your wishlist!")
    session.modified = True
                                 
    return redirect("/wishlist")



@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()
    if form.validate_on_submit():
        flash("The payment is successful. Thank you for shopping with us.")
        return redirect(url_for('home'))
    #flash("error")
    return render_template('checkout.html', title='Checkout', form=form)

                                 
@app.route("/thankyou")
def thankyou():
    return render_template('thankyou.html', title='Thank you for being awesome')

'''
@app.route('/search')
def search():
    book = Book.query.whoosh_search(request.args.get('query')).all()
    return render_template('home.html', books=books, title="the bookstore")


  '''     

