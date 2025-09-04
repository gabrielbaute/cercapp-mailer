from datetime import datetime
from flask import Blueprint, request, render_template, flash, send_from_directory, url_for, redirect
from flask_login import login_required, current_user

from src.server.forms import CSVUploadForm

main_bp = Blueprint("main", __name__, template_folder="templates")

@main_bp.route("/")
@login_required
def home():
    return redirect(url_for("main.index"))

@main_bp.route("/index")
@login_required
def index():
    return render_template("main/index.html")

@main_bp.route("/load_file", methods=["GET", "POST"])
@login_required
def load_file():
    form = CSVUploadForm()
    if form.validate_on_submit():
        file = form.csv_file.data
        filename = f"{current_user.id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{file.filename}"
        if not filename.lower().endswith('.csv'):
            flash("Por favor, suba un archivo CSV válido.", "danger")
            return render_template("main/load_file.html", form=form)
        file.save(f"data/uploads/{filename}")
    return render_template("main/load_file.html", form=form)