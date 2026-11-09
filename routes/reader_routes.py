from flask import Blueprint, current_app, flash, render_template, redirect, url_for,request
from flask_login import login_required
from services.reader_services import add_reader,get_all_readers,delete_reader

reader = Blueprint("reader",__name__)

@reader.route("/reader/add",methods=["GET","POST"])
@login_required
def add():
    if request.method == "GET":
        page = request.args.get("page",1,type=int)
        readers = get_all_readers(page=page)

    if request.method == "POST":
        reader_name = request.form.get("reader_name","").strip()
        phone_number = request.form.get("phone_number","").strip()

        try:
            add_reader(reader_name=reader_name,phone_number=phone_number)
            flash("New reader added successfully.","success")
        except ValueError as error:
            flash(str(error),"error")
        except Exception:
            current_app.logger.exception("Something went wrong while adding the reader.","error")

        return redirect(url_for("reader.add"))
    return render_template("readers.html",readers=readers)

@reader.route("/reader/<int:reader_id>/delete",methods=["POST"])
@login_required
def delete(reader_id):
    try:
        delete_reader(reader_id=reader_id)
        flash("Reader deleted successfully.","success")
    except ValueError as error:
        flash(str(error),"error")
    except Exception:
        current_app.logger.exception("Problem in deleting reader.")
        flash("Something went wrong while deleting the reader.", "error")
    return redirect(url_for("reader.add"))
