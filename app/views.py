import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt

from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, ItemsForm, BidForm, PurchaseItemForm
from app.models import User, Item, Bids

from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')


# USER CREDENTIALS
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/admin", methods=['GET', 'POST'])
def admin_page():
    form = ItemsForm()
    if form.validate_on_submit():
        item = Item(name=form.name.data, category=form.category.data, description=form.description.data,price=form.price.data, image_file=form.image_file.data)
        db.session.add(item)
        db.session.commit()

        return redirect(url_for('cars'))
    return render_template('admin.html', form=form)


# FUNCTIONALITY
@app.route('/home/NFTs')
def nft():
    title = 'NFTs'

    NFTs = Item.query.filter_by(category='NFTs').all()

    return render_template('NFTs.html', title=title, NFTs=NFTs)


@app.route('/home/jewellery')
def jewellery():
    title = 'Jewellery'

    jewellery = Item.query.filter_by(category='Jewellery').all()

    return render_template('jewellery.html', title=title, jewellery=jewellery)


@app.route('/home/cars')
def cars():
    purchase_item = PurchaseItemForm()
    title = 'Vintage cars'

    cars = Item.query.filter_by(category='Classic Cars').all()

    return render_template('cars.html', title=title, cars=cars, purchase_item=purchase_item)


@app.route('/home/artworks')
def artworks():
    title = 'Artworks'

    artworks = Item.query.filter_by(category='Artworks').all()

    return render_template('artworks.html', title=title, artworks=artworks)


@app.route('/home/electronics')
def electronics():
    title = 'Electronics'

    electronics = Item.query.filter_by(category='Electronics').all()

    return render_template('electronics.html', title=title, electronics=electronics)


@app.route('/home/furniture')
def furniture():
    title = 'Furniture'

    furniture = Item.query.filter_by(category='Furniture').all()

    return render_template('furniture.html', title=title, furniture=furniture)


@app.route("/bid/<int:id>", methods=['GET', 'POST'])
@login_required
def bid(id):
    form = BidForm()
    itemBid = Bids.query.filter_by(id=id)
    print(itemBid)
    if form.validate_on_submit():
        bid = Bids(item=form.name.data, price=form.price.data, owner=current_user.username)
        db.session.add(bid)
        db.session.commit()
        flash('Your bid has been recorded', 'success')
        return redirect(url_for('bid', id=id))
    return render_template('bid-now.html', form=form, itemBid=itemBid)

