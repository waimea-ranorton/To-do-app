#===========================================================
# APP NAME HERE
# By YOUR NAME HERE
#===========================================================

from flask import Flask, request, session, render_template, flash, redirect, send_file, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from os import getenv
from io import BytesIO
import html
from app.helpers import *


# Create the app
app = Flask(__name__)


#===========================================================
# App Routes Handlers
#===========================================================

#-----------------------------------------------
#  Show all the tasks
#-----------------------------------------------------------
@app.get("/")
def show_all_tasks():
    with connect_db() as db:
        sql = """
            SELECT id, name, priority, complete
            FROM tasks
            ORDER By priority ASC
        """
        params = ()
        tasks = db.execute(sql, params).fetchall()

        return render_template("pages/tasks_list.jinja", tasks=tasks)

#-----------------------------------------------------------
# Add a new task
#-----------------------------------------------------------
@app.post("/task/new")
def process_task_form():
    #get form data
    name = request.form.get("name", "unknown").strip() #default value if no species
    priority = request.form.get("priority", "unknown").strip()

    #connect to the DB
    with connect_db() as db:
        sql = """
            INSERT INTO tasks (priority, name)
            VALUES (?, ?)
        """
        params = (name, priority)

        #run query
        db.execute(sql, params)

        flash(f"Task {name} added successfully")

        #done, return to list
        return redirect("/")

#-----------------------------------------------------------
# Mark task finished
#-----------------------------------------------------------
@app.get("/task/<int:id>/complete")
def mark_task_done(id):
    with connect_db() as db:
        sql = """
            UPDATE tasks SET complete = 1 WHERE id = ?
        """
        params = (id,)
        db.execute(sql, params)

        return redirect("/")

#-----------------------------------------------------------
# Mark task unfinished
#-----------------------------------------------------------
@app.get("/task/<int:id>/incomplete")
def mark_task_not_done(id):
    with connect_db() as db:
        sql = """
            UPDATE tasks SET complete = 0 WHERE id = ?
        """
        params = (id,)
        db.execute(sql, params)

        return redirect("/")        

#-----------------------------------------------------------
# Task deletion
#-----------------------------------------------------------
@app.get("/task/<int:id>/delete")
def delete_a_task(id):
    with connect_db() as db:
        ##delete task using its id
        sql = """
            DELETE FROM tasks
            WHERE id=?
        """
        params = (id,)
        db.execute(sql, params)


        flash("task deleted", "success")
##back to list
        return redirect("/")

#-----------------------------------------------------------
# Help page - Show some help
#-----------------------------------------------------------
@app.get("/help")
def show_help():

    flash("Flash test message")
    flash("Flash test message with a longer bit of text")
    flash("Success test message", "success")
    flash("Error test message", "error")

    return render_template("pages/help.jinja")


#===========================================================
# Configure the app
#===========================================================
load_dotenv()
app.config.from_prefixed_env()
init_logging(app)
init_text_filters(app)
init_date_filters(app)
init_error_handlers(app)
init_database()
register_commands(app)

