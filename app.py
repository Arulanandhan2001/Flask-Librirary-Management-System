from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean, default=True)

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        new_book = Book(title=title, author=author, year=int(year))
        db.session.add(new_book)
        db.session.commit()
        flash('Book Added Successfully!')
        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.year = int(request.form['year'])
        db.session.commit()
        flash('Book Updated Successfully!')
        return redirect(url_for('index'))
    return render_template('edit_book.html', book=book)

@app.route('/delete/<int:id>')
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Book Deleted Successfully!')
    return redirect(url_for('index'))

@app.route('/borrow/<int:id>')
def borrow_book(id):
    book = Book.query.get_or_404(id)
    if book.available:
        book.available = False
        db.session.commit()
        flash('Book Borrowed!')
    else:
        flash('Book is already borrowed!')
    return redirect(url_for('index'))

@app.route('/return/<int:id>')
def return_book(id):
    book = Book.query.get_or_404(id)
    if not book.available:
        book.available = True
        db.session.commit()
        flash('Book Returned!')
    else:
        flash('Book was already returned!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
