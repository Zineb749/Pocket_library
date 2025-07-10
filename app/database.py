# database.py
# Gère la connexion à la base de données MySQL
# Fournit les outils pour créer des modèles et interagir avec la base
# Utilisé par SQLAlchemy avec FastAPI

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de connexion à la base de données MySQL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:TonNouveauMotDePasse@localhost:3306/pocket_library"

# Création du moteur SQLAlchemy qui gère la connexion à MySQL
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True  # Vérifie que la connexion est encore active avant d'envoyer une requête
)

# Création d'une session pour interagir avec la base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base à partir de laquelle tous les modèles de tables hériteront
Base = declarative_base()

# Fonction utilisée dans FastAPI pour fournir une session à chaque requête
# Elle ouvre une session à la base et la ferme automatiquement à la fin
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
