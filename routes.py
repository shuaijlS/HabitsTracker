from flask import Blueprint, redirect, render_template, request, redirect, url_for
from collections import defaultdict
import datetime

pages=Blueprint("habits", __name__, template_folder="templates", static_folder="stsatic")
habits = ["Test habit", "Test habit2"]
completions = defaultdict(list)


@pages.context_processor
def add_calc_date_range():
    def date_range(start: datetime.date):
        dates = [start + datetime.timedelta(days = diff) for diff in range(-3,4)]
        return dates
    return {"date_range":date_range}

@pages.route("/")
def index():
    date_str = request.args.get("date")
    if date_str:
        selected_date = datetime.date.fromisoformat(date_str)
    else:
        selected_date = datetime.date.today()
    return render_template("index.html",
     habits=habits, 
     title="Habit Tracker - Home", 
     completions=completions[selected_date],
     selected_date = selected_date)

@pages.route("/add", methods=["GET", "POST"])
def add_habit():
    if request.method== "POST":
        habit = request.form.get("habit")
        habits.append(habit)
    return render_template("add_habit.html", title="Habit Tracker - Add Habit", selected_date = datetime.date.today())

@pages.post("/complete")
def complete():
    date_string = request.form.get("date")
    habit = request.form.get("habitName")
    date = datetime.date.fromisoformat(date_string)
    completions[date].append(habit)
    return redirect(url_for("habits.index",date=date_string))