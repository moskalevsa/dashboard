from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



#Настройка подключения к базе данных**
DATABASE_URL = 'postgresql://postgres:Crba@localhost:5432/dronsevents'
# Создание двигателя базы данных
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

query = ("""
         SELECT eventsdatetime
           ,eventcount
           ,name
           ,unitcode
           ,district
           ,adresse
           FROM events.dronevent;
           """)

#print (query)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


