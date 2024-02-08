from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'sqlite:///./sql_app.db' #подключение к базе данных SQLite

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}) #создание "движка" SQLAlchemy

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #Каждый экземпляр класса SessionLocal будет сеансом бд
#autocommit=False означает, что каждая операция записи (INSERT, UPDATE, DELETE) не будет автоматически фиксироваться в бд.
#autoflush=False отключает автоочистку для сессии
#bind=engine связывает сессию с экземпляром движка SQLAlchemy, указывая, с какой базой данных должна взаимодействовать эта сессия

Base = declarative_base() #создаёт базовый класс для объявления моделей данных с использованием декларативного подхода