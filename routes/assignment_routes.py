from flask import Blueprint, current_app, flash, render_template, redirect, url_for,request
from flask_login import login_required
from services.reader_services import get_all_readers
from services.dashboard_services import get_available_books
from services.assigments_services import assign_book,get_assigned_books,book_returns
assign = Blueprint("assign",__name__)

@assign.route("/assignments")
@login_required
def assignments_page():
    readers = get_all_readers()
    books = get_available_books()
    page = request.args.get("page",1,type=int)
    assignments = get_assigned_books(page)
    return render_template("assignments.html",readers=readers,books=books,assignments=assignments)

@assign.route("/assign-book",methods=["POST"])
@login_required
def assign_book_route():
    try:
        reader_id = int(request.form.get("reader",""))
        book_id = int(request.form.get("book",""))
    except ValueError:
        flash("Reader ID and Book ID must be integer.","error")
        return redirect(url_for("assign.assignments_page"))
    try:
        assign_book(reader_id=reader_id,book_id=book_id)
        flash("Book is assigned successfully.","success")
    except ValueError as error:
        flash(str(error),"error")
    except Exception:
        current_app.logger.exception("Some problem in assigning book.")
        flash("Some problem in assigning book.","error")
    return redirect(url_for("assign.assignments_page"))


@assign.route("/return-book/<int:assignment_id>",methods=["POST"])
@login_required
def return_book_route(assignment_id):
    try:
        book_returns(assignment_id)
        flash("Book returned successfully.","success")
    except ValueError as error:
        flash(str(error),"error")
    except Exception:
        current_app.logger.exception("There is a problem in deleting book.")
        flash("There is a problem in returning book.","error")
    return redirect(url_for("assign.assignments_page"))
