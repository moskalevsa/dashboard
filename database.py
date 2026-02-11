from sqlalchemy import create_engine


#Настройка подключения к базе данных**
DATABASE_URL = 'postgresql://postgres:Crba@localhost:5432/dronsevents'
# Создание асинхронного двигателя базы данных
engine = create_engine(DATABASE_URL, echo=True)

query = ("""
         SELECT eventsdatetime
           ,eventcount
           ,name
           ,unitcode
           ,district
           ,adresse
           FROM events.dronevent;
           """)

print (query)


