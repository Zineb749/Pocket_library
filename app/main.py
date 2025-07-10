"""
Point d'entrée principal de l'application Pocket Library API.

Ce fichier configure l'application FastAPI, gère les middlewares, la création des tables
en base de données au démarrage, et inclut les différents routeurs pour organiser les routes.

Il configure également la politique CORS pour permettre les appels API depuis le frontend Vue.js local.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base

# Import des routeurs principaux, renommés dans le __init__.py du dossier routers
from app.routers import auth_router, books_router, mybooks_router, users_router

# Import du routeur utilitaire pour l'import de livres via Google Books API
from app.utils.google_books_import import router as google_books_router

# Création de l'instance FastAPI avec un titre
app = FastAPI(title="Pocket Library API")

# Middleware CORS pour autoriser les requêtes venant du frontend Vue.js en local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adresse du frontend Vue.js en local
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Autorise tous les headers
)

# Evénement au démarrage de l'application : création des tables dans la base si elles n'existent pas
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Inclusion des routeurs avec leurs préfixes et tags pour organiser les routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(books_router, prefix="/books", tags=["books"])
app.include_router(mybooks_router, prefix="/user-books", tags=["user_books"])
app.include_router(users_router, prefix="/users", tags=["users"])

# Routeur pour importer des livres via l'API Google Books, avec un préfixe dédié
app.include_router(google_books_router, prefix="/books/import-google-books", tags=["google_books"])

# Route racine simple pour vérifier que l'API fonctionne
@app.get("/")
async def root():
    return {"message": "Bienvenue sur Pocket Library API"}
