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
            INSERT INTO tasks (name, priority)
            VALUES (?, ?)
        """
        params = (name, priority)

        #run query
        db.execute(sql, params)

        flash(f"Task {name} added successfully")

        #done, return to list
        return redirect("/")

#-----------------------------------------------
# Mark task finished
#-----------------------------------------------------------
@app.get("/task/<int:id>/complete")
def mark_task_done():
    with connect_db() as db:
        sql = """
            SELECT id, name, priority, complete
            FROM tasks
        """
        params = ()
        tasks = db.execute(sql, params).fetchall()

        return render_template("pages/tasks_list.jinja", tasks=tasks)
        
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

