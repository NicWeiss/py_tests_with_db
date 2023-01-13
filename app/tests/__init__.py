from testcontainers.postgres import PostgresContainer

import sqlalchemy
from sqlalchemy.orm import sessionmaker


postgres = PostgresContainer("postgres:13")
postgres.start()

engine = sqlalchemy.create_engine(postgres.get_connection_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
