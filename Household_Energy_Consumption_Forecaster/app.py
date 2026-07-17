# ==========================================
# IMPORTS
# ==========================================
import re
from flask import Flask, render_template, request, redirect, url_for, flash
import os

from dotenv import load_dotenv
from flask import session
import random
import psycopg2
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg2.connect(DATABASE_URL)
import requests

from werkzeug.utils import secure_filename
import pandas as pd
import io
import joblib
import plotly.express as px
from datetime import datetime

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from reportlab.platypus import Table

from reportlab.platypus import TableStyle

from reportlab.lib import colors

from reportlab.lib.styles import getSampleStyleSheet

from flask import send_file

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)

from werkzeug.security import generate_password_hash, check_password_hash
import csv

from flask import make_response
from authlib.integrations.flask_client import OAuth

# ==========================================
# DATABASE INITIALIZATION
# ==========================================

def init_db():

    connection = get_connection()
    cursor = connection.cursor()

    # USERS TABLE

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(

            id SERIAL PRIMARY KEY,

            username TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            profile_picture TEXT DEFAULT 'default.png',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    # PREDICTIONS TABLE

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions(

            id SERIAL PRIMARY KEY,

            user_id INTEGER,

            global_reactive_power DOUBLE PRECISION,

            voltage DOUBLE PRECISION,

            global_intensity DOUBLE PRECISION,

            sub_metering_1 DOUBLE PRECISION,

            sub_metering_2 DOUBLE PRECISION,

            sub_metering_3 DOUBLE PRECISION,

            predicted_power DOUBLE PRECISION,

            category TEXT,

            advice TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
            REFERENCES users(id)

        )
    """)

    connection.commit()

    cursor.close()

    connection.close()

    print("PostgreSQL Database initialized successfully!")
# ==========================================
# CREATE APP
# ==========================================

app = Flask(__name__)
oauth = OAuth(app)

google = oauth.register(

    name="google",

    client_id=os.getenv(
        "GOOGLE_CLIENT_ID"
    ),

    client_secret=os.getenv(
        "GOOGLE_CLIENT_SECRET"
    ),

    server_metadata_url=
    "https://accounts.google.com/.well-known/openid-configuration",

    client_kwargs={

        "scope": "openid email profile"

    }

)
init_db()
app.config["UPLOAD_FOLDER"] = "static/uploads"

app.secret_key = os.getenv("SECRET_KEY")


def send_otp_email(receiver_email, username, otp):

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {

        "accept": "application/json",

        "api-key": os.getenv(
            "BREVO_API_KEY"
        ),

        "content-type": "application/json"

    }

    payload = {

        "sender": {

            "name": "Energy Forecaster",

            "email": "harshabhogaraju@gmail.com"

        },

        "to": [

            {

                "email": receiver_email,

                "name": username

            }

        ],

        "subject": "Email Verification OTP",

        "htmlContent": f"""

        <h2>Hello {username},</h2>

        <p>Your OTP for registration is:</p>

        <h1>{otp}</h1>

        <p>Please enter this OTP to complete your registration.</p>

        """

    }

    try:

        response = requests.post(

            url,

            json=payload,

            headers=headers

        )

        print(response.status_code)

        print(response.text)

        return response.status_code == 201

    except Exception as e:

        print(

            "Brevo Error:",

            e

        )

        return False
# ==========================================
# LOAD MODEL
# ==========================================

def load_model():
    return joblib.load(
        "models/final_model.pkl"
    )

# ==========================================
# LOGIN MANAGER
# ==========================================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"

# ==========================================
# USER CLASS
# ==========================================


class User(UserMixin):

    def __init__(self, id, username=None, email=None):

        self.id = id

        self.username = username

        self.email = email


# ==========================================
# LOAD USER
# ==========================================


@login_manager.user_loader
def load_user(user_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            username,
            email,
            profile_picture
        FROM users
        WHERE id = %s
        """,
        (user_id,),
    )

    user = cursor.fetchone()

    cursor.close()

    connection.close()

    if user:

        u = User(user[0], user[1], user[2])

        u.profile_picture = user[3]

        return u

    return None
# ==========================================
# HOME
# ==========================================


@app.route("/")
def home():

    return render_template("index.html")

# ==========================================
# REGISTER
# ==========================================
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]

        email = request.form["email"]

        password = request.form["password"]

        confirm_password = request.form["confirm_password"]

        if len(password) < 8:
            flash("Password must contain at least 8 characters.")
            return redirect(url_for("register"))

        if not re.search(r"[A-Z]", password):
            flash("Password must contain at least one uppercase letter.")
            return redirect(url_for("register"))

        if not re.search(r"[a-z]", password):
            flash("Password must contain at least one lowercase letter.")
            return redirect(url_for("register"))

        if not re.search(r"\d", password):
            flash("Password must contain at least one number.")
            return redirect(url_for("register"))

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            flash("Password must contain at least one special character.")
            return redirect(url_for("register"))

        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for("register"))

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE email = %s
            """,
            (email,),
        )

        existing_user = cursor.fetchone()

        if existing_user:

            cursor.close()

            connection.close()

            flash("Email already registered!")

            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                email,
                password
            )
            VALUES (%s, %s, %s)
            """,
            (
                username,
                email,
                hashed_password,
            ),
        )

        connection.commit()

        cursor.close()

        connection.close()

        flash("Registration successful!")

        return redirect(url_for("login"))

    return render_template("register.html")
# ==========================================
# GOOGLE LOGIN
# ==========================================
@app.route("/google_login")
def google_login():

    redirect_uri = url_for(

        "google_callback",

        _external=True

    )

    return google.authorize_redirect(

        redirect_uri

    )
# ==========================================
# GOOGLE CALLBACK
# ==========================================
@app.route("/google/callback")
def google_callback():

    token = google.authorize_access_token()

    user_info = token["userinfo"]

    username = user_info["name"]

    email = user_info["email"]

    profile_picture = user_info["picture"]

    connection = get_connection()

    cursor = connection.cursor()

    # Check if user already exists
    cursor.execute(
        """
        SELECT
            id,
            username,
            email,
            profile_picture
        FROM users
        WHERE email = %s
        """,
        (email,),
    )

    user = cursor.fetchone()

    if user is None:

        # Insert new Google user
        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                email,
                password,
                profile_picture
            )
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (
                username,
                email,
                "",
                profile_picture,
            ),
        )

        user_id = cursor.fetchone()[0]

        connection.commit()

    else:

        user_id = user[0]

    cursor.close()

    connection.close()

    user = User(
        user_id,
        username,
        email,
    )

    user.profile_picture = profile_picture

    login_user(user)

    flash("Logged in successfully!")

    return redirect(url_for("home"))

# ==========================================
# LOGIN
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                username,
                email,
                password
            FROM users
            WHERE email = %s
            """,
            (email,),
        )

        user = cursor.fetchone()

        cursor.close()

        connection.close()

        if user and check_password_hash(user[3], password):

            user_obj = User(
                user[0],
                user[1],
                user[2],
            )

            login_user(user_obj)

            flash("Login successful!")

            return redirect(url_for("home"))

        else:

            flash("Invalid email or password!")

            return redirect(url_for("login"))

    return render_template("login.html")
# ==========================================
# PROFILE
# ==========================================


@app.route("/profile")
@login_required
def profile():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT

            predicted_power

        FROM predictions

        WHERE user_id = %s
        """,
        (current_user.id,),
    )

    records = cursor.fetchall()

    cursor.close()

    connection.close()

    powers = [record[0] for record in records]

    total_predictions = len(powers)

    if total_predictions > 0:

        average_consumption = round(sum(powers) / total_predictions, 3)

        highest_consumption = round(max(powers), 3)

    else:

        average_consumption = 0

        highest_consumption = 0

    return render_template(
        "profile.html",
        total_predictions=total_predictions,
        average_consumption=average_consumption,
        highest_consumption=highest_consumption,
    )

# ==========================================
# CHANGE PASSWORD
# ==========================================


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():

    if request.method == "POST":

        current_password = request.form["current_password"]

        new_password = request.form["new_password"]

        confirm_password = request.form["confirm_password"]

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT

                password

            FROM users

            WHERE id = %s
            """,
            (current_user.id,),
        )

        user = cursor.fetchone()

        if not check_password_hash(user[0], current_password):

            flash("Current password is incorrect!")

            cursor.close()

            connection.close()

            return redirect(url_for("change_password"))

        if new_password != confirm_password:

            flash("Passwords do not match!")

            cursor.close()

            connection.close()

            return redirect(url_for("change_password"))

        hashed_password = generate_password_hash(new_password)

        cursor.execute(
            """
            UPDATE users

            SET password = %s

            WHERE id = %s
            """,
            (
                hashed_password,
                current_user.id,
            ),
        )

        connection.commit()

        cursor.close()

        connection.close()

        flash("Password changed successfully!")

        return redirect(url_for("profile"))

    return render_template("change_password.html")

# ==========================================
# UPLOAD PROFILE PICTURE
# ==========================================


@app.route("/upload_profile_picture", methods=["POST"])
@login_required
def upload_profile_picture():

    if "profile_picture" not in request.files:

        return redirect(url_for("profile"))

    file = request.files["profile_picture"]

    if file.filename == "":

        return redirect(url_for("profile"))

    filename = secure_filename(file.filename)

    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE users

        SET profile_picture = %s

        WHERE id = %s
        """,
        (
            filename,
            current_user.id,
        ),
    )

    connection.commit()

    cursor.close()

    connection.close()

    flash("Profile picture updated successfully!")

    return redirect(url_for("profile"))

# ==========================================
# PREDICT
# ==========================================
@app.route("/predict", methods=["GET", "POST"])
@login_required
def predict():

    prediction = None
    category = None
    advice = None

    global_reactive_power = ""
    voltage = ""
    global_intensity = ""
    sub_metering_1 = ""
    sub_metering_2 = ""
    sub_metering_3 = ""

    if request.method == "POST":

        global_reactive_power = request.form["global_reactive_power"]
        voltage = request.form["voltage"]
        global_intensity = request.form["global_intensity"]
        sub_metering_1 = request.form["sub_metering_1"]
        sub_metering_2 = request.form["sub_metering_2"]
        sub_metering_3 = request.form["sub_metering_3"]

        sample = pd.DataFrame(
            [{
                "Global_reactive_power": float(global_reactive_power),
                "Voltage": float(voltage),
                "Global_intensity": float(global_intensity),
                "Sub_metering_1": float(sub_metering_1),
                "Sub_metering_2": float(sub_metering_2),
                "Sub_metering_3": float(sub_metering_3),
            }]
        )

        model = load_model()

        prediction = round(model.predict(sample)[0], 3)

        if prediction < 1:

            category = "Low Consumption"
            advice = "Power usage is low."

        elif prediction < 3:

            category = "Moderate Consumption"
            advice = "Power usage is within normal range."

        else:

            category = "High Consumption"
            advice = "Power usage is high. Consider saving energy."

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO predictions
            (
                user_id,
                global_reactive_power,
                voltage,
                global_intensity,
                sub_metering_1,
                sub_metering_2,
                sub_metering_3,
                predicted_power,
                category,
                advice
            )

            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                current_user.id,
                float(global_reactive_power),
                float(voltage),
                float(global_intensity),
                float(sub_metering_1),
                float(sub_metering_2),
                float(sub_metering_3),
                prediction,
                category,
                advice,
            ),
        )

        connection.commit()

        cursor.close()

        connection.close()

    return render_template(
        "predict.html",
        prediction=prediction,
        category=category,
        advice=advice,
        global_reactive_power=global_reactive_power,
        voltage=voltage,
        global_intensity=global_intensity,
        sub_metering_1=sub_metering_1,
        sub_metering_2=sub_metering_2,
        sub_metering_3=sub_metering_3,
    )


# ==========================================
# DOWNLOAD PDF REPORT
# ==========================================

@app.route("/download_report")
@login_required
def download_report():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT

            predicted_power,

            category,

            advice,

            created_at

        FROM predictions

        WHERE user_id = %s

        ORDER BY id DESC

        LIMIT 1
        """,
        (current_user.id,),
    )

    record = cursor.fetchone()

    cursor.close()

    connection.close()

    if record is None:

        return redirect(url_for("predict"))

    pdf = SimpleDocTemplate("energy_report.pdf")

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "Household Energy Consumption Report",
        styles["Title"]
    )

    elements.append(title)

    elements.append(Spacer(1, 20))

    data = [
        ["Predicted Power", f"{record[0]} kW"],
        ["Category", record[1]],
        ["Advice", record[2]],
        ["Date", str(record[3])],
    ]

    table = Table(data)

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                ("BOX", (0, 0), (-1, -1), 1, colors.black),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )

    elements.append(table)

    pdf.build(elements)

    return send_file(
        "energy_report.pdf",
        as_attachment=True,
    )

# ==========================================
# EXPORT HISTORY TO CSV
# ==========================================


@app.route("/export_csv")
@login_required
def export_csv():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT

            predicted_power,

            category,

            advice,

            created_at

        FROM predictions

        WHERE user_id = %s

        ORDER BY created_at DESC
        """,
        (current_user.id,),
    )

    records = cursor.fetchall()

    cursor.close()

    connection.close()

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow(
        [
            "Predicted Power",
            "Category",
            "Advice",
            "Date",
        ]
    )

    writer.writerows(records)

    response = make_response(output.getvalue())

    response.headers["Content-Disposition"] = (
        "attachment; filename=prediction_history.csv"
    )

    response.headers["Content-Type"] = "text/csv"

    return response


# ==========================================
# HISTORY
# ==========================================


@app.route("/history")
@login_required
def history():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT

            id,

            predicted_power,

            category,

            advice,

            created_at

        FROM predictions

        WHERE user_id = %s

        ORDER BY created_at DESC
        """,
        (current_user.id,),
    )

    records = cursor.fetchall()

    cursor.close()

    connection.close()

    return render_template(
        "history.html",
        records=records,
    )


# ==========================================
# DELETE HISTORY RECORD
# ==========================================

@app.route("/delete_prediction/<int:id>")
@login_required
def delete_prediction(id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM predictions

        WHERE id = %s

        AND user_id = %s
        """,
        (
            id,
            current_user.id,
        ),
    )

    connection.commit()

    cursor.close()

    connection.close()

    return redirect(url_for("history"))


# ==========================================
# ANALYTICS
# ==========================================

@app.route("/analytics")
@login_required
def analytics():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT

            predicted_power,

            category,

            created_at

        FROM predictions

        WHERE user_id = %s
        """,
        (current_user.id,),
    )

    records = cursor.fetchall()

    cursor.close()

    connection.close()

    if len(records) == 0:

        return render_template("analytics.html")

    powers = [record[0] for record in records]

    categories = [record[1] for record in records]

    dates = [record[2] for record in records]

    total_predictions = len(powers)

    average_consumption = round(sum(powers) / total_predictions, 3)

    highest_consumption = round(max(powers), 3)

    lowest_consumption = round(min(powers), 3)

    high_percentage = round(
        categories.count("High Consumption") * 100 / total_predictions,
        2,
    )

    # ==========================================
    # PIE CHART
    # ==========================================

    category_counts = {
        "Low Consumption": categories.count("Low Consumption"),
        "Moderate Consumption": categories.count("Moderate Consumption"),
        "High Consumption": categories.count("High Consumption"),
    }

    pie_chart = px.pie(
        names=list(category_counts.keys()),
        values=list(category_counts.values()),
        title="Consumption Category Distribution",
    )

    pie_chart.update_traces(
        textposition="inside",
        textinfo="percent+label",
    )

    pie_chart_html = pie_chart.to_html(full_html=False)

    # ==========================================
    # TOP 10 HIGHEST CONSUMPTION RECORDS
    # ==========================================

    top_10_powers = sorted(
        powers,
        reverse=True,
    )[:10]

    labels = [
        f"Record {i+1}"
        for i in range(len(top_10_powers))
    ]

    bar_chart = px.bar(
        x=top_10_powers,
        y=labels,
        orientation="h",
        title="Top 10 Highest Consumption Records",
    )

    bar_chart.update_layout(
        yaxis_title="Records",
        xaxis_title="Predicted Power (kW)",
    )

    bar_chart_html = bar_chart.to_html(full_html=False)

    # ==========================================
    # WEEKLY AVERAGE CONSUMPTION TREND
    # ==========================================

    df = pd.DataFrame(
        {
            "Power": powers,
            "Date": pd.to_datetime(dates),
        }
    )

    df["Day"] = df["Date"].dt.day_name()

    weekly_avg = (
        df.groupby("Day")["Power"]
        .mean()
        .reset_index()
    )

    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    weekly_avg["Day"] = pd.Categorical(
        weekly_avg["Day"],
        categories=day_order,
        ordered=True,
    )

    weekly_avg = weekly_avg.sort_values("Day")

    line_chart = px.line(
        weekly_avg,
        x="Day",
        y="Power",
        markers=True,
        title="Weekly Average Consumption Trend",
    )

    line_chart.update_layout(
        xaxis_title="Day",
        yaxis_title="Average Consumption (kW)",
    )

    line_chart_html = line_chart.to_html(full_html=False)

    return render_template(
        "analytics.html",
        total_predictions=total_predictions,
        average_consumption=average_consumption,
        highest_consumption=highest_consumption,
        lowest_consumption=lowest_consumption,
        high_percentage=high_percentage,
        pie_chart=pie_chart_html,
        bar_chart=bar_chart_html,
        line_chart=line_chart_html,
    )

# ==========================================
# ABOUT
# ==========================================


@app.route("/about")
def about():

    return render_template("about.html")


# ==========================================
# LOGOUT
# ==========================================


@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("home"))


# ==========================================
# RUN APP
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)
