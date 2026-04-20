from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from database import db
from models import Book, User, IssuedBook

api_blueprint = Blueprint('api', __name__)

# ================================
# Books Endpoints
# ================================

@api_blueprint.route('/books', methods=['GET'])
def get_books():
    """Retrieve all books or search by title/author.
    Use ?search=query parameter to filter."""
    search_query = request.args.get('search', '')
    
    if search_query:
        books = Book.query.filter(
            Book.title.ilike(f'%{search_query}%') | 
            Book.author.ilike(f'%{search_query}%')
        ).all()
    else:
        books = Book.query.all()
        
    return jsonify([book.to_dict() for book in books]), 200

@api_blueprint.route('/books', methods=['POST'])
def add_book():
    """Add a new book."""
    data = request.json
    
    # Validation
    if not data or not data.get('title') or not data.get('author') or not data.get('genre'):
        return jsonify({'error': 'Title, author, and genre are required fields.'}), 400
        
    new_book = Book(
        title=data['title'],
        author=data['author'],
        genre=data['genre'],
        availability=data.get('availability', True)
    )
    
    db.session.add(new_book)
    db.session.commit()
    
    return jsonify({'message': 'Book added successfully!', 'book': new_book.to_dict()}), 201

@api_blueprint.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Update existing book details."""
    book = Book.query.get_or_404(book_id)
    data = request.json
    
    if 'title' in data: book.title = data['title']
    if 'author' in data: book.author = data['author']
    if 'genre' in data: book.genre = data['genre']
    if 'availability' in data: book.availability = data['availability']
    
    db.session.commit()
    return jsonify({'message': 'Book updated successfully', 'book': book.to_dict()}), 200

@api_blueprint.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete a book from the library catalog."""
    book = Book.query.get_or_404(book_id)
    
    if not book.availability:
        return jsonify({'error': 'Cannot delete an issued book. Please return it first so it can be unlinked safely.'}), 400
        
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'}), 200

# ================================
# Users Endpoints
# ================================

@api_blueprint.route('/users', methods=['GET'])
def get_users():
    """Retrieve all users."""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@api_blueprint.route('/users', methods=['POST'])
def add_user():
    """Add a new user helpers."""
    data = request.json
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({'error': 'Name and email are required to register.'}), 400
        
    # Ensure email is unique
    existing = User.query.filter_by(email=data['email']).first()
    if existing:
        return jsonify({'error': 'A user with this email already exists.'}), 400
        
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully', 'user': new_user.to_dict()}), 201

# ================================
# Issue & Return Endpoints
# ================================

@api_blueprint.route('/issue', methods=['POST'])
def issue_book():
    """Issue a book to a user."""
    data = request.json
    book_id = data.get('book_id')
    user_id = data.get('user_id')
    
    if not book_id or not user_id:
        return jsonify({'error': 'Book ID and User ID are required to issue a book.'}), 400
        
    book = Book.query.get(book_id)
    user = User.query.get(user_id)
    
    if not book:
        return jsonify({'error': 'Book not found.'}), 404
    if not user:
        return jsonify({'error': 'User not found.'}), 404
        
    if not book.availability:
        return jsonify({'error': 'This book is already issued to someone else.'}), 400
        
    # Mark book unavailable
    book.availability = False
    
    # Create issue tracking record
    issue_record = IssuedBook(
        user_id=user.id,
        book_id=book.id,
        issue_date=datetime.now(timezone.utc)
    )
    
    db.session.add(issue_record)
    db.session.commit()
    
    return jsonify({'message': f'Book "{book.title}" successfully issued to {user.name}', 'record': issue_record.to_dict()}), 200

@api_blueprint.route('/return', methods=['POST'])
def return_book():
    """Return a previously issued book."""
    data = request.json
    book_id = data.get('book_id')
    
    if not book_id:
        return jsonify({'error': 'Book ID is required to return a book.'}), 400
        
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found.'}), 404
        
    if book.availability:
        return jsonify({'error': 'This book is already available in the library.'}), 400
        
    # Find the active issue record
    record = IssuedBook.query.filter_by(book_id=book.id, return_date=None).first()
    
    if not record:
        # Fallback in case of strange data states, forces book back to available
        book.availability = True
        db.session.commit()
        return jsonify({'error': 'No active issue record found, but book status reset to available.'}), 500
        
    # Mark return status
    record.return_date = datetime.now(timezone.utc)
    book.availability = True
    
    db.session.commit()
    
    return jsonify({'message': f'Book "{book.title}" was safely returned.', 'record': record.to_dict()}), 200

@api_blueprint.route('/issued', methods=['GET'])
def get_issued_books():
    """Retrieve all issued books that have not yet been returned."""
    records = IssuedBook.query.filter(IssuedBook.return_date == None).all()
    return jsonify([record.to_dict() for record in records]), 200
@api_blueprint.route('/')
def home():
    return "Library API is running "