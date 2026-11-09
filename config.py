import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY","eihht3ybtygvyty985")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL","sqlite:///library.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False