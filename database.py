import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base

def get_database_url():
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    db_config = config['database']
    return f"postgresql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

engine = create_engine(get_database_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()