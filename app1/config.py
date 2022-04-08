from dotenv import load_dotenv
import os


load_dotenv()


class Configuration:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:{os.getenv("DB_PASSWORD")}@localhost/blogtest'
    SECRET_KEY = os.getenv('SECRET_KEY')
    SECURITY_PASSWORD_SALT = 'Salt+gdfgfdg88 aawerf838 if@ (Ifdg-9 i(_#'
    SECURITY_PASSWORD_HASH = "pbkdf2_sha512"