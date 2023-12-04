from os import environ

SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI") or "sqlite:///w18.db"
SECRET_KEY = environ.get("SECRET_KEY") or "BYsy7iWyuEUiOGNObpb7zoW7FGxKbgW4"