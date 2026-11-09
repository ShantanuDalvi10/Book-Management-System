from flask import Blueprint, current_app, flash, render_template, redirect, url_for,request
from flask_login import login_required
from services.dashboard_services import get_all_books,add_book,search_book,delete_book

dash = Blueprint("dash",__name__)

@dash.route("/dashboard",methods=["GET"])
@login_required
def dashboard():
    searched_results=False
    page = request.args.get("page",1,type=int)
    books = get_all_books(page=page)
    print("Current page:", books.page)
    print("Per page:", books.per_page)
    print("Total records:", books.total)
    print("Records returned:", len(books.items))
    return render_template("dashboard.html",books=books,searched_results=searched_results)

@dash.route("/add-book",methods=["POST"])
@login_required
def add_new_book():

    book_name = request.form.get("book_name","").strip()
    author = request.form.get("book_author","").strip()
    number_of_copies = request.form.get("number_of_copies")
    try:
        add_book(book_name=book_name,author=author,number_of_copies=number_of_copies)
        flash("Book added successfully.","success")
    except ValueError as error:
        flash(str(error),"error")
    except Exception:
        current_app.logger.exception("Book couldn't be added.")
        flash("New book cannot be added","error")
    return redirect(url_for("dash.dashboard"))

@dash.route("/book/search",methods=["GET"])
@login_required
def search():
    search_text = request.args.get("book_name","").strip()
    books = get_all_books()
    search_results = []
    searched_results = True
    try:
        search_results = search_book(search_text=search_text)
    except ValueError as error:
        flash(str(error),"error")
        books=get_all_books()
    else:
        if not search_results:
            flash("Book Not Found","error")
    return render_template("dashboard.html",search_results=search_results,books=books,searched_results=searched_results)

@dash.route("/book/<path:book_id>/delete",methods=["POST"])
@login_required
def delete(book_id):
    try:
        delete_book(book_id=book_id)
        flash("Book is deleted successfully.","success")
    except ValueError as error:
        flash(str(error),"error")
    except Exception:
        current_app.logger.exception("Error in book deletion.")
        flash("Error in book deletion","error")
    return redirect(url_for("dash.dashboard"))





