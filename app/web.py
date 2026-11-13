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
from app.services.patient_service import (
    get_all_patients , 
    create_patient , 
    get_patient_by_id,
    update_patient,
    delete_patient)
from app.services.doctor_service import (
    get_all_doctors,
    get_doctor_by_id,
    create_doctor,
    update_doctor,
    delete_doctor,
)
from app.services.doctor_schedule_service import (
    get_doctor_schedule,
    save_doctor_schedule,
    get_available_slots,
)
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

    print("PATIENT ROUTE EXECUTED")
    print("PATIENT COUNT:", len(records))
    print("CURRENT ROLE:", session.get("role"))

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

# ------------------------------------------
# View Patient Details
# ------------------------------------------

@app.route("/patients/<int:patient_id>")
@login_required
def view_patient(patient_id):

    role = session.get("role")

    if role not in ("Admin", "Doctor", "Staff"):
        abort(403)

    patient = get_patient_by_id(
        patient_id,
        role=role,
    )

    if isinstance(patient, dict):
        abort(403)

    if patient is None:
        abort(404)

    return render_template(
        "view_patient.html",
        patient=patient,
    )


# ------------------------------------------
# Edit Patient
# ------------------------------------------

@app.route(
    "/patients/<int:patient_id>/edit",
    methods=["GET", "POST"],
)
@login_required
def edit_patient(patient_id):

    role = session.get("role")

    # The service performs the final permission check.
    if role not in ("Admin", "Staff"):
        abort(403)

    patient = get_patient_by_id(
        patient_id,
        role=role,
    )

    if patient is None:
        abort(404)

    if isinstance(patient, dict):
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

        result = update_patient(
            patient_id=patient_id,
            data=data,
            role=role,
            user_id=session["user_id"],
        )

        if isinstance(result, dict):
            flash(
                result.get(
                    "message",
                    "Patient update failed.",
                ),
                "danger",
            )

        elif result is False:
            flash("Patient not found.", "warning")

        else:
            flash(
                "Patient updated successfully.",
                "success",
            )
            return redirect(
                url_for("view_patient", patient_id=patient_id)
            )

    return render_template(
        "edit_patient.html",
        patient=patient,
    )


# ------------------------------------------
# Delete Patient
# ------------------------------------------

@app.route(
    "/patients/<int:patient_id>/delete",
    methods=["POST"],
)
@login_required
def remove_patient(patient_id):

    # Restrict deletion to Admin.
    if session.get("role") != "Admin":
        abort(403)

    result = delete_patient(
        patient_id=patient_id,
        role=session["role"],
        user_id=session["user_id"],
    )

    if isinstance(result, dict):
        flash(
            result.get(
                "message",
                "Patient deletion failed.",
            ),
            "danger",
        )

    elif result is False:
        flash("Patient not found.", "warning")

    else:
        flash(
            "Patient deleted successfully.",
            "success",
        )

    return redirect(url_for("patients"))


@app.route("/doctors")
@login_required
def doctors():
    role = session.get("role")

    if role not in ("Admin", "Doctor", "Staff"):
        abort(403)

    records = get_all_doctors(role=role)

    if isinstance(records, dict):
        abort(403)

    return render_template(
        "doctors.html",
        doctors=records,
    )


@app.route("/doctors/register", methods=["GET", "POST"])
@login_required
def register_doctor():
    role = session.get("role")

    if role != "Admin":
        abort(403)

    if request.method == "POST":
        from uuid import uuid4

        data = {
            "doctor_code": f"TMP-{uuid4().hex}",
            "name": request.form.get("name", "").strip(),
            "specialization": request.form.get(
                "specialization", ""
            ).strip(),
            "department": request.form.get(
                "department", ""
            ).strip(),
            "phone": request.form.get("phone", "").strip(),
            "email": request.form.get("email", "").strip(),
        }

        result = create_doctor(
            data=data,
            role=role,
            user_id=session["user_id"],
        )

        if isinstance(result, dict):
            message = result.get(
                "message", "Doctor registration failed."
            )

            errors = result.get("errors", [])

            if errors:
                message += " " + " ".join(errors)

            flash(message, "danger")

        else:
            flash(
                f"Doctor registered successfully! ID: {result}",
                "success",
            )

            return redirect(url_for("doctors"))

    return render_template("register_doctor.html")

@app.route("/doctors/<int:doctor_id>")
@login_required
def view_doctor(doctor_id):
    role = session.get("role")

    if role not in ("Admin", "Doctor", "Staff"):
        abort(403)

    doctor = get_doctor_by_id(doctor_id, role=role)

    if isinstance(doctor, dict):
        abort(403)

    if doctor is None:
        abort(404)

    return render_template(
        "view_doctor.html",
        doctor=doctor,
    )


@app.route("/doctors/<int:doctor_id>/edit", methods=["GET", "POST"])
@login_required
def edit_doctor(doctor_id):
    role = session.get("role")

    if role != "Admin":
        abort(403)

    doctor = get_doctor_by_id(doctor_id, role=role)

    if isinstance(doctor, dict):
        abort(403)

    if doctor is None:
        abort(404)

    if request.method == "POST":
        data = {
            "doctor_code": doctor["doctor_code"],
            "name": request.form.get("name", "").strip(),
            "specialization": request.form.get(
                "specialization", ""
            ).strip(),
            "department": request.form.get(
                "department", ""
            ).strip(),
            "phone": request.form.get("phone", "").strip(),
            "email": request.form.get("email", "").strip(),
        }

        result = update_doctor(
            doctor_id=doctor_id,
            data=data,
            role=role,
            user_id=session["user_id"],
        )

        if isinstance(result, dict):
            message = result.get(
                "message", "Doctor update failed."
            )
            errors = result.get("errors", [])

            if errors:
                message += " " + " ".join(errors)

            flash(message, "danger")

        elif result is False:
            flash("Doctor not found.", "warning")

        else:
            flash("Doctor updated successfully.", "success")

            return redirect(
                url_for("view_doctor", doctor_id=doctor_id)
            )

    return render_template(
        "edit_doctor.html",
        doctor=doctor,
    )


@app.route("/doctors/<int:doctor_id>/delete", methods=["POST"])
@login_required
def remove_doctor(doctor_id):
    if session.get("role") != "Admin":
        abort(403)

    result = delete_doctor(
        doctor_id=doctor_id,
        role=session["role"],
        user_id=session["user_id"],
    )

    if isinstance(result, dict):
        flash(
            result.get("error")
            or result.get("message", "Doctor deletion failed."),
            "danger",
        )

    elif result is False:
        flash("Doctor not found.", "warning")

    else:
        flash("Doctor deleted successfully.", "success")

    return redirect(url_for("doctors"))

@app.route(
    "/doctors/<int:doctor_id>/schedule",
    methods=["GET", "POST"],
)
@login_required
def doctor_schedule(doctor_id):
    if session.get("role") != "Admin":
        abort(403)

    doctor = get_doctor_by_id(
        doctor_id,
        role=session["role"],
    )

    if doctor is None:
        abort(404)

    if isinstance(doctor, dict):
        abort(403)

    if request.method == "POST":
        result = save_doctor_schedule(
            doctor_id=doctor_id,
            day_of_week=request.form.get("day_of_week"),
            start_time=request.form.get("start_time", ""),
            end_time=request.form.get("end_time", ""),
            is_active=request.form.get("is_active") == "on",
            role=session["role"],
            user_id=session["user_id"],
        )

        flash(
            result["message"],
            "success" if result["success"] else "danger",
        )

        if result["success"]:
            return redirect(
                url_for("doctor_schedule", doctor_id=doctor_id)
            )

    schedule = get_doctor_schedule(doctor_id)

    return render_template(
        "doctor_schedule.html",
        doctor=doctor,
        schedule=schedule,
    )

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")
