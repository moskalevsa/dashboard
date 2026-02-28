from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker



#Настройка подключения к базе данных**
DATABASE_URL = 'postgresql://postgres:Crba@localhost:5432/dronsevents'
# Создание двигателя базы данных
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase): pass

query = ("""
         SELECT eventsdatetime
           ,eventcount
           ,class as clas
           ,unitcode
           ,district
		   ,size
           ,adresse
           FROM events.dronevent
           """)

#print (query)



