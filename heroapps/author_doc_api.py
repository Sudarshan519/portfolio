"""
FastAPI app called 'Bookipedia' that serves information about books and their authors. A simple example of a
"many-to-many" relationship *without* extra data.
"""

from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# Make the engine
engine = create_engine("sqlite:///authors_books.db", future=True, echo=True,
                       connect_args={"check_same_thread": False})

# Make the DeclarativeMeta
Base = declarative_base()

# Declare Classes / Tables
book_authors = Table('book_authors', Base.metadata,
    Column('book_id', ForeignKey('books.id'), primary_key=True),
    Column('author_id', ForeignKey('authors.id'), primary_key=True)
)

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    authors = relationship("Author", secondary="book_authors", back_populates='books')

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    books = relationship("Book", secondary="book_authors", back_populates='authors')

# Create the tables in the database
Base.metadata.create_all(engine)



# Insert data
from sqlalchemy.orm import Session
with Session(bind=engine) as session:
    book1 = Book(title="Dead People Who'd Be Influencers Today")
    book2 = Book(title="How To Make Friends In Your 30s")
    
    author1 = Author(name="Blu Renolds")
    author2 = Author(name="Chip Egan")
    author3 = Author(name="Alyssa Wyatt")
    
    book1.authors = [author1, author2]
    book2.authors = [author1, author3]
    
    session.add_all([book1, book2, author1, author2, author3])
    session.commit()

with Session(bind=engine) as session:
    db_book = session.query(Book).\
        options(joinedload(Book.authors)).\
        where(Book.id == 1).one()

schema_book = BookSchema.from_orm(db_book)
print(schema_book.json())
