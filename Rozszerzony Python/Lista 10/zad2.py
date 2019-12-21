import sqlalchemy as db
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import sys


engine = db.create_engine('sqlite:///zad2.db')
Session = sessionmaker(bind=engine)
conn = engine.connect()
Base = declarative_base()


class Movie(Base):
    __tablename__ = 'movies'
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.VARCHAR)
    year = db.Column('year', db.Integer)
    people = relationship('People')

    def __init__(self, title, year):
        self.title = title
        self.year = year


class People(Base):
    __tablename__ = 'people'
    id = db.Column('id', db.Integer, primary_key=True)
    director = db.Column('director', db.VARCHAR)
    producer = db.Column('producer', db.VARCHAR)
    movie_id = db.Column('movie_id', db.ForeignKey('movies.id'))

    def __init__(self, dir, prod, m_id):
        self.director = dir
        self.producer = prod
        self.movie_id = m_id


if __name__ == '__main__':
    if len(sys.argv) == 1:
        exit()

    Base.metadata.create_all(engine)
    session = Session()

    _new = None
    if sys.argv[1] == 'movies':
        if sys.argv[2] == '--add':
            _new = Movie(*sys.argv[3:])

        elif sys.argv[2] == '--show-all':
            movies = session.query(Movie).all()
            print('\n### All movies')
            for m in movies:
                print(f'{m.title} released on {m.year}')

    elif sys.argv[1] == 'people':
        if sys.argv[2] == '--add':
            _new = People(*sys.argv[3:])
        elif sys.argv[2] == '--show-all':
            people = session.query(People).all()
            print('\n### All people')
            for p in people:
                print(f'Director: {p.director}, producer: {p.producer}, movie_id: {p.movie_id}')

    if _new is not None:
        session.add(_new)
        session.commit()
        session.close()
