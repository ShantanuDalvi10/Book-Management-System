from models import db,Assignment,Reader,Book

def assign_book(reader_id,book_id):
    book = db.session.get(Book,book_id)
    if book is None:
        raise ValueError("Enter the valid Book Id.")
    reader = db.session.get(Reader,reader_id)
    if reader is None:
        raise ValueError("Enter valid Reader Id.")
    if book.available_copies < 1:
        raise ValueError("Available copies cannot be zero or negative.")

    try:
        assign = Assignment(book_id=book_id,reader_id=reader_id,status="Issued")
        db.session.add(assign)
        book.available_copies -= 1
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

def get_assigned_books(page=1,per_page=5):
    return db.paginate(
        db.select(Assignment).order_by(Assignment.id.asc()),
    page=page,per_page=per_page,error_out=False)

def book_returns(assignment_id):
    assignment = db.session.execute(
        db.select(Assignment).filter(Assignment.id==assignment_id)
    ).scalar_one_or_none()
    if assignment is None:
        raise ValueError("Assignment is not found.")
    if assignment.status != "Issued":
        raise ValueError("Book is not issued")
    try:
        assignment.book.available_copies += 1
        db.session.delete(assignment)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

