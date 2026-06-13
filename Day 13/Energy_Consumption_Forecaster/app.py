# ==========================================
# IMPORTS
# ==========================================

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

import sqlite3
import pandas as pd

import joblib

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

# ==========================================
# CREATE APP
# ==========================================

app = Flask(__name__)

app.secret_key = "energy_secret_key"
# ==========================================
# LOAD MODEL
# ==========================================

model = joblib.load(
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

    def __init__(
        self,
        id,
        username=None,
        email=None
    ):

        self.id = id

        self.username = username

        self.email = email


# ==========================================
# LOAD USER
# ==========================================

@login_manager.user_loader
def load_user(user_id):

    connection = sqlite3.connect(
        "database.db"
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            username,
            email

        FROM users

        WHERE id = ?
        """,

        (
            user_id,
        )
    )

    user = cursor.fetchone()

    connection.close()

    if user:

        return User(
            user[0],
            user[1],
            user[2]
        )

    return None


# ==========================================
# HOME
# ==========================================

@app.route('/')
def home():

    return render_template(
        'index.html'
    )


# ==========================================
# REGISTER
# ==========================================

@app.route(
    '/register',
    methods=['GET', 'POST']
)
def register():

    if request.method == 'POST':

        username = request.form['username']

        email = request.form['email']

        password = request.form['password']

        confirm_password = request.form['confirm_password']

        if password != confirm_password:

            flash(
                "Passwords do not match!"
            )

            return redirect(
                url_for(
                    'register'
                )
            )

        hashed_password = generate_password_hash(
            password
        )

        connection = sqlite3.connect(
            "database.db"
        )

        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO users
                (
                    username,
                    email,
                    password
                )

                VALUES (?, ?, ?)
                """,

                (
                    username,
                    email,
                    hashed_password
                )
            )

            connection.commit()

        except sqlite3.IntegrityError:

            flash(
                "Email already registered!"
            )

            connection.close()

            return redirect(
                url_for(
                    'register'
                )
            )

        connection.close()

        flash(
            "Registration successful!"
        )

        return redirect(
            url_for(
                'login'
            )
        )

    return render_template(
        'register.html'
    )


# ==========================================
# LOGIN
# ==========================================

@app.route(
    '/login',
    methods=['GET', 'POST']
)
def login():

    if request.method == 'POST':

        email = request.form['email']

        password = request.form['password']

        connection = sqlite3.connect(
            "database.db"
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                username,
                email,
                password

            FROM users

            WHERE email = ?
            """,

            (
                email,
            )
        )

        user = cursor.fetchone()

        connection.close()

        if user and check_password_hash(
            user[3],
            password
        ):

            login_user(

                User(

                    user[0],

                    user[1],

                    user[2]

                )

            )

            return redirect(
                url_for(
                    'profile'
                )
            )

        flash(
            "Invalid email or password!"
        )

    return render_template(
        'login.html'
    )


# ==========================================
# PROFILE
# ==========================================

@app.route('/profile')
@login_required
def profile():

    return render_template(
        'profile.html'
    )

# ==========================================
# PREDICT
# ==========================================

@app.route(
    '/predict',
    methods=['GET', 'POST']
)

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

    if request.method == 'POST':

        global_reactive_power = request.form[
            'global_reactive_power'
        ]

        voltage = request.form[
            'voltage'
        ]

        global_intensity = request.form[
            'global_intensity'
        ]

        sub_metering_1 = request.form[
            'sub_metering_1'
        ]

        sub_metering_2 = request.form[
            'sub_metering_2'
        ]

        sub_metering_3 = request.form[
            'sub_metering_3'
        ]

        sample = pd.DataFrame([{

            "Global_reactive_power":

            float(global_reactive_power),

            "Voltage":

            float(voltage),

            "Global_intensity":

            float(global_intensity),

            "Sub_metering_1":

            float(sub_metering_1),

            "Sub_metering_2":

            float(sub_metering_2),

            "Sub_metering_3":

            float(sub_metering_3)

        }])

        prediction = round(

            model.predict(
                sample
            )[0],

            3

        )

        if prediction < 1:

            category = "Low Consumption"

            advice = "Power usage is low."

        elif prediction < 3:

            category = "Moderate Consumption"

            advice = (
                "Power usage is within normal range."
            )

        else:

            category = "High Consumption"

            advice = (
                "Power usage is high. Consider saving energy."
            )

        connection = sqlite3.connect(
            "database.db"
        )

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

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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

                advice

            )

        )

        connection.commit()

        connection.close()

    return render_template(

        'predict.html',

        prediction=prediction,

        category=category,

        advice=advice,

        global_reactive_power=
        global_reactive_power,

        voltage=
        voltage,

        global_intensity=
        global_intensity,

        sub_metering_1=
        sub_metering_1,

        sub_metering_2=
        sub_metering_2,

        sub_metering_3=
        sub_metering_3

    )

# ==========================================
# HISTORY
# ==========================================

@app.route('/history')

@login_required

def history():

    connection = sqlite3.connect(
        "database.db"
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT

            predicted_power,

            category,

            advice,

            created_at

        FROM predictions

        WHERE user_id = ?

        ORDER BY created_at DESC
        """,

        (
            current_user.id,
        )

    )

    records = cursor.fetchall()

    connection.close()

    return render_template(

        'history.html',

        records=records

    )

# ==========================================
# ANALYTICS
# ==========================================

@app.route('/analytics')
@login_required
def analytics():

    return render_template(
        'analytics.html'
    )


# ==========================================
# ABOUT
# ==========================================

@app.route('/about')
def about():

    return render_template(
        'about.html'
    )
# ==========================================
# LOGOUT
# ==========================================

@app.route('/logout')
@login_required
def logout():

    logout_user()

    return redirect(
        url_for(
            'home'
        )
    )


# ==========================================
# RUN APP
# ==========================================

if __name__ == '__main__':

    app.run(
        debug=True
    )