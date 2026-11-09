from models import db,Reader,Assignment

def add_reader(reader_name,phone_number):
    reader_name = reader_name.strip()
    phone_number = phone_number.strip()

    if not reader_name or not phone_number:
        raise ValueError("All fields are required.")
    existing_phone_number = db.session.execute(
        db.select(Reader).filter(Reader.phone_number==phone_number)
    ).scalar_one_or_none()
    if existing_phone_number:
        raise ValueError("Phone number already exists.")
    new_reader = Reader(reader_name=reader_name,phone_number=phone_number)
    try:
        db.session.add(new_reader)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

def get_all_readers(page=1,per_page=5):
    return db.paginate(
        db.select(Reader).order_by(Reader.id.asc()),
    page=page,per_page=per_page,error_out=False)

def delete_reader(reader_id):
    reader = db.session.execute(
        db.select(Reader).filter(Reader.id==reader_id)
    ).scalar_one_or_none()
    if not reader:
        raise ValueError("Reader does not exists.")
    book_issued = db.session.execute(
        db.select(Assignment).filter(Assignment.reader_id==reader_id,
                                     Assignment.status=="Issued")
    ).scalar_one_or_none()
    if book_issued:
        raise ValueError("Reader is assigned with book, it cannot be deleted.")
    try:
        db.session.delete(reader)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
