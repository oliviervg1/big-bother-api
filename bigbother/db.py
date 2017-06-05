import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

DB_ENDPOINT = os.environ["DB_ENDPOINT"]

engine = create_engine(DB_ENDPOINT)
Session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base()
Base.query = Session.query_property()


def init_db():
    from models import Room, Person
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Fixtures
    session = Session()

    main_area = Room(name='main area', city='london')
    kitchen = Room(name='kitchen', city='london')
    reception = Room(name='reception', city='london')
    juannex = Room(name='juannex', city='london')
    session.add_all([main_area, kitchen, reception, juannex])

    j_s = Person(full_name='john smith')
    j_s.room = kitchen
    j_d = Person(full_name='john doe')
    j_d.room = kitchen
    a_s = Person(full_name='alice springs')
    a_s.room = juannex
    session.add_all([j_s, j_d, a_s])
    session.commit()
