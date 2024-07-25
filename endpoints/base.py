from flask import Blueprint, render_template

router = Blueprint(name='base', import_name="base_router", url_prefix='/')


@router.route("/")
def index():
    return render_template("auth_page.html")