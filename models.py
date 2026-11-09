from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

class Admin(db.Model,UserMixin):
    __tablename__ ="admins"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),unique=True,nullable=False)
    password = db.Column(db.String(512),nullable=False)

class Book(db.Model):
    __tablename__="books"
    id = db.Column(db.Integer,primary_key=True)
    book_name = db.Column(db.String(100),nullable=False)
    author = db.Column(db.String(100),nullable=False)
    total_copies = db.Column(db.Integer,nullable=False)
    available_copies = db.Column(db.Integer,nullable=False)
    assignments = db.relationship("Assignment",back_populates="book")

class Reader(db.Model):
    __tablename__="readers"
    id = db.Column(db.Integer,primary_key=True)
    reader_name = db.Column(db.String(100),nullable=False)
    phone_number = db.Column(db.String(50),nullable=False,unique=True)
    assignments = db.relationship("Assignment",back_populates="reader")

class Assignment(db.Model):
    __tablename__="book_assignments"
    id = db.Column(db.Integer,primary_key=True)
    book_id = db.Column(db.Integer,db.ForeignKey("books.id"),nullable=False)
    reader_id = db.Column(db.Integer,db.ForeignKey("readers.id"),nullable=False)
    status = db.Column(db.String(20),nullable=False)
    book = db.relationship("Book",back_populates="assignments")
    reader = db.relationship("Reader",back_populates="assignments")