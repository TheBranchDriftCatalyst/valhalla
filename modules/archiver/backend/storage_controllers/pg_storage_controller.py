from os import environ
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker


class PGStorageController:
    
    ENGINE = None
    SESSION = None
    METADATA = MetaData()
    
    @classmethod
    def get_engine(cls):
        if cls.ENGINE is None:
            cls.ENGINE = create_engine(
                f'postgresql://{environ.get("PG_HOST", "localhost"):{environ.get("PG_PORT", "5432")}}/{environ.get("ENV", "dev")}',
                echo=True,
                future=True,
            )
        return cls.ENGINE
    
    @classmethod
    def get_session(cls):
        if cls.SESSION is None:
            cls.SESSION = sessionmaker(bind=cls.ENGINE)
        return cls.SESSION
    
    @classmethod
    def run_migrations_if_needed(cls, alchemy_models):
        engine = cls.get_engine()
        cls.METADATA()
        
    
    def __init__(self):
        self.engine = self.get_engine()
        self.session = self.get_session()
