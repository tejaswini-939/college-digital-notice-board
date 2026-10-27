"""A small Flask application for a college digital notice board."""

import os
import re

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Flask signs session cookies with this value. Keep it in an environment
# variable instead of committing a secret to the project.
session_secret = os.environ.get("SESSION_SECRET")
if not session_secret:
    raise RuntimeError(
        "SESSION_SECRET is required. Set it before starting the application."
    )

app.config.update(
    SECRET_KEY=session_secret,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("SESSION_COOKIE_SECURE", "false").lower()
    == "true",
)

# This dictionary is for a classroom demonstration only. Accounts disappear
# whenever the application restarts and are not shared between processes.
USERS = {}

# Sample notices are kept in a Python list so no database is needed.
NOTICES = [
    {
        "title": "End-Semester Examination Schedule",
        "description": "The end-semester examinations begin on 18 November. Check the department notice board for your room and subject-wise timetable.",
        "category": "Examinations",
        "date": "2026-11-18",
    },
    {
        "title": "Practical Exam Registration",
        "description": "Register for laboratory practical examinations through your department office by 10 November. Bring your student ID card.",
        "category": "Examinations",
        "date": "2026-11-04",
    },
    {
        "title": "Campus Placement Drive: Northstar Technologies",
        "description": "Final-year students from Computer Science and Electronics can apply. Submit your updated resume to the placement cell.",
        "category": "Placements",
        "date": "2026-11-02",
    },
    {
        "title": "Resume and Interview Workshop",
        "description": "The placement cell is hosting a resume review and mock interview workshop. Sign up at the student career office.",
        "category": "Placements",
        "date": "2026-10-30",
    },
    {
        "title": "Annual Cultural Festival",
        "description": "Join us for music, dance, theatre, and student art at the annual college cultural festival in the main auditorium.",
        "category": "Events",
        "date": "2026-11-12",
    },
    {
        "title": "Inter-Department Sports Meet",
        "description": "Teams can register for football, badminton, athletics, and chess with the sports office. All students are welcome.",
        "category": "Events",
        "date": "2026-11-08",
    },
    {
        "title": "Library Hours During Study Week",
        "description": "The central library will remain open until 10:00 PM during study week. Please carry your student ID for entry.",
        "category": "General",
        "date": "2026-11-09",
    },
    {
        "title": "Update Your Student Contact Details",
        "description": "Please confirm your phone number and email address with the student office so the college can contact you when needed.",
        "category": "General",
        "date": "2026-10-28",
    },
]


def get_current_student():
    """Return the signed-in student's details, or clear a stale session."""
    email = session.get("student_email")
    student = USERS.get(email)

    # A user might not exist after a restart or when a request reaches another
    # worker, because the demo account dictionary only lives in this process.
    if email and student is None:
        session.clear()

    return student


def is_valid_email(email):
    """Perform a simple format check suitable for this classroom example."""
    return re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email) is not None


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Register a student in memory, storing only a password hash."""
    if get_current_student():
        return redirect(url_for("home"))

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().casefold()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not full_name or not email or not password or not confirm_password:
            flash("Please complete every field.", "danger")
        elif not is_valid_email(email):
            flash("Enter a valid email address.", "danger")
        elif email in USERS:
            flash("An account with that email already exists. Please log in.", "danger")
        elif len(password) < 8:
            flash("Choose a password with at least 8 characters.", "danger")
        elif password != confirm_password:
            flash("The passwords do not match. Please try again.", "danger")
        else:
            USERS[email] = {
                "name": full_name,
                "password_hash": generate_password_hash(password),
            }
            flash("Your account was created. Please log in.", "success")
            return redirect(url_for("login"))

        return render_template(
            "signup.html",
            full_name=full_name,
            email=request.form.get("email", "").strip(),
        )

    return render_template("signup.html", full_name="", email="")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Check a student's password and create a signed-in session."""
    if get_current_student():
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().casefold()
        password = request.form.get("password", "")
        student = USERS.get(email)

        if student and check_password_hash(student["password_hash"], password):
            session.clear()
            session["student_email"] = email
            flash(f"Welcome back, {student['name']}!", "success")
            return redirect(url_for("home"))

        flash("Email or password is incorrect.", "danger")
        return render_template("login.html", email=request.form.get("email", "").strip())

    return render_template("login.html", email="")


@app.route("/logout", methods=["POST"])
def logout():
    """Remove the signed-in student's session."""
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/")
def home():
    """Show searchable notices to signed-in students only."""
    student = get_current_student()
    if not student:
        return redirect(url_for("login"))

    search_text = request.args.get("q", "").strip()

    if search_text:
        visible_notices = [
            notice
            for notice in NOTICES
            if search_text.casefold() in notice["title"].casefold()
        ]
    else:
        visible_notices = NOTICES

    return render_template(
        "index.html",
        notices=visible_notices,
        search_text=search_text,
        total_notices=len(NOTICES),
        student_name=student["name"],
    )


if __name__ == "__main__":
    # PORT is provided by the preview environment or by Docker.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
