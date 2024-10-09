import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# # Caminho do Banco de Dados SQLite
# DATABASE_URL = f"sqlite:///{os.path.join(os.path.dirname(__file__), '../database/database.db')}"

# # Configuração do SQLAlchemy
# engine = create_engine(DATABASE_URL, echo=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()
