from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Remplace par tes infos MySQL (utilisateur, mot de passe, host, port, nom de la base)
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:TonNouveauMotDePasse@localhost:3306/pocket_library"

# Création du moteur SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Utile pour MySQL pour garder la connexion vivante
)

# Création de la session liée à ce moteur
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base de déclaration des modèles SQLAlchemy
Base = declarative_base()

# Fonction dépendance FastAPI pour fournir une session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
