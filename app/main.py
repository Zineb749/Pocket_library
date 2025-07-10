from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base

# Import des routers renommés dans __init__.py
from app.routers import auth_router, books_router, mybooks_router, users_router

# Import du router d'import Google Books
from app.utils.google_books_import import router as google_books_router

# Création de l'application FastAPI
app = FastAPI(title="Pocket Library API")

# Middleware CORS pour autoriser le frontend (Vue.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # autorise les appels depuis Vue.js en local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crée les tables dans la base si elles n'existent pas
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Inclusion des différents routeurs
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(books_router, prefix="/books", tags=["books"])
app.include_router(mybooks_router, prefix="/user-books", tags=["user_books"])
app.include_router(users_router, prefix="/users", tags=["users"])

# Route d'import Google Books avec un prefix plus simple
app.include_router(google_books_router, prefix="/books/import-google-books", tags=["google_books"])

# Route racine
@app.get("/")
async def root():
    return {"message": "Bienvenue sur Pocket Library API"}
