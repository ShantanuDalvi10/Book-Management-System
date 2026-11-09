from models import db,Book
from sqlalchemy import func

def get_all_books(page=1,per_page=5):
    return db.paginate(
        db.select(Book).order_by(Book.id.asc()),
    page = page,per_page=per_page,error_out=False)

def add_book(book_name,author,number_of_copies):
    book_name = book_name.strip()
    author = author.strip()
    if not book_name or not author or not number_of_copies:
        raise ValueError("Enter all required fields.")

    try:
        number_of_copies = int(number_of_copies)
    except ValueError:
        raise ValueError("Number of Copies should be Integer not text or float.")

    if number_of_copies <= 0:
        raise ValueError("Number of Copies should be positive whole number which shouldn't be text.")

    try:
        existing_book = db.session.execute(
            db.select(Book).filter(func.lower(Book.book_name)==book_name.lower(),func.lower(Book.author)==author.lower())
        ).scalar_one_or_none()
        if existing_book:
            existing_book.total_copies = existing_book.total_copies + number_of_copies
            existing_book.available_copies = existing_book.available_copies + number_of_copies
            db.session.commit()
        else:
            new_book = Book(book_name=book_name,author=author,total_copies=number_of_copies,available_copies=number_of_copies)
            db.session.add(new_book)
            db.session.commit()
    except Exception:
        db.session.rollback()
        raise

def search_book(search_text):
    search_text = search_text.strip()
    if not search_text:
        raise ValueError("Enter book name to search.")
    book = db.session.execute(
        db.select(Book).where(Book.book_name.contains(search_text))
    ).scalars().all()
    return book

def delete_book(book_id):
    book = db.session.execute(
        db.select(Book).filter(Book.id==book_id)
    ).scalar_one_or_none()
    if not book:
        raise ValueError("Book ID is not exist.")
    if book.total_copies != book.available_copies:
        raise ValueError("Book cannot be deleted. All books are not returned yet.")
    try:
        db.session.delete(book)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

def get_available_books():
    return db.session.execute(
        db.select(Book).filter(Book.available_copies > 0).order_by(Book.id.asc())
    ).scalars().all()
