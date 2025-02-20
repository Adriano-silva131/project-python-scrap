from sqlalchemy import create_engine

url = "postgresql+psycopg2://adriano:Z2s!Ys3BVz7tpmb@localhost:5432/cenciveste"

engine = create_engine(url)

try:
    with engine.connect() as connection:
        print("Conexão com o banco de dados estabelecida com sucesso!")
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
