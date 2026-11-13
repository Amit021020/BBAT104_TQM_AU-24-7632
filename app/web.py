
import os
from functools import wraps

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    abort,
)

from flask_wtf.csrf import CSRFProtect

from app.database.db import initialize_database, get_connection
from app.services.user_service import authenticate_user
from app.services.patient_service import get_all_patients , create_patient


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["FLASK_SECRET_KEY"]
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

csrf = CSRFProtect(app)

initialize_database()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))

        return view(*args, **kwargs)

    return wrapped


@app.before_request
def load_current_user():
    if "user_id" not in session:
        return

    conn = get_connection()

    try:
        user = conn.execute(
            """
            SELECT id, username, role, is_active
            FROM users
            WHERE id = ?
            """,
            (session["user_id"],),
        ).fetchone()

        if user is None or not user["is_active"]:
            session.clear()
            return

        session["username"] = user["username"]
        session["role"] = user["role"]

    finally:
        conn.close()


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        user = authenticate_user(username, password)

        if user is None:
            flash("Invalid username or password.", "error")
        else:
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))



@app.route("/")
@login_required
def dashboard():
    conn = get_connection()

    try:
        stats = {}

        tables = {
            "patients": "patients",
            "doctors": "doctors",
            "appointments": "appointments",
            "medical_records": "medical_records",
            "bills": "bills",
        }

        for key, table in tables.items():
            stats[key] = conn.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]

        recent_patients = conn.execute(
            """
            SELECT id, patient_code, name, age, gender, created_at
            FROM patients
            ORDER BY id DESC
            LIMIT 5
            """
        ).fetchall()

    finally:
        conn.close()

    return render_template(
        "dashboard.html",
        stats=stats,
        recent_patients=recent_patients,
    )


@app.route("/patients")
@login_required
def patients():
    if session.get("role") not in ("Admin", "Doctor", "Staff"):
        abort(403)

    records = get_all_patients(role=session["role"])

    if isinstance(records, dict):
        abort(403)

    return render_template("patients.html", patients=records)



@app.route("/patients/register", methods=["GET", "POST"])
@login_required
def register_patient():

    # Check permission before displaying or processing the form.
    if session.get("role") not in ("Admin", "Staff"):
        abort(403)

    if request.method == "POST":

        data = {
            "name": request.form.get("name", "").strip(),
            "age": request.form.get("age", "").strip(),
            "gender": request.form.get("gender", "").strip(),
            "blood_group": request.form.get("blood_group", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "address": request.form.get("address", "").strip(),
            "emergency_contact": request.form.get(
                "emergency_contact", ""
            ).strip(),
        }

        result = create_patient(
            data=data,
            role=session["role"],
            user_id=session["user_id"],
        )

        # The service returns an integer on success
        # and an error dictionary on failure.
        if isinstance(result, dict):
            message = result.get(
                "message", "Patient registration failed."
            )

            errors = result.get("errors", [])
            if errors:
                message += " " + " ".join(errors)

            flash(message, "danger")

        else:
            flash(
                f"Patient registered successfully! ID: {result}",
                "success",
            )

            return redirect(url_for("patients"))

    return render_template("register_patient.html")

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")
