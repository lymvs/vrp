"""Main script for the flask app."""
from datetime import timedelta

import pandas as pd
from flask import Flask, redirect, render_template, request, session, url_for
from flask.typing import ResponseReturnValue
from requests import Response

from flask_session import Session
from functions import (
    create_data_model,
    solver_ortools_cvrp,
    solver_ortools_vrp,
)

# Constants
VRP_VARIATIONS = {
    "Vehicle Routing Problem": ["vrp", "active"],  # [vrp_variation, active/disabled state] # noqa: E501
    "Capacitated VRP": ["cvrp", "active"],
    "VRP with Time Windows": ["vrptw", "disabled"],
    "VRP with Pickup and Delivery": ["vrppd", "disabled"],
    "VRP with Backhauls": ["vrpb", "disabled"],
    }

TABS = {
    "Overview": ["/", "home"],  # [route, endpoint]
    "Upload Files": ["/upload_files", "upload_files"],
    "Solver": ["/solver", "solver"],
    "Output": ["/output", "output"],
    }


# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
Session(app)


@app.after_request
def after_request(response: Response) -> Response:
    """Ensure responses aren't cached."""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.context_processor
def inject_tabs() -> dict:
    """Inject menu tabs to each template."""
    tabs = TABS
    return dict(tabs=tabs)


@app.route("/", methods=["GET", "POST"], endpoint="home")
def index() -> ResponseReturnValue:
    """Homepage."""
    return render_template(
        "index.html",
        vrp_variations=VRP_VARIATIONS,
        )


@app.route("/upload_files", methods=["GET", "POST"], endpoint="upload_files")
def upload() -> ResponseReturnValue:
    """Upload files."""
    if request.method == "POST":
        if (not request.files.get("customers")
           or not request.files.get("vehicles")):
            return render_template("apology.html")

        # Get files from input widgets
        customers_file = request.files.get("customers")
        vehicles_file = request.files.get("vehicles")

        # Read csv files into pandas dataframes
        customers_df = pd.read_csv(customers_file)
        vehicles_df = pd.read_csv(vehicles_file)

        # Create the data model
        data = create_data_model(customers_df, vehicles_df)

        session["data"] = data

        return redirect(url_for("solver"))

    # List of file requirements
    input_files_list = {
        "customers": "Upload Customers Data",
        "vehicles": "Upload Vehicles Data",
    }

    return render_template("upload_files.html", files_list=input_files_list)


@app.route("/solver", methods=["GET", "POST"], endpoint="solver")
def solver() -> ResponseReturnValue:
    """Run solver."""
    data = session.get("data", {})

    if request.method == "POST":
        option = request.form.get("vrp_variation")

        if option == "vrp":

            session["solution"] = solver_ortools_vrp(data)

            return redirect(url_for("output"))

        elif option == "cvrp":

            session["solution"] = solver_ortools_cvrp(data)

            return redirect(url_for("output"))

    return render_template("solver.html", vrp_variations=VRP_VARIATIONS)


@app.route("/output", methods=["GET"], endpoint="output")
def output() -> ResponseReturnValue:
    """Print the output to the user."""
    solution = session.get("solution", {})

    return render_template("output.html", solution=solution)
