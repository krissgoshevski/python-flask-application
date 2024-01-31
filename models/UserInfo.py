from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class UserInfo(db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    #  relationship between Userinfo and UserSpending
    spendings = db.relationship('UserSpending', backref='user_info', lazy=True)



    def __repr__(self):
        return f"<Userinfo(id={self.id}, name={self.name}, email={self.email}, age={self.age})>"




class UserSpending(db.Model):
    __tablename__ = 'user_spending'

    money_spent = db.Column(db.Float, nullable=False)
    year = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user_info.id', ondelete='CASCADE'),  # ondelete cascade
        primary_key=True,
        nullable=False
    )

    def __repr__(self):
        return (f"<UserSpending(id={self.id},"
                f" money_spent={self.money_spent},"
                f" year={self.year},"
                f" user_id={self.user_id})>")

