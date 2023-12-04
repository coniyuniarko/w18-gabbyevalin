import datetime
from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash

from w18_gabbyevalin import db


class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(96), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(96), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def to_json(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name
        }


class Product(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(96), nullable=False)
    description: Mapped[str] = mapped_column(String(96), nullable=False)
    priority: Mapped[str] = mapped_column(String(96), nullable=False)
    due_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date.strftime("%Y-%m-%d"),
        }
