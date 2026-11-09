from models import db,Admin
from werkzeug.security import generate_password_hash,check_password_hash

def register_user(username,password,confirm_password):
    username = username.strip()

    if not username or not password or not confirm_password:
        raise ValueError("All fields are required.")

    if password != confirm_password:
        raise ValueError("Enter valid password to confirm.")

    existing_username = db.session.execute(
        db.select(Admin).filter(Admin.username==username)
    ).scalar_one_or_none()

    if existing_username:
        raise ValueError("Username already exists.")

    if password != confirm_password:
        raise ValueError("Enter valid password to confirm.")

    hash_password = generate_password_hash(password)


    new_user = Admin(username=username,password=hash_password)

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise


def authenticate_user(username,password):
    username = username.strip()

    if not username or not password:
        raise ValueError("Required all fields.")

    existing_user = db.session.execute(
        db.select(Admin).filter(Admin.username==username)
    ).scalar_one_or_none()

    if not existing_user:
        raise ValueError("Invalid Username or Password.")

    correct_password = check_password_hash(existing_user.password,password)

    if not correct_password:
        raise ValueError("Incorrect password or username")

    return existing_user

