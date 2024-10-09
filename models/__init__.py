from sqlalchemy.ext.declarative import declarative_base

# Criar o objeto Base
Base = declarative_base()

# Importe suas models aqui
from .camada_model import Camada  # Exemplo, ajuste conforme o nome das classes
from .ordem_model import Ordem