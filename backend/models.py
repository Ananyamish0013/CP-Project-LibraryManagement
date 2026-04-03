from database import db
from datetime import datetime, timezone

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    availability = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'availability': self.availability
        }

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

class IssuedBook(db.Model):
    __tablename__ = 'issued_books'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    issue_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    return_date = db.Column(db.DateTime, nullable=True)

    # Relationships to access related book/user info directly
    book = db.relationship('Book', backref=db.backref('issue_records', lazy=True))
    user = db.relationship('User', backref=db.backref('borrowed_books', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.name if self.user else None,
            'book_id': self.book_id,
            'book_title': self.book.title if self.book else None,
            'issue_date': self.issue_date.strftime('%Y-%m-%d %H:%M:%S') if self.issue_date else None,
            'return_date': self.return_date.strftime('%Y-%m-%d %H:%M:%S') if self.return_date else None
        }
