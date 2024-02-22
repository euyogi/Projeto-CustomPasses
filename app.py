from datetime import datetime

from generic import Generic
from flask import Flask, redirect, render_template, request

# Get at https://pay.google.com/business/console/ -> API Google Wallet
ISSUER_ID = ...

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"

    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Card visual properties
        properties = dict(logo=request.form.get("logo"), title=request.form.get("title"),
                          subheader=request.form.get("subheader"), header=request.form.get("header"),
                          qr_code_content=request.form.get("qr_code_content"),
                          show_qr_code_content=(request.form.get("show_qr_code_content") == "on"),
                          hex_background_color=request.form.get("hex_background_color"),
                          image=request.form.get("image"))

        # Card text modules
        modules = []
        for pair in request.form.get("inside_values").split(','):
            modules.append(pair.split(':'))
        modules.pop()

        # Create a demo class instance
        # Creates the authenticated HTTP client
        demo = Generic()

        # Creates a class if it weren't created yet
        demo.create_class(issuer_id=ISSUER_ID, class_suffix='0')

        # Create an "Add to Google Wallet" link
        # that generates a new pass class and object
        link = demo.create_jwt_new_objects(issuer_id=ISSUER_ID,
                                           class_suffix='0',
                                           object_suffix=datetime.now().strftime("%d%m%y%H%M%S"),
                                           properties=properties,
                                           modules=modules)

        return redirect(link)

    else:
        return render_template("index.html")
