from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = "sqlite:///todoapp.db" # create location of the database
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}) # database engine
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://username:password@127.0.0.1:3306/todo_application_database'
SQLALCHEMY_DATABASE_URL = 'postgresql://psql:psql@localhost:5432/todo_application_database'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # like persistent manager
Base = declarative_base()