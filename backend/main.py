from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    jsonify,
    session,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import date, datetime
import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt

import uuid

from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_cors import CORS

from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

from datetime import timedelta
from flask_bcrypt import Bcrypt

from flask_caching import Cache
from time import perf_counter_ns


app = Flask(__name__)


app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users_10.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt()
app.app_context().push()

CORS(app, resources={r"/*": {"origins": "*"}})


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True)


class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    m_name = db.Column(db.String(100), unique=True, nullable=False)
    m_password_hash = db.Column(db.String(100), nullable=False)

    @staticmethod
    def initialize_manager():
        manager = Manager.query.filter_by(m_name="manager").first()
        if not manager:
            new_manager = Manager(m_name="manager")
            new_manager.set_password("manager@123")
            db.session.add(new_manager)
            db.session.commit()

    def set_password(self, password):
        self.m_password_hash = bcrypt.generate_password_hash(password).decode("utf-8")


class Section(db.Model):
    section_id = db.Column(db.Integer, primary_key=True)
    section_name = db.Column(db.String(100), unique=True, nullable=False)
    section_description = db.Column(db.String(1000), nullable=False)
    products = db.relationship(
        "Product", backref="section", lazy=True, cascade="all, delete-orphan"
    )


class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    product_manufacture_date = db.Column(db.Date)
    product_expiry_date = db.Column(db.Date)
    product_rate_per_unit = db.Column(db.Float, nullable=False)
    product_unit = db.Column(db.String(20))  # For example, 'Rs/Kg', 'Rs/Litre'
    product_stock = db.Column(db.Integer, nullable=False)
    section_id = db.Column(
        db.Integer, db.ForeignKey("section.section_id"), nullable=False
    )

    def __repr__(self):
        return f"Product('{self.product_name}', Manufactured: {self.product_manufacture_date}, Expires: {self.product_expiry_date}, Rate: {self.product_rate_per_unit} {self.product_unit})"


class UserCart(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    product_rate_per_unit = db.Column(db.Float, nullable=False)
    product_qty = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    last_modified = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def serialize(self):
        return {
            "item_id": self.item_id,
            "username": self.username,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "product_rate_per_unit": self.product_rate_per_unit,
            "product_qty": self.product_qty,
            "amount": self.amount,
            "last_modified": self.last_modified.isoformat(),
        }


class UserTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ut_date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    product_rate_per_unit = db.Column(db.Float, nullable=False)
    product_qty = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)


class StoreManagerRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class StoreManager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(100), nullable=False)


from celery_worker import make_celery

app.config.update(
    CELERY_BROKER_URL="redis://localhost:6379",
    CELERY_RESULT_BACKEND="redis://localhost:6379",
)
celery = make_celery(app)

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import *
import base64
from jinja2 import Template
from celery.schedules import crontab


SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "no-projectcart@gmail.com"
SENDER_PASSWORD = ""


def send_email(to_address, subject, message, content="text", attachment_file=None):
    mail = MIMEMultipart()
    mail["From"] = SENDER_ADDRESS
    mail["To"] = to_address
    mail["Subject"] = subject

    if content == "html":
        mail.attach(MIMEText(message, "html"))
    else:
        mail.attach(MIMEText(message, "plain"))

    if attachment_file:
        with open(attachment_file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encode_base64(part)

        part.add_header(
            "Content-Disposition", f"attachment; filename={attachment_file}"
        )
        mail.attach(part)

    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(mail)
    s.quit()

    return True


def make_cache():
    cache_mapping = {
        "CACHE_TYPE": "RedisCache",
        "CACHE_REDIS_HOST": "localhost",
        "CACHE_REDIS_PORT": 6379,
    }

    app.config.from_mapping(cache_mapping)

    cache = Cache(app)
    app.app_context().push()

    return cache


current_cache = make_cache()


@celery.on_after_configure.connect
def setup_intervalTASK(sender, **kwargs):  # schedule jobs
    sender.add_periodic_task(
        crontab(minute=30, hour=19),
        send_inactive_users_emails.s(),
        name="send_reminder",
    )
    sender.add_periodic_task(
        crontab(minute=30, hour=19),
        send_monthly_report.s(),
        name="Monthly Report",
    )
    sender.add_periodic_task(
        crontab(minute=30, hour=19),
        cleanup_abandoned_carts.s(),
        name="Monthly Report",
    )


@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = bcrypt.generate_password_hash(data.get("password")).decode("utf-8")

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 400

    new_user = User(username=username, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@app.route("/login_manager", methods=["POST"])
def manager_login():
    data = request.get_json()
    m_name = data.get("m_name")
    m_password = data.get("m_password")
    manager = Manager.query.filter_by(m_name=m_name).first()
    if manager and bcrypt.check_password_hash(manager.m_password_hash, m_password):
        access_token = create_access_token(identity=m_name)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@app.route("/add_section", methods=["GET", "POST"])
def create_section():
    if request.method == "POST":
        data = request.get_json()
        s_name = data.get("s_name")
        s_description = data.get("s_description")

        sec = Section(section_name=s_name, section_description=s_description)

        db.session.add(sec)
        db.session.commit()

        return jsonify({"message": "Section created successfully"}), 201
    return jsonify({"message": "Method not allowed"}), 405


@current_cache.memoize(timeout=50)
@app.route("/view_section", methods=["GET"])
def get_sections():
    start = perf_counter_ns()
    all_sections = Section.query.all()
    stop = perf_counter_ns()
    print("time taken", stop - start)
    sections = [
        {
            "id": section.section_id,
            "name": section.section_name,
            "description": section.section_description,
        }
        for section in all_sections
    ]
    return jsonify(sections)


@app.route("/view_section/<int:section_id>/delete", methods=["DELETE"])
def delete_section(section_id):
    section = Section.query.get(section_id)
    if section:
        db.session.delete(section)
        db.session.commit()
        return jsonify({"message": "Section deleted successfully"})
    else:
        return jsonify({"message": "Section not found"}, 404)


@app.route("/view_section/<int:section_id>/update", methods=["POST"])
def update_section(section_id):
    section = Section.query.get(section_id)
    if section:
        if request.is_json:
            data = request.get_json()
            section.section_name = data.get("section_name", section.section_name)
            section.section_description = data.get(
                "section_description", section.section_description
            )
            db.session.commit()
            return jsonify({"message": "Section updated successfully"})
        else:
            return jsonify({"message": "Invalid request data format"}, 400)
    else:
        return jsonify({"message": "Section not found"}, 404)


@app.route("/section_name", methods=["GET"])
def section_name():
    if request.method == "GET":
        all_sections = Section.query.all()
        sections = [
            {"id": section.section_id, "name": section.section_name}
            for section in all_sections
        ]
        return jsonify(sections)


@app.route("/add_product", methods=["POST"])
def create_product():
    if request.method == "POST":
        data = request.get_json()
        p_name = data.get("p_name")
        p_manufact = datetime.strptime(data.get("p_manufact"), "%Y-%m-%d")
        p_expiry = datetime.strptime(data.get("p_expiry"), "%Y-%m-%d")
        p_perunit = data.get("p_perunit")
        p_unit = data.get("p_unit")
        p_stock = data.get("p_stock")
        p_section = data.get("p_section")
        section = Section.query.filter_by(section_name=p_section).first()
        if section:
            prod = Product(
                product_name=p_name,
                product_manufacture_date=p_manufact,
                product_expiry_date=p_expiry,
                product_rate_per_unit=p_perunit,
                product_unit=p_unit,
                product_stock=p_stock,
                section_id=section.section_id,
            )

            db.session.add(prod)
            db.session.commit()

            return jsonify({"message": "Product created successfully"})

        else:
            return jsonify(
                {"error": "Section not found. Please enter a valid section name."}
            )


@app.route("/view_product", methods=["GET"])
def get_products():
    all_products = Product.query.all()
    products = [
        {
            "id": product.product_id,
            "name": product.product_name,
            "manufacture": str(product.product_manufacture_date),
            "expiry": str(product.product_expiry_date),
            "per_unit": product.product_rate_per_unit,
            "unit": product.product_unit,
            "stock": product.product_stock,
            "section": product.section_id,
        }
        for product in all_products
    ]
    return jsonify(products)


@app.route("/view_product/<int:product_id>/delete", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Section deleted successfully"})
    else:
        return jsonify({"message": "Section not found"}, 404)


@app.route("/view_product/<int:product_id>/update", methods=["POST"])
def update_product(product_id):
    product = Product.query.get(product_id)
    if product:
        if request.is_json:
            data = request.get_json()
            product.product_name = data.get("product_name", product.product_name)
            manufacture_date_str = data.get("product_manufacture_date")
            expiry_date_str = data.get("product_expiry_date")
            try:
                manufacture_date = datetime.strptime(
                    manufacture_date_str, "%Y-%m-%d"
                ).date()
                expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"message": "Invalid date format"}, 400)

            product.product_rate_per_unit = data.get(
                "product_rate_per_unit", product.product_rate_per_unit
            )
            product.product_unit = data.get("product_unit", product.product_unit)
            product.product_manufacture_date = manufacture_date
            product.product_expiry_date = expiry_date
            product.product_stock = data.get("product_stock", product.product_stock)
            db.session.commit()
            return jsonify({"message": "Product updated successfully"})
        else:
            return jsonify({"message": "Invalid request data format"}, 400)
    else:
        return jsonify({"message": "Product not found"}, 404)


@app.route("/user_after_login_section")
@jwt_required()
def user_dashboard():
    current_user_username = get_jwt_identity()
    username = User.query.filter_by(username=current_user_username).first()

    if not username:
        return jsonify({"error": "User not found"}), 404

    sections = Section.query.all()

    sections_data = [
        {
            "section_id": section.section_id,
            "section_name": section.section_name,
        }
        for section in sections
    ]

    response_data = {"username": username.username, "sections": sections_data}

    return jsonify(response_data)


@app.route("/section/<int:section_id>/products", methods=["GET"])
def api_user_products_list(section_id):
    s1 = Section.query.get(section_id)
    items = s1.products

    product_data = [
        {
            "product_id": item.product_id,
            "product_name": item.product_name,
            "product_manufacture_date": str(item.product_manufacture_date),
            "product_expiry_date": str(item.product_expiry_date),
            "product_rate_per_unit": item.product_rate_per_unit,
            "product_unit": item.product_unit,
            "product_stock": item.product_stock,
        }
        for item in items
    ]

    return jsonify({"section": s1.section_id, "items": product_data})


@app.route("/products/<int:product_id>/add_to_cart", methods=["POST"])
@app.route("/user/cart", methods=["POST"])
@jwt_required()
def api_user_cart(product_id):
    current_user_username = get_jwt_identity()

    user = User.query.filter_by(username=current_user_username).first()
    if user is not None:
        uname = user.username
    else:
        return jsonify({"error": "User not found"}), 404

    if request.method == "POST":
        if product_id is not None:
            data = request.get_json()
            product_qty = data.get("product_qty")
            product = Product.query.get(product_id)
            if product_qty > product.product_stock:
                return (
                    jsonify(
                        {
                            "message": f"Requested quantity exceeds available stock. Max stock: {product.product_stock}"
                        }
                    ),
                    400,
                )
            amt = product.product_rate_per_unit * int(product_qty)
            i1 = UserCart(
                username=uname,
                product_id=product_id,
                product_name=product.product_name,
                product_rate_per_unit=product.product_rate_per_unit,
                product_qty=product_qty,
                amount=amt,
            )

            db.session.add(i1)
            db.session.commit()

            return jsonify({"success": True})


@app.route("/user/cart", methods=["GET"])
@jwt_required()
def get_user_cart_details():
    current_user_username = get_jwt_identity()
    user = User.query.filter_by(username=current_user_username).first()
    if user is not None:
        uname = user.username
    else:
        return jsonify({"error": "User not found"}), 404

    user_cart = UserCart.query.filter_by(username=uname).all()
    userCart = [
        {
            "product_id": item.product_id,
            "product_name": item.product_name,
            "product_rate_per_unit": item.product_rate_per_unit,
            "product_qty": item.product_qty,
            "amount": item.amount,
            "item_id": item.item_id,
            "username": item.username,
        }
        for item in user_cart
    ]

    return jsonify({"uname": uname, "userCart": userCart})


@app.route("/update/<string:uname>/<int:item_id>", methods=["GET", "POST"])
@jwt_required()
def cart_update(uname, item_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    uname = user.username
    i1 = UserCart.query.get(item_id)

    if not i1:
        return jsonify({"message": "Item not found"}), 404

    if current_user != uname:
        return jsonify({"message": "Unauthorized"}), 403

    if request.method == "GET":
        return jsonify({"item": i1.serialize(), "username": uname})

    if request.method == "POST":
        data = request.get_json()

        if "product_qty" not in data:
            return jsonify({"message": "Invalid JSON data"}), 400

        p_qty = int(data["product_qty"])
        product = Product.query.get(i1.product_id)
        if p_qty > product.product_stock:
            return (
                jsonify(
                    {
                        "message": f"Requested quantity exceeds available stock. Max stock: {product.product_stock}"
                    }
                ),
                400,
            )
        i1.product_qty = p_qty
        # i1.amount = i1.product_qty * i1.product_rate_per_unit
        i1.amount = p_qty * i1.product_rate_per_unit
        db.session.commit()

        user_cart = [
            item.serialize() for item in UserCart.query.filter_by(username=uname).all()
        ]

        return jsonify({"message": "Cart updated successfully", "user_cart": user_cart})


@app.route(
    "/products/<int:product_id>/<string:username>/delete_from_cart", methods=["DELETE"]
)
@jwt_required()
def delete_from_cart(product_id, username):
    current_user = get_jwt_identity()
    user_cart_item = UserCart.query.filter_by(
        username=current_user, product_id=product_id
    ).first()

    if not user_cart_item or current_user != username:
        return jsonify({"message": "Unauthorized"}), 403

    db.session.delete(user_cart_item)
    db.session.commit()

    user_cart = [
        item.serialize()
        for item in UserCart.query.filter_by(username=current_user).all()
    ]

    return jsonify(
        {
            "message": "Item deleted from cart",
            "user_cart": user_cart,
            "username": current_user,
        }
    )


@app.route("/checkout/<string:username>", methods=["GET", "POST"])
@jwt_required()
def api_checkout(username):
    current_user = get_jwt_identity()
    if current_user != username:
        return jsonify({"message": "Access denied"}), 403

    tdate = datetime.utcnow().date()
    totalAmount = 0
    i1s = UserCart.query.filter_by(username=current_user).all()
    cart_items = []
    for i1 in i1s:
        product = Product.query.get(i1.product_id)

        if i1.product_qty <= product.product_stock:
            utransaction = UserTransaction(
                ut_date=tdate,
                username=username,
                product_id=i1.product_id,
                product_name=i1.product_name,
                product_rate_per_unit=i1.product_rate_per_unit,
                product_qty=i1.product_qty,
                amount=i1.amount,
            )

            db.session.add(utransaction)
            product.product_stock -= i1.product_qty
            totalAmount += i1.amount

            cart_items.append(
                {
                    "id": i1.product_id,
                    "product_name": i1.product_name,
                    "product_qty": i1.product_qty,
                    "amount": i1.amount,
                }
            )

        else:
            return (
                jsonify(
                    {
                        "message": f"Not enough {i1.product_name} in stock to complete the transaction."
                    }
                ),
                400,
            )

    if request.method == "GET":
        return jsonify({"cartItems": cart_items, "totalAmount": totalAmount})

    if request.method == "POST":
        UserCart.query.filter_by(username=current_user).delete()
        db.session.commit()
        return jsonify(
            {
                "message": "Checkout successful! Your order has been placed.",
            }
        )


@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt_identity()
    return jsonify(logout="OK"), 200


@app.route("/logout_admin", methods=["POST"])
@jwt_required()
def logout_admin():
    jti = get_jwt_identity()
    return jsonify(logout="OK"), 200


@app.route("/logout_manager", methods=["POST"])
@jwt_required()
def logout_manager():
    jti = get_jwt_identity()
    return jsonify(logout="OK"), 200


@app.route("/store-manager-request", methods=["POST"])
def store_manager_request_signup():
    data = request.get_json()
    password = bcrypt.generate_password_hash(data.get("password")).decode("utf-8")
    new_request = StoreManagerRequest(
        name=data["name"],
        email=data["email"],
        password=bcrypt.generate_password_hash(data["password"]).decode("utf-8"),
    )
    db.session.add(new_request)
    db.session.commit()
    return jsonify({"message": "Request submitted successfully"})


@app.route("/admin-approve", methods=["POST"])
def admin_approve():
    data = request.get_json()
    request_to_approve = StoreManagerRequest.query.get(data["id"])
    new_store_manager = StoreManager(
        name=request_to_approve.name,
        email=request_to_approve.email,
        password=request_to_approve.password,
    )
    db.session.add(new_store_manager)
    db.session.delete(request_to_approve)
    db.session.commit()
    return jsonify({"message": "Request approved"})


@app.route("/admin-deny", methods=["POST"])
def admin_deny():
    data = request.get_json()
    request_to_deny = StoreManagerRequest.query.get(data["id"])
    db.session.delete(request_to_deny)
    db.session.commit()
    return jsonify({"message": "Request denied"})


@app.route("/store-manager-request", methods=["GET"])
def get_store_manager_requests():
    store_manager_requests = StoreManagerRequest.query.all()
    requests_data = [
        {"id": request.id, "name": request.name, "email": request.email}
        for request in store_manager_requests
    ]
    return jsonify(requests_data)


@app.route("/store_manager_login", methods=["POST"])
def login_manager():
    data = request.json
    name = data.get("name")
    password = data.get("password")

    user = StoreManager.query.filter_by(name=name).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=name)

        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@celery.task()
def send_inactive_users_emails():
    cutoff_time = datetime.utcnow() - timedelta(days=1)
    inactive_users = (
        db.session.query(User)
        .outerjoin(UserTransaction, User.username == UserTransaction.username)
        .filter(
            (UserTransaction.ut_date < cutoff_time)
            | (UserTransaction.ut_date.is_(None))
        )
        .all()
    )
    with open(r"templates/reminder_mail.html") as file:
        template_content = Template(file.read())

    for user in inactive_users:
        message = template_content.render(user=user)
        subject = "[REMINDER] Shopping please"
        send_email(
            to_address=user.email, subject=subject, message=message, content="html"
        )

    return {"message": "send_reminder_completed"}


@celery.task()
def send_monthly_report():
    """original code starts according to the documentation"""
    current_month = datetime.utcnow().replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )
    if current_month.month == 1:
        last_month = current_month.replace(year=current_month.year - 1, month=12)
    else:
        last_month = current_month - timedelta(days=current_month.day)

    """original code ends"""

    """this code is for demonstartion for project video, it takes month from 17 November to 17 December"""

    # target_month = 12
    # current_month = datetime.utcnow().replace(
    #     day=17, month=target_month, hour=0, minute=0, second=0, microsecond=0
    # )

    # # Calculate last month based on the target month
    # last_month = current_month.replace(
    #     month=target_month - 1,
    #     year=current_month.year - 1 if target_month == 1 else current_month.year,
    # )

    users = User.query.all()

    for user in users:
        orders = UserTransaction.query.filter(
            UserTransaction.username == user.username,
            UserTransaction.ut_date >= last_month,
            UserTransaction.ut_date <= current_month,
        ).all()

        total_expenditure = sum(order.amount for order in orders)
        total_products_purchased = (
            db.session.query(func.sum(UserTransaction.product_qty))
            .filter(
                UserTransaction.username == user.username,
                UserTransaction.ut_date >= last_month,
                UserTransaction.ut_date <= current_month,
            )
            .scalar()
        )

        with open(r"templates/monthly_mail.html") as file:
            template_content = Template(file.read())
            message = template_content.render(
                user=user,
                total_expenditure=total_expenditure,
                total_products_purchased=total_products_purchased,
            )
            subject = "Your monthly reviews"
            send_email(
                to_address=user.email, subject=subject, message=message, content="html"
            )

    return {"message": "monthly_report_sent"}


import csv
from io import StringIO


@app.route("/download_csv", methods=["GET"])
def download_csv():
    products_data = Product.query.all()
    csv_data = StringIO()
    csv_writer = csv.writer(csv_data)
    csv_writer.writerow(
        [
            "Product Name",
            "Manufacture Date",
            "Expiry Date",
            "Rate per Unit",
            "Unit",
            "Stock",
        ]
    )
    # for product in products_data:
    #     csv_writer.writerow([product.product_name, product.product_manufacture_date, product.product_expiry_date,
    #                          product.product_rate_per_unit, product.product_unit, product.product_stock])
    csv_writer.writerows(
        [
            [
                product.product_name,
                product.product_manufacture_date,
                product.product_expiry_date,
                product.product_rate_per_unit,
                product.product_unit,
                product.product_stock,
            ]
            for product in products_data
        ]
    )
    csv_content = csv_data.getvalue()

    return csv_content


@app.route("/cleanup_abandoned_carts", methods=["POST"])
def cleanup_abandoned_carts():
    abandoned_duration = timedelta(hours=1)
    threshold_timestamp = datetime.utcnow() - abandoned_duration

    abandoned_carts = UserCart.query.filter(
        UserCart.last_modified < threshold_timestamp
    ).all()

    for cart in abandoned_carts:
        db.session.delete(cart)

    db.session.commit()

    return jsonify({"success": True})


if __name__ == "__main__":
    db.create_all()
    with app.app_context():
        Manager.initialize_manager()
    app.run(debug=True)
