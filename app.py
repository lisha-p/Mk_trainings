from flask import Flask, render_template, request, redirect, url_for, session, send_file
import os
import csv

app = Flask(__name__)
app.secret_key = "mk_secret"

try:
    from replit import db
except ImportError:
    db = {}

# Helpers
def save_to_db(key, value):
    if db is not None:
        db[key] = value

def get_all_students():
    if db is not None:
        return [db[key] for key in db.keys() if key.startswith("student_")]
    return []

def delete_student(key):
    if db is not None:
        del db[key]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "course": request.form["course"],
            "skills": request.form["skills"],
            "resume": request.form["resume"],
        }
        key = f"student_{data['name'].replace(' ', '_').lower()}"
        data["key"] = key
        data["badges"] = ["Resume Alchemist", "Soft Skills Ninja"]
        save_to_db(key, data)
        return redirect(url_for("home"))
    return render_template("form.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if request.form["username"] == "adminmk" and request.form["password"] == "mk123train":
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            return render_template("admin_login.html", error="Invalid credentials")
    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin"))
    students = get_all_students()
    return render_template("admin_dashboard.html", students=students)

@app.route("/admin/delete/<key>", methods=["POST"])
def admin_delete(key):
    if session.get("admin"):
        delete_student(key)
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/export_csv")
def export_csv():
    if not session.get("admin"):
        return redirect(url_for("admin"))
    students = get_all_students()
    file_path = "/mnt/data/students.csv"
    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Email", "Course", "Skills", "Resume"])
        for s in students:
            writer.writerow([s["name"], s["email"], s["course"], s["skills"], s["resume"]])
    return send_file(file_path, as_attachment=True)

@app.route("/resume-analyzer", methods=["GET", "POST"])
def resume_analyzer():
    suggestions = []
    resume_text = ""
    if request.method == "POST":
        resume_text = request.form["resume_text"].lower()
        if "team" not in resume_text:
            suggestions.append("Mention your teamwork experience.")
        if "communication" not in resume_text:
            suggestions.append("Include communication skills.")
        if "project" not in resume_text:
            suggestions.append("Add academic or personal projects.")
        if len(resume_text) < 300:
            suggestions.append("Your resume seems too short.")
    return render_template("resume-analyzer.html", suggestions=suggestions, resume_text=resume_text)

@app.route("/game")
def game():
    return render_template("game.html")

@app.route("/calendar")
def calendar():
    return render_template("calendar.html")

@app.route("/career-bot", methods=["GET", "POST"])
def career_bot():
    recommendation = None
    if request.method == "POST":
        interests = request.form["interests"].lower()
        if "design" in interests and "communication" in interests:
            recommendation = "UX Designer + Soft Skills Pro"
        elif "data" in interests:
            recommendation = "Data Analyst"
        else:
            recommendation = "Career Counselor will reach out."
    return render_template("career_bot.html", recommendation=recommendation)

@app.route("/students/<name>")
def student_portfolio(name):
    key = f"student_{name}"
    student = db.get(key) if db else None
    if not student:
        return "Student not found", 404
    return render_template("portfolio.html", student=student)

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
