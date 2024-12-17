from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from models import db, User, Product, CartItem, Order
from forms import RegisterForm, LoginForm
from recommendations import generate_recommendations

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['TESTING'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(nickname=form.nickname.data, email=form.email.data, gender=form.gender.data[0],
                    age=form.age.data, interests=",".join(form.interests.data), password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Login failed. Check your credentials.', 'danger')
    return render_template('login.html', form=form)


@app.route('/profile')
@login_required
def profile():
    recommendations = generate_recommendations({
        'age': current_user.age,
        'interests': current_user.interests
    })
    return render_template('profile.html', recommendations=recommendations)


@app.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart_item = CartItem(user_id=current_user.id, product_id=product.id, quantity=1)
    db.session.add(cart_item)
    db.session.commit()
    flash(f'{product.name} added to cart!', 'success')
    return redirect(url_for('index'))


@app.route('/checkout')
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    return render_template('cart.html', cart_items=cart_items)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
